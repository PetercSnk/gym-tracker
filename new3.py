import os
import pandas as pd
import json


# Directories and file locations
cwd = os.path.dirname(os.path.abspath(__file__))
configPath = os.path.join(cwd, 'config')
dataPath = os.path.join(cwd, 'data')
binPath = os.path.join(cwd, 'bin')
groupsFile = os.path.join(configPath, 'groups.csv')
exercisesFile = os.path.join(configPath, 'exercises.csv')
config = os.path.join(cwd, 'config.json')


# Read csv file
def readCSV(filename):
    return pd.read_csv(filename)


# Write csv file
def writeCSV(filename, df):
    df.to_csv(filename, index=False)


# Create directories
for directory in [configPath, dataPath, binPath]:
    if not os.path.exists(directory):
        os.mkdir(directory)


# Create config files
for filename in [groupsFile, exercisesFile]:
    if not os.path.isfile(filename):
        df = pd.DataFrame(columns=['name'])
        writeCSV(filename, df)


def readJSON(file):
    try:
        with open(file, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        #write conf here
        print('File not found')
        return {}


class Config():
    def __init__(self, file):
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
        exercises = [exercise for exercise in self.data['exercises'] if not (exercise == name)]
        self.data['exercises'] = exercises

    def addExerciseToGroup(self, exerciseName, groupName):
        for index in range(len(self.data['groups'])):
            if self.data['groups'][index]['name'] == groupName:
                if exerciseName in self.data['exercises']:
                    if exerciseName not in self.data['groups'][index]['exercises']:
                        self.data['groups'][index]['exercises'].append(exerciseName)


        








c = Config(config)
print(c.getGroup("g1"))
c.addGroup("g2")
#c.removeGroup("g2")
c.addExercise("z")
c.removeExercise("x")
c.addExerciseToGroup("a", "g3")
print(c.data)
