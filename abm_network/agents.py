from mesa.agent import Agent
from .constants import State

class MalwareAgent(Agent):
    def __init__(
        self,
        unique_id,
        model,
        initial_state,
        malware_spread_chance,
        malware_check_frequency,
        recovery_chance,
        gain_resistance_chance,
        importance,
        susceptible_chance,
        death_chance,
    ):
        super().__init__(unique_id, model)
        self.model = model
        self.state = initial_state
        self.malware_spread_chance = malware_spread_chance
        self.malware_check_frequency = malware_check_frequency
        self.recovery_chance = recovery_chance
        self.gain_resistance_chance = gain_resistance_chance
        self.importance = importance
        self.susceptible_chance = susceptible_chance
        self.death_chance = death_chance

    def try_to_notify_neighbors(self):

        """ if importance under 0.8, nodes can shut themselves down in order to prevent being infected """

        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
        susceptible_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.SUSCEPTIBLE
        ]

        for a in susceptible_neighbors:
            offline_probability = 0 # to check
            if a.importance < 0.8:
                offline_probability = 1 - a.importance
            if self.random.random() < offline_probability:
                a.state = State.OFFLINE

    def try_to_infect_neighbors(self):
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
        susceptible_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.SUSCEPTIBLE
        ]
        for a in susceptible_neighbors:
            if self.random.random() < self.malware_spread_chance:
                a.state = State.INFECTED


    def try_be_susceptible(self):
        if self.random.random() < self.susceptible_chance:
            self.state = State.SUSCEPTIBLE

    def try_to_reboot(self):
        if self.random.random() < self.importance:
            self.state = State.SUSCEPTIBLE

    def try_gain_resistance(self):
        if self.random.random() < self.gain_resistance_chance:
            self.state = State.RESISTANT

    def try_remove_infection(self):
        var = self.random.random()
        # Try to remove
        if var < self.recovery_chance:
            # Success
            self.state = State.SUSCEPTIBLE
            self.try_gain_resistance()
        elif var > 1 - self.death_chance:
            self.state = State.DEATH
        else:
            self.state = State.INFECTED

    def try_check_situation(self):
        if self.random.random() < self.malware_check_frequency:
            # Checking...
            if self.state is State.INFECTED:
                self.try_remove_infection()
            if self.state is State.OFFLINE:
                self.try_to_reboot()
            if self.state is State.RESISTANT:
                self.try_be_susceptible()

    def step(self):
        if self.state is State.INFECTED:
            self.try_to_infect_neighbors()
            self.try_to_notify_neighbors()
        if self.state is not State.DEATH:
            self.try_check_situation()
