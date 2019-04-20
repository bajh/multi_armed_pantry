import random
#import matplotlib.pyplot as plt

class RestaurantDistribution():
    def __init__(self, restaurant, distribution = None):
        self.restaurant = restaurant
        # Each element in a distribution represents how confident we are in the probability
        # a given restaurant will be good.
        # For example, the float stored in element 90 represents how confident we are that
        # the restaurant has a 90% chance of being good. Each time we receive an experience report
        # about a restaurant (a report that it is "good" or "bad"), two things effectively change:
        # 1) The maximum probability, mean, and other parameters telling us whether we think the
        # restaurant is good or bad
        # 2) Measures of the spread of the distributions, such as the variance, which tell us how
        # confident we should be in this central tendency.
        # Instead of representing the distribution as a series of discrete values, we could represent
        # it as parameters to a Beta distribution, which models the continuous probability
        if distribution:
            self.distribution = distribution
        else:
            # If no prior distribution is provided, we'll construct a triangle distribution based on the
            # restaurant's rating. The rating will be the maximum likelihood, and the probability will
            # decrease linearly as we move left and right
            self.distribution = triangle_distribution(restaurant.rating / 5.0)

# TODO: revisit this
#    def plot(self):
#        plt.plot(self.distribution)

    def update(self, observation):
        # Joint probability = the probability of both a specific probability being true p(H)
        # and an observation occurring p(D|H)
        joint_probabilities = []
        for prob in range(0, len(self.distribution)):
            # Given our belief in whether this probability is credible, how likely is it that we
            # would make this observation? This is a little mind-bending, so examples are helpful... 
            # If we're very confident the restaurant is good, it's unlikely that we'll hear about a bad experience
            # If we're not super confident, then we'll be less surprised to hear about a bad experience
            # Question: how can we model how much an observation affects different types of distributions?
            likelihood_of_observation = prob / 100.0 if observation else 1 - prob / 100.0
            joint_probabilities.append(likelihood_of_observation * self.distribution[prob])
        normalizing_constant = sum(joint_probabilities)
        self.distribution = list(map(lambda p: p / normalizing_constant, joint_probabilities))

    # sample randomly chooses a probability that the restaurant is good by sampling from the range of
    # probabilities, weighted by our confidence in each probability value
    def sample(self):
        # TODO: don't crash if this returns an empty list for some reason
        return random.choices(
            population=[x/100 for x in range(0, 100)],
            weights=self.distribution,
            k=1
        )[0]

def sample(restaurant_distributions):
    weights = list(map(lambda d: d.sample(), restaurant_distributions))
    results = random.choices(
        population=restaurant_distributions,
        weights=weights,
        k=1
    )
    # todo: empty guard
    return results[0].restaurant

def triangle_distribution(median_prob):
    probs = []
    tick = 0
    while tick < median_prob and len(probs) < 100:
        tick = tick + .01
        probs.append(tick)
    while len(probs) < 100:
        tick = tick - .01
        probs.append(tick)
    total = sum(probs)
    return [prob / total for prob in probs]
