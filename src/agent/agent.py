

class Agent:
    def __init__(self, env):
        self.env = env
        self.epoch = 0
        self.learning_rate = 0.01
        self.gamma = 0.99
        self.epsilon = 0.1
        

    def act(self, state):
        if self.epoch%10 and self.epoch!=10:
            self.learning_rate = self.learning_rate * 0.9
        self.epoch += 1
        action = 