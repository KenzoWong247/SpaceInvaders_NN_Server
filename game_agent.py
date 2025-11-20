import copy
from enum import Enum
import uuid

import torch


class ActionSet(Enum):
    LEFT = 0,
    RIGHT = 1,
    SHOOT = 2

class GameState:
    def __init__(self, state_array):
        self.state = state_array

    def copy_state(self):
        return copy.copy(self.state)

    def get_tensor(self):
        return torch.tensor(self.state, dtype=torch.int16).unsqueeze(0)

class GameAgent:
    previous_state = None
    def __init__(self, trainer):
        self.client_id = uuid.uuid4()
        self.trainer = trainer

    def train_step(self, next_state):
        state = GameState(next_state)
        # TODO: Get an action from the neural network


        self.previous_state = state.copy_state()


    def get_action(self, new_state):
        # TODO: Return an action in the action space
        action = self.trainer.get_action(new_state)
        self.train_step(new_state)
        return action

    def save_experience(self):
        pass

