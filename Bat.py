from evauation_functions import fitness_function
class Bat:
    def __init__(self, selected_features, loudness, frequency,X,y):
        self.selected_features = selected_features
        self.best_selected_features = selected_features
        self.best_fitness = fitness_function(selected_features,X,y)
        self.loudness = loudness
        self.frequency = frequency
