from mesa.agent import Agent
from .constants import State
flag = False

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

        offline_probability = 0 # to check
        for a in susceptible_neighbors:
            p_importance = a.importance
            if callable(a.importance):
                p_importance = a.importance(self.model)

            if p_importance < 0.8:
                offline_probability = 1 - p_importance
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
            p_spread = self.malware_spread_chance
            if callable(self.malware_spread_chance):
                p_spread = self.susceptible_chance(self.model)

            if self.random.random() < p_spread:
                a.state = State.INFECTED


    def try_be_susceptible(self):
        p_chance = self.susceptible_chance
        if callable(self.susceptible_chance):
            p_chance = self.susceptible_chance(self.model)

        if self.random.random() < p_chance:
            self.state = State.SUSCEPTIBLE


    def update_software(self):

        if self.state is State.OFFLINE:
            self.state = State.RESISTANT
            return

        p_chance = 0.5
        
        if self.random.random() < p_chance:
            self.state = State.RESISTANT


    def try_check_situation(self):
        p_freq = self.malware_check_frequency

        if callable(self.malware_check_frequency):
            p_freq = self.malware_check_frequency(self.model)

        if self.random.random() < p_freq:
            # Checking...
            if self.state is State.INFECTED:
                self.state = State.OFFLINE
                # self.try_to_notify_neighbors()


    def step(self):
        if self.state is State.INFECTED:
            self.try_to_infect_neighbors()
            self.try_check_situation()
       
        if self.model.antivirus:
                self.update_software()