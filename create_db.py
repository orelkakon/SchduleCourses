import sqlite3
import os
import sys
import atexit
configFile = sys.argv[1]
if configFile.find(".txt") == -1:
    configFile = configFile + ".txt"
databaseExist = os.path.isfile(configFile)
connection = sqlite3.connect('schedule.db')


def create_tables(sql):
    sql.execute("""CREATE TABLE classrooms (
                id              INT              NOT NULL,
                location        TEXT             NOT NULL,
                current_course_id INTEGER        NOT NULL,
                current_course_time_left INTEGER NOT NULL
                );""")

    sql.execute("""CREATE TABLE courses (
                id      INTEGER         PRIMARY KEY,
                course_name    TEXT        NOT NULL,
                student        TEXT        NOT NULL,
                number_of_students INTEGER NOT NULL,
                class_id INTEGER REFERENCES classrooms(id),
                course_length INTEGER NOT NULL
                );""")

    sql.execute("""CREATE TABLE students (
                grade          TEXT      PRIMARY KEY,
                count    INTEGER            NOT NULL
                );
                """)
    connection.commit()


def insert_course(sql, courseId, courseName, student, numStudents, classId, courseLength):
    sql.execute("""
        INSERT INTO courses (id, course_name,student,number_of_students,class_id,course_length) VALUES (?, ?, ?, ?, ?, ?)
    """, [courseId, courseName, student, numStudents, classId, courseLength])
    connection.commit()


def insert_students(sql, grade, count):
    sql.execute("""INSERT INTO students (grade, count) VALUES (?, ?)""", [grade, count])
    connection.commit()


def insert_classroom(sql, id, location, current_course_id, current_course_time_left):
    sql.execute("""INSERT INTO classrooms (id, location, current_course_id, current_course_time_left) 
    VALUES (?, ?, ?, ?)""", [id, location.strip("\n"), current_course_id, current_course_time_left])
    connection.commit()


def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)


def print_tables(sql):
    sql.execute("""SELECT * FROM courses""")
    connection.commit()
    course = sql.fetchall()
    print("courses")
    print_table(course)
    sql.execute("""SELECT * FROM classrooms""")
    connection.commit()
    classRoom = sql.fetchall()
    print("classrooms")
    print_table(classRoom)
    sql.execute("""SELECT * FROM students""")
    connection.commit()
    student = sql.fetchall()
    print("students")
    print_table(student)


def _close_db():
    connection.commit()
    connection.close()


atexit.register(_close_db)


def main():
    with connection:
        sql = connection.cursor()
        try:
            create_tables(sql)
        except :
            return
        with open(configFile, "r") as file:
            for line in file:
                if line[0] == 'C':
                    kind, courseID, courseName, student, num, classID, size = line.split(",")
                    insert_course(sql, courseID, courseName.strip(), student.strip(), num, classID, size)
                elif line[0] == 'R':
                    kind, classID, location = line.split(",")
                    insert_classroom(sql, classID, location.strip(), 0, 0)
                # must be S
                else:
                    kind, grade, count = line.split(",")
                    insert_students(sql, grade.strip(), count)
        print_tables(sql)


if __name__ == '__main__' and databaseExist:
    main()

