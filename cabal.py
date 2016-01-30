#!/usr/bin/env python3
import math

class Cabal:
    """
    A quick python class implementation of the research paper 'On the Viability 
    of Conspiratorial Beliefs' by David Robert Grimes. 
    """
    def __init__(self, initial_conspirators, leak_odds=.00000409, 
            decay='gompertzian', alpha=.0001, beta=.085, avg_age=45):
        """
        In decay, only 'constant' and 'gompertzian' are accepted right now, 
        although I would like to implement future rates of decay, and possibly
        even growth to represent an expanding conspiracy.

        'leak_odds' is taken directly from the paper, though can be adjusted 
        lower or higher based on how skilled your cabal is. 

        'avg_age' can be set as needed, and is only really significant in decay
        """
        self.N_0 = initial_conspirators
        self.P = leak_odds 
        self.decay_rate = decay
        self.t = 0.0

        self.alpha = alpha
        self.beta = beta
        self.te = avg_age

        self.revealed = False


    def gompertzian(self):
        """
        Drops the population of conspirators, N(t), from N_0 at a rate
        approximately equal to the natural death rate. 
        """
        ab_rat = self.alpha / self.beta
        e2 = self.beta * (self.t + self.te)
        q = ab_rat * (1 - (math.e ** e2))

        N_t = self.N_0 * (math.e ** q)

        return N_t


    def advance_time(self, ta=1.0):
        self.t += ta


    def set_time(self, new_time):
        self.t = new_time


    def N(self):
        if self.decay_rate == 'constant':
            return self.N_0

        elif self.decay_rate == 'gompertzian':
            return self.gompertzian()


    def phi(self):
        return 1 - (1 - self.P) ** self.N()


    def L(self, t=None):
        """
        Returns the odds of your conspiracy being discovered at a given time. 

        Time must be provided as a float in years (1.237 years)

        If no time is provided, it will use the interal time that can be set. 
        Not setting time in advance will likely cause issues in decaying 
        cicumstances. 
        """
        if t is None:
            return 1 - math.e ** (-1 * self.t * self.phi())
        
        else:
            return 1 - math.e ** (-1 * t * self.phi())


    def time_to_fail(self, max_L=.95, precision=3):
        """
        Estimates the time expected until your conspiracy will be discovered, 
        in years, accurate to your set precision, and the second.
        """
        year = 1.0
        day = year/365
        hour = day/24
        second = hour/60

        advancing_list = [year, day, hour, second]
        x = 0
        f = 0.0
        advancing_by = advancing_list[x]
        while True:
            if x >= 3 and f >= max_L:
                return round(self.t, precision)
            
            elif x > 0 and f <= 0:
                # An impossible number, could raise an exception.
                return -1

            elif f >= max_L:
                x += 1
                self.t -= advancing_by * 2
                advancing_by = advancing_list[x]
                
                f = round(self.L(), precision)

            else:
                f = round(self.L(), precision)
                self.advance_time(ta=advancing_by)
            
            

if __name__ == "__main__":
    moon_landing_sustained = Cabal(411000, decay='constant')
    moon_landing_decay = Cabal(411000)
    
    global_warming_scientists = Cabal(29083, decay='constant')
    global_warming_all = Cabal(405000, decay='constant')
    
    vaccines_govs = Cabal(22000, decay='constant')
    vaccines_all = Cabal(726000, decay='constant')

    cancer = Cabal(714000, decay='constant')

    print(
            'Moon landings:\n\tsustained:', moon_landing_sustained.time_to_fail(), 
            '\n\tdecaying:', moon_landing_decay.time_to_fail(), 
            '\nClimage Change:\n\tscientists:', global_warming_scientists.time_to_fail(), 
            '\n\tincluding bodies:', global_warming_all.time_to_fail(), 
            '\nVaccines:\n\tagencies:', vaccines_govs.time_to_fail(), 
            '\n\tagencies and companies:', vaccines_all.time_to_fail(), 
            '\nCancer:', cancer.time_to_fail()
            )
