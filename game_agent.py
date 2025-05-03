import uuid

class GameAgent:
    state = []
    previous_state = []
    def __init__(self):
        self.client_id = uuid.uuid4()

    def get_state(self):
        return self.state

    def train_step(self, next_state):
        self.previous_state = self.state.copy()
        self.state = next_state