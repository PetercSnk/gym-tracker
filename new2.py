import csv
import os
import numpy as np
import pandas as pd


cwd = os.path.dirname(os.path.abspath(__file__))
groupsFile = os.path.join(cwd, "groups.csv")
exercisesFile = os.path.join(cwd, "exercises.csv")


# def appendCSV(filename, data):
#     with open(filename, "a+", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(data)


def writeCSV(filename, df):
    df.to_csv(filename, index=False)


def readCSV(filename):
    df = pd.read_csv(filename)
    return df


def createConfig():
    if not os.path.isfile(groupsFile):
        df = pd.DataFrame(columns=["name"])
        writeCSV(groupsFile, df)
    if not os.path.isfile(exercisesFile):
        df = pd.DataFrame(columns=["name", "maxSets"])
        writeCSV(exercisesFile, df)


def inputGroupName():
    return input("Group Name: ")


def inputChoice():
    return int(input("Selection: "))


def inputManagerGroups(df):
    df = df
    print(
        """
        Create Group (1)
        Delete Group (2)
        Rename Group (3)
        Save (4)
        """
    )
 
    while True:
        print(df)
        choice = inputChoice()
        match choice:
            case 1:
                name = inputGroupName()
                df.loc[len(df)] = [name]
            case 2:
                name = inputGroupName()
                df.drop(df.loc[df["name"] == name].index, inplace=True)
            case 3:
                pass
            case 4:
                writeCSV(groupsFile, df)
                return
            case _:
                print("Invalid")
                

def inputManager():
    print("Configure Groups (1)")
    choice = inputChoice()
    match choice:
        case 1:
            df = readCSV(groupsFile)
            inputManagerGroups(df)



if __name__ == "__main__":
    createConfig()
    inputManager()
