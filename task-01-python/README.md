# Task 01 - Python

## Task description
**Problem statement**

- Using MySQL database (or other relational database, for example, PostgreSQL) to create a data schema corresponding to the files in the attachment (many-to-one relationship)
- Write a script to load these two files and write data to the database.

**Necessary queries to the database**

- List of rooms and the number of students in each of them
- 5 rooms with the smallest average age of students
- 5 rooms with the largest difference in the age of students
- List of rooms where different-sex students live

**Requirements and comments**

1. Propose options for optimizing queries using indexes
2. As a result we need to generate a SQL query that adds the required indexes.
3. Unload the result in JSON or XML format
4. All the “math” should be done at the database level
5. The command interface should support the following input parameters

    5.1. students (path to students file)

    5.2. rooms (path to the rooms file)

    5.3. format (output format: xml or json)

    5.4. use OOP and SOLID

    5.5. no ORM (use SQL)

**Before you begin the task** 

- Make sure you have understood the condition correctly 
- Created and configured the virtual environment 
- Designed the architecture 

--------------------------------------------

## Setup

Requirements: Python 3.14, PostgreSQL with an existing empty database.

```
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in the database connection settings.

## Usage


1. Open a terminal and go to the `task-01-python` folder.
2. Run the script with paths to both data files:

```
python main.py --students data/students.json --rooms data/rooms.json
```

Parameters:

| Parameter | Required | Description | Example |
|---|---|---|---|
| `--students` | yes | path to the JSON file with students | `data/students.json` |
| `--rooms` | yes | path to the JSON file with rooms | `data/rooms.json` |
| `--format` | no | output format; only `json` is supported (default) | `json` |


The script creates the schema, loads the data, adds indexes, runs the four queries
and saves the results.

## Output

`output/query_results.json` – one file with four sections:

- `query_rooms_student_count` – rooms and number of students
- `query_smallest_avg_age` – 5 rooms with the smallest average age
- `query_largest_diff_age` – 5 rooms with the largest age difference
- `query_diff_sex_rooms` – rooms with students of different sex

## Decisions

- Only JSON export is implemented.
- Running the script again does not duplicate data.

--------------------------------------------

## Index optimization

Proposed indexes (sql/indexes.sql):

- `(room_id, birthday)` – for average age and age difference per room
- `(room_id, sex)` – for rooms with students of different sex

`room_id` is the first column because all queries group by room.
The second column holds the only other value each query needs,
so the database could answer from the index without reading the table.
A separate index on the foreign key `room_id` is not needed,
because `room_id` is the first column of both indexes.

### Results

Execution plans (EXPLAIN ANALYZE) before and after creating the indexes
are identical: PostgreSQL uses a sequential scan in all four queries.
The students table has 10,000 rows (76 pages, about 600 kB), so reading it
in full is cheaper than using an index. Differences in execution time
between runs came from measurement noise, not from the indexes.

In the average age and age difference queries, most of the time is spent
calculating age for every row (about 9 ms out of 10 ms), not on reading data.
An index does not reduce that cost.

The indexes are expected to be used as the table grows.
