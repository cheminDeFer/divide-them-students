import random
import pprint
import sqlite3
from student import Student 
class Group:
    def __init__(self, students=None):
        if students == None:
            self.students = []
        else:
            self.students = students
    def add_student(self, s):
        self.students.append(s)
    def __repr__(self):
        return f'Group({self.students})'
    def __str__(self):
        return f'Group: {[str(i) for i in self.students]}'

def load_students(file_path: str):
    result = []
    with open(file_path, "r") as f:
        while True:
            line = f.readline()
            if line == '':
                break
            result.append(Student(line[:-1]))
    return tuple(result)

def div_students_by_2(students):
    # calculate how many groups
    group_number, rem = divmod(len(students), 2)
    gcs = [2 for i in range(group_number)]
    if rem == 1:
        gcs[-1] += 1
    groups = populate_groups(students, gcs)
    return tuple(groups)

def populate_groups(students, gcs):
    groups = [Group() for i in range(len(gcs))] 
    for i, g in enumerate(groups):
        for j in range(gcs[i]):
            s_candidate = random.choice(students)
            students.remove(s_candidate)
            g.add_student(s_candidate)
    return groups

def adapt_groups(groups):
    a = ''
    for g in groups:
        a += adapt_students(g.students)
        a += ':'
    return a[:-1]

def adapt_students(students):
    a = ''
    for s in students:
        a += s.name
        a += ';'
    return a[:-1]

def dump_groups_db(groups, file_path: str):
    con = sqlite3.connect(file_path)
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    grouping  = res.fetchone()
    if grouping is None:
        cur.execute("CREATE TABLE grouping(groups, topic, date)")

    cur.execute("INSERT INTO grouping VALUES(?,?,?)", (adapt_groups(groups), 'writing', '30112022'))
    con.commit()
    for row in cur.execute("SELECT groups,topic, date FROM grouping ORDER BY date"):
        print(row)
    con.close()

def dump_groups_to_file(groups, file_path: str): 
    with open(file_path, "w") as f:
        for g in groups:
            f.write(str(g) + '\n')

def main():
    pprinter = pprint.PrettyPrinter()
    studs = load_students("Students.txt")
    [print(str(i)) for i in studs]
    print("#"*80)
    groups = div_students_by_2(list(studs))
    pprinter.pprint(groups)
    dump_groups_db(groups, "gs.db")
if __name__ == '__main__':
    main()
