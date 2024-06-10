# Source : Grokking Deep Reinforcement Learning by Miguel Morales

import numpy as np
import torch

EPS=1e-10

def optimize_model(self):
    # Get states, actions, returns, generalized advantage estimations (GAEs), and log probabilities
    states, actions, returns, gaes, logpas = self.episode_buffer.get_stacks()
    
    # Detach values from the value model
    values = self.value_model(states).detach()
    
    # Normalize GAEs
    gaes = (gaes - gaes.mean()) / (gaes.std() + EPS)
    
    # Number of samples
    n_samples = len(actions)
    
    # Policy Optimization Loop
    for i in range(self.policy_optimization_epochs):
        # Determine the batch size
        batch_size = int(self.policy_sample_ratio * n_samples)
        
        # Randomly select batch indices
        batch_idxs = np.random.choice(n_samples, batch_size, replace=False)
        
        # Create batches from the sampled indices
        states_batch = states[batch_idxs]
        actions_batch = actions[batch_idxs]
        gaes_batch = gaes[batch_idxs]
        logpas_batch = logpas[batch_idxs]
        
        # Get log probabilities and entropies from the policy model
        logpas_pred, entropies_pred = self.policy_model.get_predictions(states_batch, actions_batch)
        
        # Calculate the ratios
        ratios = (logpas_pred - logpas_batch).exp()
        
        # Calculate the unclipped policy objective
        pi_obj = gaes_batch * ratios
        
        # Calculate the clipped policy objective
        pi_obj_clipped = gaes_batch * ratios.clamp(1.0 - self.policy_clip_range, 1.0 + self.policy_clip_range)
        
        # Final policy loss using the minimum of unclipped and clipped objective
        policy_loss = -torch.min(pi_obj, pi_obj_clipped).mean()
        
        # Entropy loss for encouraging exploration
        entropy_loss = -entropies_pred.mean() * self.entropy_loss_weight
        
        # Zero out the gradients
        self.policy_optimizer.zero_grad()
        
        # Backpropagation for policy and entropy loss
        (policy_loss + entropy_loss).backward()
        
        # Gradient clipping for stability
        torch.nn.utils.clip_grad_norm_(self.policy_model.parameters(), self.policy_model_max_grad_norm)
        
        # Policy optimizer step
        self.policy_optimizer.step()
        
        # Calculate the KL divergence
        with torch.no_grad():
            logpas_pred_all, _ = self.policy_model.get_predictions(states, actions)
            kl = (logpas - logpas_pred_all).mean()
        
        # Early stopping based on KL divergence threshold
        if kl.item() > self.policy_stopping_kl:
            break
    
    # Value Optimization Loop
    for i in range(self.value_optimization_epochs):
        # Determine the batch size
        batch_size = int(self.value_sample_ratio * n_samples)
        
        # Randomly select batch indices
        batch_idxs = np.random.choice(n_samples, batch_size, replace=False)
        
        # Create batches from the sampled indices
        states_batch = states[batch_idxs]
        returns_batch = returns[batch_idxs]
        values_batch = values[batch_idxs]
        
        # Predict values for the current batch
        values_pred = self.value_model(states_batch)
        
        # Calculate the value loss
        v_loss = (values_pred - returns_batch).pow(2)
        
        # Clipped value prediction to prevent large updates
        values_pred_clipped = values_batch + (values_pred - values_batch).clamp(-self.value_clip_range, self.value_clip_range)
        
        # Clipped value loss
        v_loss_clipped = (values_pred_clipped - returns_batch).pow(2)
        
        # Final value loss using the maximum of unclipped and clipped loss
        value_loss = torch.max(v_loss, v_loss_clipped).mul(0.5).mean()
        
        # Zero out the gradients
        self.value_optimizer.zero_grad()
        
        # Backpropagation for value loss
        value_loss.backward()
        
        # Gradient clipping for stability
        torch.nn.utils.clip_grad_norm_(self.value_model.parameters(), self.value_model_max_grad_norm)
        
        # Value optimizer step
        self.value_optimizer.step()
        
        # Calculate the mean squared error
        with torch.no_grad():
            values_pred_all = self.value_model(states)
            mse = (values - values_pred_all).pow(2).mul(0.5).mean()
        
        # Early stopping based on MSE threshold
        if mse.item() > self.value_stopping_mse:
            break
