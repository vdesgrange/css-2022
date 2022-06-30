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
        self.susceptible_chance = susceptible_chance
        self.death_chance = death_chance
        self.importance_fn = importance

        self.importance = importance
        if callable(importance):
            self.importance = self.importance_fn(self)

    def try_to_notify_neighbors(self):
        """
        if importance under 0.8, nodes can shut themselves down in order to prevent being infected 
        """

        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
        susceptible_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.SUSCEPTIBLE
        ]

        offline_probability = 0 # to check
        for a in susceptible_neighbors:
            p_importance = a.importance
            if callable(a.importance_fn):
                p_importance = a.importance_fn(a)
                a.importance = p_importance

            if p_importance < 0.8:
                offline_probability = 1 - p_importance
            if self.random.random() < offline_probability:
                a.state = State.OFFLINE

    def try_to_infect_neighbors(self):
        """
        Try to infect neighbors nodes.
        """
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
        susceptible_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.SUSCEPTIBLE
        ]
        for a in susceptible_neighbors:
            p_spread = self.malware_spread_chance
            if callable(self.malware_spread_chance):
                p_spread = self.susceptible_chance(self.model)

            if self.random.random() < p_spread:
                a.state = State.INFECTED

    def try_be_susceptible(self):
        """
        Try to become susceptible
        """
        p_chance = self.susceptible_chance
        if callable(self.susceptible_chance):
            p_chance = self.susceptible_chance(self.model)

        if self.random.random() < p_chance:
            self.state = State.SUSCEPTIBLE

    def try_to_reboot(self):
        """
        Try to switch from offline to online state
        """
        p_reboot = self.importance
        if callable(self.importance):
            p_reboot = self.importance(self.model)

        if self.random.random() < p_reboot:
            self.state = State.SUSCEPTIBLE

    def try_gain_resistance(self):
        """
        Try to gain resistance to virus. (Update software ie. log4j)
        """
        p_gain = self.gain_resistance_chance
        if callable(self.gain_resistance_chance):
            p_gain = self.gain_resistance_chance(self.model)

        if self.random.random() < p_gain:
            self.state = State.RESISTANT

    def try_remove_infection(self):
        """
        Try to remove infection.
        Become susceptible (then try to become resistant) or become dead.
        """
        var = self.random.random()

        p_r = self.recovery_chance
        if callable(self.recovery_chance):
            p_r = self.recovery_chance(self.model)

        p_d = self.death_chance
        if callable(self.death_chance):
            p_d = self.death_chance(self.model)

        # Try to remove
        if var < p_r:
            # Success
            self.state = State.SUSCEPTIBLE
            self.try_gain_resistance()
        elif var > 1 - p_d:
            self.state = State.DEATH
        else:
            self.state = State.INFECTED

    def try_check_situation(self):
        """
        Try to act with regards to current agent state
        """
        p_freq = self.malware_check_frequency
        if callable(self.malware_check_frequency):
            p_freq = self.malware_check_frequency(self.model)

        if self.random.random() < p_freq:
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
