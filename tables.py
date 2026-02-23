class Exercise:
    def __init__(self, id, name, workout):
        self.id = id
        self.name = name
        self.workout = workout

    def __repr__(self):
        return "Exercise({0}:{1}:{2})".format(self.id, self.name, self.workout)


class WorkoutTimestamp:
    def __init__(self, id, unix):
        self.id = id
        self.unix = unix

    def __repr__(self):
        return "WorkoutTimestamp({0}:{1})".format(self.id, self.unix)


class Workout:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "Workout({0}:{1})".format(self.id, self.name)


class ExerciseTracker:
    def __init__(self, id, sets, rps, wps, unix, exercise):
        self.id = id
        self.sets = sets
        self.rps = rps
        self.wps = wps
        self.unix = unix
        self.exercise = exercise

    def __repr__(self):
        return "ExerciseTracker({0}:{1}:{2}:{3}:{4}:{5})".format(
            self.id, self.sets, self.rps, self.wps, self.unix,
            self.exercise)


class IntTracker:
    def __init__(self, id, name, data, unix):
        self.id = id
        self.name = name
        self.data = data
        self.unix = unix

    def __repr__(self):
        return "IntTracker({0}:{1}:{2}:{3})".format(
            self.id, self.name, self.data, self.unix)
