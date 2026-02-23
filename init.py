statments = [
    """
    CREATE TABLE IF NOT EXISTS workout (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS workout_timestamp (
        id INTEGER PRIMARY KEY,
        unix INTEGER NOT NULL UNIQUE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS exercise (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        workout_id INTEGER NOT NULL,
        FOREIGN KEY(workout_id) REFERENCES workout(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS exercise_tracker (
        id INTEGER PRIMARY KEY,
        sets INTEGER NOT NULL,
        rps TEXT NOT NULL,
        wps TEXT NOT NULL,
        workout_timestamp_id INTEGER NOT NULL,
        exercise_id INTEGER NOT NULL,
        FOREIGN KEY(workout_timestamp_id) REFERENCES workout_timestamp(id),
        FOREIGN KEY(exercise_id) REFERENCES exercise(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS intTracker (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        data INTEGER NOT NULL,
        workout_timestamp_id INTEGER NOT NULL,
        FOREIGN KEY(workout_timestamp_id) REFERENCES workout_timestamp(id)
    );
    """
]
