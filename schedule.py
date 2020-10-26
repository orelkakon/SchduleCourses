import sqlite3
import os
connection = sqlite3.connect('schedule.db')


def select_current_id_time(sql, classId):
    sql.execute("""
        SELECT current_course_id, current_course_time_left FROM classrooms WHERE id = (?)
        """, [classId])
    connection.commit()
    # maybe need fix below line
    return sql.fetchall()


def select_class_location(sql, classId):
    sql.execute("""
        SELECT location FROM classrooms WHERE id = (?)
        """, [classId])
    connection.commit()
    # maybe need fix below line
    return sql.fetchone()


def select_course_name(sql, classId):
    sql.execute("""
        SELECT current_course_id, current_course_time_left FROM classrooms WHERE id = (?)
        """, [classId])
    connection.commit()
    # maybe need fix below line
    return sql.fetchall()


def delete_course(sql, courseId):
    sql.execute("""
        DELETE FROM courses WHERE id=(?)
        """, [courseId])
    connection.commit()


def update_decrease_by_one(sql, cuerrentTime, classID):
    sql.execute("""
        UPDATE classrooms SET current_course_time_left=(?) WHERE id=(?)
        """, [cuerrentTime, classID])
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


def update_current_time_and_id(sql, newCurrentId, newCuerrentTime, classId):
    sql.execute("""
        UPDATE classrooms SET current_course_id=(?), current_course_time_left=(?) WHERE id=(?)
        """, [newCurrentId, newCuerrentTime, classId])
    connection.commit()


def update_reduce_students(sql, newNumStudent, kind):
    sql.execute("""
        UPDATE students SET count=(?) WHERE grade=(?)
        """, [newNumStudent, kind])
    connection.commit()


def select_count(sql, kind):
    sql.execute("""
        SELECT count FROM students WHERE grade = (?)
        """, [kind])
    connection.commit()
    # maybe need fix below line
    return sql.fetchone()


def update_reset_class(sql, courseId):
    sql.execute("""
        UPDATE classrooms SET current_course_time_left =(?) , current_course_id=(?)  WHERE id=(?)
        """, [0, 0, courseId])
    connection.commit()


def main():
    sql = connection.cursor()
    sql.execute("SELECT * FROM courses")
    connection.commit()
    courses = sql.fetchall()
    list = []
    i = 0
    secoendRun = True
    while os.path.isfile('schedule.db') and len(courses) != 0:
        secoendRun = False
        sql.execute("SELECT * FROM courses")
        connection.commit()
        courses = sql.fetchall()
        for cs in courses:
            class_id = int(cs[4])
            cuerrentCourseID = select_current_id_time(sql, class_id)[0][0]
            cuerrentTimeLeft = select_current_id_time(sql, class_id)[0][1]
            if cuerrentTimeLeft == 0:
                # course over !
                if cuerrentCourseID != 0:
                    print("("+str(i)+") " + select_class_location(sql, class_id)[0]+": "+cs[1]+" is done")
                    delete_course(sql, cs[0])
                    update_reset_class(sql, cs[4])

                # new course need catch the class !
                else:
                    print("("+str(i)+") " + select_class_location(sql, class_id)[0]+": " + cs[1] + " is schedule to start")
                    update_current_time_and_id(sql, cs[0], cs[5], class_id)
                    update_reduce_students(sql, int(select_count(sql, cs[2])[0]) - int(cs[3]), cs[2])
            # occupied class !
            else:
                if i == 0:
                    continue
                if list.__contains__(select_class_location(sql, class_id)[0]):
                    continue
                if int(cuerrentTimeLeft) == 1:
                    print("(" + str(i) + ") " + select_class_location(sql, class_id)[0] + ": " + cs[1] + " is done")
                    delete_course(sql, cs[0])
                    update_reset_class(sql, cs[4])
                    continue
                print("("+str(i)+") " + select_class_location(sql, class_id)[0]+": occupied by "+cs[1])
                list.append(select_class_location(sql, class_id)[0])
                update_decrease_by_one(sql, int(cuerrentTimeLeft) - 1, class_id)
        if len(courses) != 0:
            print_tables(sql)
            list = []
            i = i + 1
    if secoendRun:
        print_tables(sql)


if __name__ == '__main__':
    main()
