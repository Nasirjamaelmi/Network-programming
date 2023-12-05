import sqlite3
import os


conn = sqlite3.connect('highscore.db')
conn.execute("DROP TABLE IF EXISTS persons")
conn.execute("DROP TABLE IF EXISTS scores")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY,
                name1 TEXT,
                name2 TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS scores (
                idPerson INTEGER PRIMARY KEY,
                task INTEGER,
                score INTEGER,
                FOREIGN KEY (idPerson) REFERENCES persons(id)
            )''')

with open('score2.txt', 'r', encoding="utf-8") as f:
    for line in f:
        elements = line.split()
        task = elements[1]
        firstnamn = elements[2]
        efternamn = elements[3]
        points = int(elements[4])

        # Insert data into 'persons' table
        c.execute('INSERT OR IGNORE INTO persons (name1, name2) VALUES (?, ?)', (firstnamn, efternamn))


        # Insert data into 'scores' table with the corresponding id from 'persons'
        c.execute('INSERT OR IGNORE INTO scores (task, score) VALUES (?, ?)', (task, points))

# Commit the changes
conn.commit()
# Close the connection
cursor = conn.execute(
    "SELECT p.name1 || ' ' || p.name2 AS person_name, SUM(s.score) AS TOTAL FROM scores s JOIN persons p ON s.idPerson = p.id GROUP BY person_name ORDER BY TOTAL DESC LIMIT 10")

for line in cursor:
    print("Person: {}. Total Score: {}.".format(line[0], line[1]))

cursor = conn.execute(
    "SELECT task, SUM(score) AS TOTAL FROM scores GROUP BY task ORDER BY TOTAL ASC LIMIT 10") #diffrent syntax from mysql can use aliases

for line in cursor:
    print("Task: {}. Total Score: {}.".format(line[0], line[1]))
