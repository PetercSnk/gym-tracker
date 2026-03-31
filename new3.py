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

        self.data = readJSON(self.file)

        for directory in [self.trackers, self.bin]:
            if not os.path.exists(directory):
                os.mkdir(directory)

    def exercisesToStr(self):
        exercisesStr = ''
        for i, exercise in enumerate(self.data['exercises']):
            exercisesStr += '({}) {} '.format((i + 1), exercise)
        return exercisesStr

    def createGroup(self, name):
        if not self.doesGroupExist(name):
            newGroup = {
                'name': name,
                'exercises': []
            }
            self.data['groups'].append(newGroup)
        else:
            logger.error('group already exists')

    def removeGroup(self, name):
        if self.doesGroupExist(name):
            groups = [
                group
                for group in self.data['groups']
                if not (group['name'] == name)
            ]
            self.data['groups'] = groups
        else:
            logger.error('group does not exist')

    def createExercise(self, name, sets):
        if not self.doesExerciseExist(name):
            self.data['exercises'].append(name)
            headers = ["date", "position"]
            for num in range(sets):
                numStr = str(num + 1)
                headers.append("reps" + numStr)
                headers.append("weight" + numStr)
            df = pd.DataFrame(columns=headers)
            tracker = os.path.join(self.trackers, name + ".csv")
            writeCSV(tracker, df)
        else:
            logger.error('exercise already exists')

    def removeExercise(self, name):
        if self.doesExerciseExist(name):
            for group in self.data['groups']:
                self.removeExerciseFromGroup(name, group['name'])
            exercises = [
                exercise
                for exercise in self.data['exercises']
                if not (exercise == name)
            ]
            self.data['exercises'] = exercises
            n = 0
            while os.path.isfile(os.path.join(self.bin, name + str(n) + '.csv')):
                n += 1
            os.rename(os.path.join(self.trackers, name + '.csv'),
                      os.path.join(self.bin, name + str(n) + '.csv'))
        else:
            logger.error('exercise does not exist')

    def addExerciseToGroup(self, exerciseName, groupName):
        if exerciseName in self.data['exercises']:
            for index in range(len(self.data['groups'])):
                if self.data['groups'][index]['name'] == groupName:
                    if exerciseName not in self.data['groups'][index]['exercises']:
                        self.data['groups'][index]['exercises'].append(exerciseName)
                        return
        else:
            logger.error('exercise does not exist')

    def removeExerciseFromGroup(self, exerciseName, groupName):
        for index in range(len(self.data['groups'])):
            if self.data['groups'][index]['name'] == groupName:
                if exerciseName in self.data['exercises']:
                    exercises = [exercise for exercise in self.data['groups'][index]['exercises'] if not (exercise == exerciseName)]
                    self.data['groups'][index]['exercises'] = exercises
                    return

    def write(self):
        writeJSON(self.file, self.data)

    def doesGroupExist(self, name):
        groupNames = [group['name'] for group in self.data['groups']]
        if name in groupNames:
            return True
        else:
            return False

    def doesExerciseExist(self, name):
        if name in self.data['exercises']:
            return True
        else:
            return False


def getValidInt(prompt):
    i = input(prompt)
    try:
        return int(i)
    except ValueError:
        return 0
    

# def doesGroupExist(name, groups):
#     groupNames = [group['name'] for group in groups]
#     if name in groupNames:
#         return True
#     else:
#         return False


def mainMenu(config):
    while True:
        print(
            """
            ===============================
            Create Group                (1)
            Delete Group                (2)
            Create Exercise             (3)
            Delete Exercise             (4)
            Add Exercise to Group       (5)
            Remove Exercise from Group  (6)
            ===============================
            """
        )
        choice = getValidInt('choice: ')
        if choice in [1, 2, 3, 4]:
            name = input('name: ')
        match choice:
            case 1:
                if not doesGroupExist(name, config.data['groups']):
                    config.createGroup(name)
                else:
                    print('already exists')
            case 2:
                if doesGroupExist(name, config.data['groups']):
                    config.removeGroup(name)
                else:
                    print('does not exist')
            case 3:
                if name not in config.data['exercises']:
                    sets = getValidInt('sets: ')
                    if sets:
                        config.createExercise(name, sets)
                    else:
                        print('invalid number of sets')
                else:
                    print('already exists')
            case 4:
                if name in config.data['exercises']:
                    config.removeExercise(name)
                else:
                    print('does not exist')
            case 5:
                print('available exercises: ', config.exercisesToStr())
                choice = getValidInt('choice: ')
                total = len(config.data['exercises'])
                if choice > 0 and choice <= total:
                    exercise = config.data['exercises'][(choice - 1)]
                    
                else:
                    print('invalid choice')

                    

            case _:
                print('invalid')

        config.write()



if __name__ == '__main__':
    config = Config()
    mainMenu(config)




    #c.createExercise("a")
    # c.addExerciseToGroup("x", "g1")
    # c.addExerciseToGroup('x', 'g2')
    # print(c.data)
    # c.removeExercise('a')
    # c.removeExerciseFromGroup('e', 'g2')
    # print(c.data)
    # c.write()
