import os
import pandas as pd
import json
import logging

logger = logging.getLogger(__name__)


def readCSV(filename):
    return pd.read_csv(filename)


def writeCSV(filename, df):
    df.to_csv(filename, index=False)


def readJSON(file):
    try:
        with open(file, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print('File not found')


def writeJSON(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)


class Config:
    def __init__(self):
        cwd = os.path.dirname(os.path.abspath(__file__))
        self.trackers = os.path.join(cwd, 'trackers')
        self.bin = os.path.join(cwd, 'bin')
        self.file = os.path.join(cwd, 'config.json')

        if not os.path.isfile(self.file):
            template = {
                'groups': [],
                'exercises': []
            }
            writeJSON(self.file, template)

        data = readJSON(self.file)
        self.groups = data['groups']
        self.exercises = data['exercises']

        for directory in [self.trackers, self.bin]:
            if not os.path.exists(directory):
                os.mkdir(directory)

    def exercisesToStr(self):
        exercisesStr = '===========Excercises=========='
        for i, exercise in enumerate(self.exercises):
            exercisesStr += '\n({}) {} '.format(i, exercise)
        exercisesStr += '\n==============================='
        return exercisesStr

    def groupsToStr(self):
        groupsStr = ''
        for i, group in enumerate(self.groups):
            groupsStr += '({}) {} '.format(i, group['name'])
        return groupsStr

    def createGroup(self, name):
        if not self.doesGroupExist(name):
            newGroup = {
                'name': name,
                'exercises': []
            }
            self.groups.append(newGroup)
        else:
            logger.error('group already exists')

    def popGroup(self, index):
        if self.validIndex(index, self.groups):
            self.groups.pop(index)
        else:
            logger.error('group does not exist')

    def validIndex(self, index, arr):
        if 0 <= index < len(arr):
            return True
        else:
            return False

    def popExercise(self, eIndex):
        if not self.validIndex(eIndex, self.exercises):
            logger.error('exercise does not exist')
            return
        n = 0
        while os.path.isfile(os.path.join(self.bin, self.exercises[eIndex] + str(n) + '.csv')):
            n += 1
        os.rename(os.path.join(self.trackers, self.exercises[eIndex] + '.csv'),
                  os.path.join(self.bin, self.exercises[eIndex] + str(n) + '.csv'))
        for gIndex in range(len(self.groups)):
            self.popFromGroup(eIndex, gIndex)
        self.exercises.pop(eIndex)

    def addToGroup(self, eIndex, gIndex):
        if not self.validIndex(eIndex, self.exercises):
            logger.error('invalid exercise')
            return
        if not self.validIndex(gIndex, self.groups):
            logger.error('invalid group')
            return
        if self.exercises[eIndex] not in self.groups[gIndex]['exercises']:
            self.groups[gIndex]['exercises'].append(self.exercises[eIndex])

    def popFromGroup(self, eIndex, gIndex):
        if not self.validIndex(eIndex, self.exercises):
            logger.error('invalid exercise')
            return
        if not self.validIndex(gIndex, self.groups):
            logger.error('invalid group')
            return
        if self.exercises[eIndex] in self.groups[gIndex]['exercises']:
            exercises = [
                exercise
                for exercise in self.groups[gIndex]['exercises']
                if not (exercise == self.exercises[eIndex])
            ]
            self.groups[gIndex]['exercises'] = exercises

    def createExercise(self, name, sets):
        if name in self.exercises:
            logger.error('exercise already exists')
            return
        if sets < 1:
            logger.error('sets must be greater than 0')
            return
        self.exercises.append(name)
        headers = ["date", "position"]
        for num in range(sets):
            numStr = str(num + 1)
            headers.append("reps" + numStr)
            headers.append("weight" + numStr)
        df = pd.DataFrame(columns=headers)
        tracker = os.path.join(self.trackers, name + ".csv")
        writeCSV(tracker, df)

    def write(self):
        data = {
            'groups': self.groups,
            'exercises': self.exercises
        }
        writeJSON(self.file, data)

    def doesGroupExist(self, name):
        groupNames = [group['name'] for group in self.groups]
        if name in groupNames:
            return True
        else:
            return False


def toInt(i):
    try:
        return int(i)
    except ValueError:
        return -1


def mainMenu(config):
    while True:
        print(
            """
            ===============================
            Create Group                (0)
            Delete Group                (1)
            Create Exercise             (2)
            Delete Exercise             (3)
            Add Exercise to Group       (4)
            Remove Exercise from Group  (5)
            Save & Exit                 (6)
            ===============================
            """
        )
        choice = toInt(input('choice: '))
        match choice:
            case 0:
                name = input('name: ')
                config.createGroup(name)
            case 1:
                gIndex = toInt(input(config.groupsToStr()))
                config.popGroup(gIndex)
            case 2:
                name = input('name: ')
                sets = toInt(input('sets: '))
                config.createExercise(name, sets)
            case 3:
                eIndex = toInt(input(config.exercisesToStr()))
                config.popExercise(eIndex)
            case 4:
                eIndex = toInt(input(config.exercisesToStr()))
                gIndex = toInt(input(config.groupsToStr()))
                config.addToGroup(eIndex, gIndex)
            case 5:
                eIndex = toInt(input(config.exercisesToStr()))
                gIndex = toInt(input(config.groupsToStr()))
                config.popFromGroup(eIndex, gIndex)
            case 6:
                return
            case _:
                print('invalid')
        config.write()



if __name__ == '__main__':
    c = Config()
    mainMenu(c)
    #c.createExercise("a")
    # c.addExerciseToGroup("x", "g1")
    # c.addExerciseToGroup('x', 'g2')
    # print(c.data)
    # c.removeExercise('a')
    # c.removeExerciseFromGroup('e', 'g2')
    # print(c.data)
    # c.write()
