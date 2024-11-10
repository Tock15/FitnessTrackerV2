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
    
class Tracker:
    def __init__(self):
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

if __name__ == "__main__":
    tracker = Tracker()

    weightlifting = Weightlifting("Bench Press", 100, 10, 3)
    tracker.add_exercise(weightlifting)
    cardio = Cardio("Running", 30)
    tracker.add_exercise(cardio)
    weightlifting2 = Weightlifting("Squat", 150, 8, 4)
    tracker.add_exercise(weightlifting2)
    cardio2 = Cardio("Cycling", 45)
    tracker.add_exercise(cardio2)
    
    print(tracker)
