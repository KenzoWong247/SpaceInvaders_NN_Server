import math

import torch.nn as nn
import torch.nn.functional as Fn
from collections import deque, namedtuple
import random


class DDQNetwork(nn.Module):
    def __init__(self, state_tensor_size, action_set_size):
        super().__init__()

    def forward(self, x):
        x = Fn.relu(self.layer1(x))
        x = Fn.relu(self.layer2(x))
        x = Fn.relu(self.layer3(x))
        x = Fn.relu(self.layer4(x))
        return self.layer5(x)

    def __build_network(self, in_c, output_dim):
        return nn.Sequential(
            nn.Conv2d(in_channels=in_c, out_channels=32, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(3136, 512),
            nn.ReLU(),
            nn.Linear(512, output_dim)
        )

StateTransition = namedtuple('StateTransition',
                             ('state', 'action', 'next_state', 'reward'))


class ReplayMemory:
    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(StateTransition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

    def get_memory(self):
        return list(self.memory)

    def load_memory(self, memory, capacity):
        self.memory = deque(memory, maxlen=capacity)


class Hyperparameters:
    def __init__(self, learning_rate, epsilon_start, epsilon_end, epsilon_decay, target_update_rate, gamma, learning_batch_size):
        self.lr = learning_rate
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.tau = target_update_rate
        self.gamma = gamma
        self.batch_size = learning_batch_size

    def get_exploration_rate(self, steps_done):
        return self.epsilon_end + (self.epsilon_start - self.epsilon_end) * math.exp(-1 * steps_done / self.epsilon_decay)
