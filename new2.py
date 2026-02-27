import os
import pandas as pd
from datetime import datetime


# Directories and file locations
cwd = os.path.dirname(os.path.abspath(__file__))
configPath = os.path.join(cwd, "config")
dataPath = os.path.join(cwd, "data")
binPath = os.path.join(cwd, "bin")
groupsFile = os.path.join(configPath, "groups.csv")
exercisesFile = os.path.join(configPath, "exercises.csv")


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
        df = pd.DataFrame(columns=["name"])
        writeCSV(filename, df)


# Get menu choice, handle value errors
def inputChoice():
    choice = input("Selection: ")
    try:
        return int(choice)
    except ValueError:
        return 0


# Check if name exists in dataframe
def doesNameExist(df, name):
    if name in df["name"].values:
        return True
    else:
        return False


# Main menu
def mainMenu():
    while True:
        print(
            """
            Configure Manager
            Groups      (1)
            Exercises   (2)
            Exit        (3)
            """
        )
        choice = inputChoice()
        match choice:
            case 1:
                df = readCSV(groupsFile)
                df2 = editGroups(df)
                writeCSV(groupsFile, df2)
            case 2:
                df = readCSV(exercisesFile)
                df2 = editExercises(df)
                writeCSV(exercisesFile, df2)
            case 3:
                return


# Menu for creating, deleting, and saving groups
def editGroups(df):
    while True:
        print(
            """
            Group Manager
            Create  (1)
            Delete  (2)
            Save    (3)
            """
        )
        choice = inputChoice()
        if choice in [1, 2]:
            name = input("Group Name: ")
        match choice:
            case 1:
                if not doesNameExist(df, name):
                    df.loc[len(df)] = name
                else:
                    print("Already Exists")
            case 2:
                if doesNameExist(df, name):
                    df.drop(df.loc[df["name"] == name].index, inplace=True)
                else:
                    print("Does Not Exist")
            case 3:
                return df
            case _:
                print("Invalid")


# Menu for creating, deleting, and saving exercises
def editExercises(df):
    while True:
        print(
            """
            Exercise Manager
            Create  (1)
            Delete  (2)
            Log     (3)
            Save    (4)
            """
        )
        choice = inputChoice()
        if choice in [1, 2, 3]:
            name = input("Exercise Name: ")
        match choice:
            case 1:
                if not doesNameExist(df, name):
                    while True:
                        try:
                            maxSets = int(input("Max Sets: "))
                            createTracker(name, maxSets)
                            df.loc[len(df)] = name
                            break
                        except ValueError:
                            print("Invalid")
                else:
                    print("Already Exists")
            case 2:
                # ERROR WHEN FILE ALREADY IN BIN
                if doesNameExist(df, name):
                    os.rename(os.path.join(dataPath, name + ".csv"),
                              os.path.join(binPath, name + ".csv"))
                    df.drop(df.loc[df["name"] == name].index, inplace=True)
                else:
                    print("Does Not Exist")
            case 3:
                if doesNameExist(df, name):
                    logExercise(name)
                else:
                    print("Does Not Exist")
            case 4:
                return df
            case _:
                print("Invalid")


# Creates a tracker file for the given exercise
def createTracker(name, maxSets):
    headers = ["Date"]
    for num in range(maxSets):
        numStr = str(num + 1)
        headers.append("Reps Set " + numStr)
        headers.append("Weight Set " + numStr)
    df = pd.DataFrame(columns=headers)
    trackerFile = os.path.join(dataPath, name + ".csv")
    writeCSV(trackerFile, df)


# Appends data to tracker file
def logExercise(name):
    trackerFile = os.path.join(dataPath, name + ".csv")
    df = readCSV(trackerFile)
    data = [datetime.now().date()]
    for header in df.columns.values[1:]:
        data.append(input(header + ": "))
    df.loc[len(df)] = data
    writeCSV(trackerFile, df)


if __name__ == "__main__":
    mainMenu()
