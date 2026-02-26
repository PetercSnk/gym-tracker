import os
import pandas as pd


def writeCSV(filename, df):
    df.to_csv(filename, index=False)


def readCSV(filename):
    return pd.read_csv(filename)


def init():
    cwd = os.path.dirname(os.path.abspath(__file__))
    data = os.path.join(cwd, "data")
    bin = os.path.join(cwd, "bin")
    config = os.path.join(cwd, "config")
    for directory in [data, bin, config]:
        if not os.path.exists(directory):
            os.mkdir(directory)
    groups = os.path.join(config, "groups.csv")
    exercises = os.path.join(config, "exercises.csv")
    if not os.path.isfile(groups):
        df = pd.DataFrame(columns=["name"])
        writeCSV(groups, df)
    if not os.path.isfile(exercises):
        df = pd.DataFrame(columns=["name", "maxSets"])
        writeCSV(exercises, df)
    return data, bin, groups, exercises


def inputName():
    return input("Name: ")


def inputChoice():
    choice = input("Selection: ")
    try:
        return int(choice)
    except ValueError:
        return 0


def doesNameExist(df, name):
    if name in df["name"].values:
        return True
    else:
        return False


def inputManagerGroups(df):
    while True:
        print(
            """
            Group Manager
            Create  (1)
            Delete  (2)
            Rename  (3)
            Save    (4)
            """
        )
        choice = inputChoice()
        if choice in [1, 2, 3]:
            name = inputName()
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
                if doesNameExist(df, name):
                    new = input("New Name: ")
                    df.loc[df["name"] == name] = new
                else:
                    print("Does Not Exist")
            case 4:
                return df
            case _:
                print("Invalid")


def createTracker(name, maxSets, directory):
    headers = ["exercise", "date"]
    for num in range(maxSets):
        numStr = str(num + 1)
        headers.append("repsSet" + numStr)
        headers.append("weightSet" + numStr)
    df = pd.DataFrame(columns=headers)
    filename = os.path.join(directory, name + ".csv")
    writeCSV(filename, df)


def inputManagerExercises(df, data, bin):
    while True:
        print(
            """
            Exercise Manager
            Create  (1)
            Delete  (2)
            Save    (3)
            """
        )
        choice = inputChoice()
        if choice in [1, 2]:
            name = inputName()
        match choice:
            case 1:
                if not doesNameExist(df, name):
                    maxSets = int(input("Max Sets: "))
                    df.loc[len(df)] = [name, maxSets]
                    createTracker(name, maxSets, data)
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


def inputManagerMain(data, bin, groups, exercises):
    print(
        """
        Configure Groups (1)
        Configure Exercises (2)
        """
    )
    choice = inputChoice()
    match choice:
        case 1:
            df = readCSV(groups)
            df2 = inputManagerGroups(df)
            writeCSV(groups, df2)
        case 2:
            df = readCSV(exercises)
            df2 = inputManagerExercises(df, data, bin)
            writeCSV(exercises, df2)


if __name__ == "__main__":
    data, bin, groups, exercises = init()
    inputManagerMain(data, bin, groups, exercises)
