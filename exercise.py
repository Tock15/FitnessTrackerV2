import abc
class Exercise(metaclass = abc.ABCMeta):
    def __init__(self,date,name):
        self.date = date
        self.name = name
    @abc.abstractmethod
    def get_data(self):
        pass
    

class Weightlifting(Exercise):
    def __init__(self,date,name,weight,sets,reps):
        super().__init__(date,name)
        self.weight = weight
        self.sets = sets
        self.reps = reps
    def get_data(self):
        return [self.date,self.weight,self.sets,self.reps]
    def get_intensity(self):
        return float(self.weight) * float(self.sets) * float(self.reps)

# class Cardio(Exercise):
#     def __init__(self,date,name,time):
#         super().__init__(date,name)
#         self.time = time
#     def get_data(self):
#         return [self.date,self.name,self.time]
#     def get_intensity(self):
#         return float(self.time)  
    
class Tracker:
    def __init__(self,name,date):
        self.name = name
        self.date = date
        self.exercises = []
        self.logDict = {}
    def add_exercise(self,exercise):
        self.exercises.append(exercise)
        self.logDict[exercise.name] = exercise.get_data()[1:]
    def __str__(self):
        result = ""
        for name, data in self.logDict.items():
            result += f"{name}: {data}\n"
        return result

