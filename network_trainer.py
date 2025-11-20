from collections import deque
from enum import Enum

import torch

from neural_network import DDQNetwork, StateTransition, ReplayMemory, Hyperparameters
from torch import nn, optim, device, cuda, tensor, argmax
from torch.utils.tensorboard import SummaryWriter

import os.path
import random
import math

RUN_DATA_DIRECTORY = 'runs'
MODEL_SAVE_PATH = 'training'

class Trainer:
    state_size = 0
    steps_done = 0
    score_average = 0
    reward_average = 0
    games_completed = 0


    def __init__(self, training_iteration, action_set_size, memory_capacity, hyperparameters: Hyperparameters):
        self.device = device(
            "cuda" if cuda.is_available() else
            "cpu"
        )
        print(f'Using device {self.device} for training')

        self.memory = ReplayMemory(memory_capacity)
        self.actions_size = action_set_size
        self.hyperparameters = hyperparameters
        self.write = SummaryWriter(log_dir=os.path.join(RUN_DATA_DIRECTORY, f'Network_Data_{training_iteration}'))
        self.network_online = DDQNetwork()
        self.network_target = DDQNetwork()
        self.network_online.to(device=self.device)
        self.network_target.to(device=self.device)

    def select_action(self, state):
        if random.random() < self.hyperparameters.get_exploration_rate(self.steps_done):
            # Random Action
            action_index = random.randint(0, self.actions_size - 1)

        else:
            # Get Action from network
            state = tensor(state, device=self.device).unsqueeze(0)
            action_values = self.network_online(state)
            action_index = argmax(action_values, dim=1).item()

        self.steps_done += 1
        return action_index

    def save_memory(self, last_state, current_state, action, reward):
        self.memory.push(last_state, action, current_state, reward)

    def network_init(self, state_size):
        self.state_size = state_size

    def save_training(self):
        pass

    def load_training(self):
        pass

    def make_histogram(self):
        pass