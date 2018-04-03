"""read the data from each of the three files(students.txt, grade.txt, instructors.txt) and store it in a data structure """
import collections
import os
from prettytable import PrettyTable

class Repository:
    __slots__ = ['stu', 'ins', 'gra', 'studic', 'insdic']
    def __init__(self):
        self.stu = []
        self.ins = []
        self.gra = []
        self.studic = collections.defaultdict(StuInf)
        self.insdic = collections.defaultdict(InsInf)

    def get_inf(self):
        pre_path = os.getcwd()
        while True:
            # post_path = input("Please input the file of students' information:")
            post_path = 'students.txt'
            filename = os.path.join(pre_path, post_path)

            try:
                file = open(filename, 'r')
                break
            except FileNotFoundError:
                print('You input a wrong file name, please try again.')
        with file:
            # cwid name major
            for line in file.readlines():
                cwid, name, major = line.split('\t')
                self.stu.append([cwid, name, major.split('\n')[0]])

        while True:
            # post_path = input("Please input the file of instructors' information:")
            post_path = 'instructors.txt'
            filename = os.path.join(pre_path, post_path)

            try:
                file = open(filename, 'r')
                break
            except FileNotFoundError:
                print('You input a wrong file name, please try again.')
        with file:
            # ins_id name dept
            for line in file.readlines():
                ins_id, name, dept = line.split('\t')
                self.ins.append([ins_id, name, dept.split('\n')[0]])

        while True:
            # post_path = input("Please input the file of grades' information:")
            post_path = 'grades.txt'
            filename = os.path.join(pre_path, post_path)

            try:
                file = open(filename, 'r')
                break
            except FileNotFoundError:
                print('You input a wrong file name, please try again.')
        with file:
            # cwid course grade ins_id
            for line in file.readlines():
                cwid, course, grade, ins_id = line.split('\t')
                self.gra.append([cwid, course, grade, ins_id.split('\n')[0]])

    def get_stu(self):
        for cwid, name, major in self.stu:
            stu_inf = StuInf()
            stu_inf.cwid = cwid
            stu_inf.name = name
            stu_inf.major = major
            for id, course, grade, ins_id in self.gra:
                if stu_inf.cwid == id:
                    if grade not in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'F']:
                        stu_inf.courses[course] = 'No grades yet'
                    else:
                        stu_inf.courses[course] = grade
            self.studic[cwid] = stu_inf
        return self.studic

    def get_ins(self):
        for iid, name, dept in self.ins:
            ins_inf = InsInf()
            ins_inf.ins_id = iid
            ins_inf.name = name
            ins_inf.dept = dept
            for cwid, course, grade, ins_id in self.gra:
                if ins_inf.ins_id == ins_id:
                    ins_inf.course[course] += 1
            self.insdic[iid] = ins_inf
        return self.insdic

    def gen_stu_smy(self):
        pt = PrettyTable(field_names=['CWID', 'Name', 'Completed Courses'])
        for stu in self.studic.values():
            pt.add_row([stu.cwid, stu.name, sorted(stu.courses.keys())])
        print(pt)
        return pt

    def gen_ins_smy(self):
        pt = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        for ins in self.insdic.values():
            for course, stu_num in ins.course.items():
                pt.add_row([ins.ins_id, ins.name, ins.dept, course, stu_num])
        print(pt)
        return pt

class StuInf:
    __slots__ = ['cwid', 'name', 'major', 'courses']
    def __init__(self):
        self.cwid = ''
        self.name = ''
        self.major = ''
        self.courses = collections.defaultdict(str)

class InsInf:
    __slots__ = ['ins_id', 'name', 'dept', 'course']
    def __init__(self):
        self.ins_id = ''
        self.name = ''
        self.dept = ''
        self.course = collections.defaultdict(int)

def main():
    rep = Repository()
    rep.get_inf()
    rep.get_stu()
    rep.get_ins()
    rep.gen_stu_smy()
    rep.gen_ins_smy()

if __name__ == '__main__':
    main()