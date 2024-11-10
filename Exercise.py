import abc
class Exercise(metaclass = abc.ABCMeta):
    def __init__(self,name):
        self.name = name
    @abc.abstractmethod
    def get_data(self):
        pass
    

class Weightlifting(Exercise):
    def __init__(self,name,weight,reps,sets):
        super().__init__(name)
        self.weight = weight
        self.reps = reps
        self.sets = sets
    def get_data(self):
        return [self.name,self.weight,self.reps,self.sets]

class Cardio(Exercise):
    def __init__(self,name,time):
        super().__init__(name)
        self.time = time
    def get_data(self):
        return [self.name,self.time]
    