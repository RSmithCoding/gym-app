# Gym App

A command-line workout tracker. Build a library of exercises, group them into gym sessions, then log the reps and weight for each set as you train. Everything is stored in an SQLite database, ready for tracking progress over time.

## Why I built it

I wanted to build on what I learned in my first SQLite project ([Debt Relief](https://github.com/RSmithCoding/debt-relief)) with something bigger, using a properly designed database with several linked tables. I go to the gym myself, so I understood what the app needed to do from the start.

## Features

- **Exercise library:** view, add, modify and delete exercises, each with a primary and secondary body area
- **Session builder:** pick exercises for a session, filter the list by body area, toggle exercises in and out, and save it with a name
- **View sessions:** see which exercises are in each saved session, delete a session, or start training from it
- **Training log:** work through a session exercise by exercise, entering reps and weight for up to five sets each, with the date saved automatically
- Creates the database automatically the first time you run it, with a starter exercise

## Database design

The data is split across five linked tables:

| Table | Stores |
|---|---|
| `Exercises` | Each exercise and the body areas it works |
| `Sessions` | Named workout sessions |
| `SessionExercises` | Which exercises belong to which session (a many-to-many link table) |
| `WorkoutHistory` | Each time a session is trained, with the date |
| `TrainingLog` | The sets, reps and weight logged for each exercise in a workout |

Foreign keys link the tables together, so deleting a session or exercise also removes the records that depend on it.

## Built with

- Python 3
- SQLite (`sqlite3`, part of Python's standard library)

## Running it

You need Python 3. No extra packages are required.

```
python3 gymapp.py
```

On first run it creates `gymapp.db` in the same folder. Choose options from the main menu by number.

## Project status

In progress. The exercise library, session builder and training log are working. Next I'm adding:

- Viewing a previous workout by date
- A progress report for each exercise
- A chart showing overall progress

An iPhone version of the app is also in development, in a separate repository.

## What I learned

- Designing a relational database with several linked tables
- Using foreign keys with `ON DELETE CASCADE` and `ON DELETE SET NULL`
- Joining tables with `JOIN` and `LEFT JOIN` to pull related data together
- Inserting many rows at once with `executemany`
- Handling database errors with `try`/`except`/`finally` and rolling back changes