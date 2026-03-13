import os
import pandas as pd
import json


# Directories and file locations
cwd = os.path.dirname(os.path.abspath(__file__))
dataPath = os.path.join(cwd, 'data')
binPath = os.path.join(cwd, 'bin')
config = os.path.join(cwd, 'config.json')


# Read csv file
def readCSV(filename):
    return pd.read_csv(filename)


# Write csv file
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


def createTracker(name, sets):
    headers = ["Date", "Position"]
    for num in range(sets):
        numStr = str(num + 1)
        headers.append("Reps Set " + numStr)
        headers.append("Weight Set " + numStr)
    df = pd.DataFrame(columns=headers)
    trackerFile = os.path.join(dataPath, name + ".csv")
    writeCSV(trackerFile, df)


class Config():
    def __init__(self, file):
        self.file = file
        self.data = readJSON(file)

    def getGroup(self, name):
        for group in self.data['groups']:
            if group['name'] == name:
                return group

    def createGroup(self, name):
        groupNames = [group['name'] for group in self.data['groups']]
        if name not in groupNames:
            newGroup = {
                'name': name,
                'exercises': []
            }
            self.data['groups'].append(newGroup)

    def removeGroup(self, name):
        groups = [group for group in self.data['groups'] if not (group['name'] == name)]
        self.data['groups'] = groups

    def createExercise(self, name):
        if name not in self.data['exercises']:
            self.data['exercises'].append(name)

    def removeExercise(self, name):
        for group in self.data['groups']:
            self.removeExerciseFromGroup(name, group['name'])
        exercises = [exercise for exercise in self.data['exercises'] if not (exercise == name)]
        self.data['exercises'] = exercises

    def addExerciseToGroup(self, exerciseName, groupName):
        for index in range(len(self.data['groups'])):
            if self.data['groups'][index]['name'] == groupName:
                if exerciseName in self.data['exercises']:
                    if exerciseName not in self.data['groups'][index]['exercises']:
                        self.data['groups'][index]['exercises'].append(exerciseName)
                        return

    def removeExerciseFromGroup(self, exerciseName, groupName):
        for index in range(len(self.data['groups'])):
            if self.data['groups'][index]['name'] == groupName:
                if exerciseName in self.data['exercises']:
                    exercises = [exercise for exercise in self.data['groups'][index]['exercises'] if not (exercise == exerciseName)]
                    self.data['groups'][index]['exercises'] = exercises
                    return
        
    def write(self):
        writeJSON(self.file, self.data)


if __name__ == '__main__':
    # create config and directories if they dont exist
    if not os.path.isfile(config):
        data = {
            'groups': [],
            'exercises': []
        }
        writeJSON(config, data)

    for directory in [dataPath, binPath]:
        if not os.path.exists(directory):
            os.mkdir(directory)




c = Config(config)
#c.createExercise("a")
c.addExerciseToGroup("x", "g1")
c.addExerciseToGroup('x', 'g2')
print(c.data)
c.removeExercise('a')
c.removeExerciseFromGroup('e', 'g2')
print(c.data)
c.write()
