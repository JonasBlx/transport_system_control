import numpy as np
import time
import torch

class EpisodeBuffer():
    def __init__(self, max_episode_steps, max_episodes, discounts, tau_discounts, gamma):
        # Initialize buffer parameters
        self.max_episode_steps = max_episode_steps
        self.max_episodes = max_episodes
        self.discounts = discounts
        self.tau_discounts = tau_discounts
        self.gamma = gamma
        
        # Initialize memory buffers
        self.states_mem = np.zeros((max_episodes, max_episode_steps), dtype=np.object)
        self.actions_mem = np.zeros((max_episodes, max_episode_steps), dtype=np.object)
        self.logpas_mem = np.zeros((max_episodes, max_episode_steps), dtype=np.object)
        self.returns_mem = np.zeros((max_episodes, max_episode_steps), dtype=np.object)
        self.gaes_mem = np.zeros((max_episodes, max_episode_steps), dtype=np.object)
        self.episode_steps = np.zeros(max_episodes, dtype=np.uint16)
        self.episode_reward = np.zeros(max_episodes, dtype=np.float32)
        self.episode_exploration = np.zeros(max_episodes, dtype=np.float32)
        self.episode_seconds = np.zeros(max_episodes, dtype=np.float64)
        self.current_ep_idxs = np.arange(max_episodes)

    def fill(self, envs, policy_model, value_model):
        # Number of workers (assuming envs is a vectorized environment)
        n_workers = envs.num_envs

        # Reset the environments and get initial states
        states = envs.reset()

        # Initialize buffers for worker rewards, exploration status, steps, and timestamps
        we_shape = (n_workers, self.max_episode_steps)
        worker_rewards = np.zeros(shape=we_shape, dtype=np.float32)
        worker_exploratory = np.zeros(shape=we_shape, dtype=np.bool)
        worker_steps = np.zeros(shape=(n_workers), dtype=np.uint16)
        worker_seconds = np.array([time.time()] * n_workers, dtype=np.float64)

        buffer_full = False

        # Main loop to fill the episode buffer
        while not buffer_full and len(self.episode_steps[self.episode_steps > 0]) < self.max_episodes / 2:
            with torch.no_grad():
                # Get actions, log probabilities, and exploratory status from the policy model
                actions, logpas, are_exploratory = policy_model.np_pass(states)

                # Get value estimates from the value model
                values = value_model(states)

                # Take a step in the environments using the selected actions
                next_states, rewards, terminals, infos = envs.step(actions)

                # Store states, actions, log probabilities, and rewards in the memory buffers
                self.states_mem[self.current_ep_idxs, worker_steps] = states
                self.actions_mem[self.current_ep_idxs, worker_steps] = actions
                self.logpas_mem[self.current_ep_idxs, worker_steps] = logpas
                worker_exploratory[np.arange(n_workers), worker_steps] = are_exploratory
                worker_rewards[np.arange(n_workers), worker_steps] = rewards

                # Handle terminal states
                for w_idx in range(n_workers):
                    if worker_steps[w_idx] + 1 == self.max_episode_steps:
                        terminals[w_idx] = 1
                        infos[w_idx]['TimeLimit.truncated'] = True

                # Handle termination and truncation
                if terminals.sum():
                    idx_terminals = np.flatnonzero(terminals)
                    next_values = np.zeros(shape=(n_workers))
                    truncated = self._truncated_fn(infos)
                    if truncated.sum():
                        idx_truncated = np.flatnonzero(truncated)
                        with torch.no_grad():
                            next_values[idx_truncated] = value_model(next_states[idx_truncated]).cpu().numpy()

                # Update states and steps
                states = next_states
                worker_steps += 1

                # Reset environments for terminal states and update episode information
                if terminals.sum():
                    new_states = envs.reset(ranks=idx_terminals)
                    states[idx_terminals] = new_states
                    for w_idx in range(n_workers):
                        if w_idx not in idx_terminals:
                            continue
                        e_idx = self.current_ep_idxs[w_idx]
                        T = worker_steps[w_idx]
                        self.episode_steps[e_idx] = T
                        self.episode_reward[e_idx] = worker_rewards[w_idx, :T].sum()
                        self.episode_exploration[e_idx] = worker_exploratory[w_idx, :T].mean()
                        self.episode_seconds[e_idx] = time.time() - worker_seconds[w_idx]

                        # Compute returns and advantages
                        ep_rewards = np.concatenate((worker_rewards[w_idx, :T], [next_values[w_idx]]))
                        ep_discounts = self.discounts[:T+1]
                        ep_returns = np.array([np.sum(ep_discounts[:T+1-t] * ep_rewards[t:]) for t in range(T)])
                        self.returns_mem[e_idx, :T] = ep_returns

                        ep_states = self.states_mem[e_idx, :T]
                        with torch.no_grad():
                            ep_values = torch.cat((value_model(ep_states), torch.tensor([next_values[w_idx]], device=value_model.device, dtype=torch.float32)))
                        np_ep_values = ep_values.view(-1).cpu().numpy()
                        ep_tau_discounts = self.tau_discounts[:T]
                        deltas = ep_rewards[:-1] + self.gamma * np_ep_values[1:] - np_ep_values[:-1]
                        gaes = np.array([np.sum(self.tau_discounts[:T-t] * deltas[t:]) for t in range(T)])
                        self.gaes_mem[e_idx, :T] = gaes

                        # Reset worker-specific buffers
                        worker_exploratory[w_idx, :] = 0
                        worker_rewards[w_idx, :] = 0
                        worker_steps[w_idx] = 0
                        worker_seconds[w_idx] = time.time()

                        # Update episode index
                        new_ep_id = max(self.current_ep_idxs) + 1
                        if new_ep_id >= self.max_episodes:
                            buffer_full = True
                            break
                        self.current_ep_idxs[w_idx] = new_ep_id

        # Filter and concatenate episode data for training
        ep_idxs = self.episode_steps > 0
        ep_t = self.episode_steps[ep_idxs]
        self.states_mem = np.concatenate([row[:ep_t[i]] for i, row in enumerate(self.states_mem[ep_idxs])])
        self.actions_mem = np.concatenate([row[:ep_t[i]] for i, row in enumerate(self.actions_mem[ep_idxs])])
        self.returns_mem = torch.tensor(np.concatenate([row[:ep_t[i]] for i, row in enumerate(self.returns_mem[ep_idxs])]), device=value_model.device)
        self.gaes_mem = torch.tensor(np.concatenate([row[:ep_t[i]] for i, row in enumerate(self.gaes_mem[ep_idxs])]), device=value_model.device)
        self.logpas_mem = torch.tensor(np.concatenate([row[:ep_t[i]] for i, row in enumerate(self.logpas_mem[ep_idxs])]), device=value_model.device)

        # Return episode lengths, rewards, exploration rates, and durations
        ep_r = self.episode_reward[ep_idxs]
        ep_x = self.episode_exploration[ep_idxs]
        ep_s = self.episode_seconds[ep_idxs]
        return ep_t, ep_r, ep_x, ep_s
