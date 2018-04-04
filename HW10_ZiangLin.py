"""read the data from each of the three files(students.txt, grade.txt, instructors.txt) and store it in a data structure """
import collections
import os
from prettytable import PrettyTable

class Repository:
    __slots__ = ['stu', 'ins', 'gra', 'major', 'studic', 'insdic']
    def __init__(self):
        self.stu = []
        self.ins = []
        self.gra = []
        self.major = []
        self.studic = collections.defaultdict(StuInf)
        self.insdic = collections.defaultdict(InsInf)

    def get_inf(self):
        pre_path = os.getcwd()
        # post_path = input("Please input the file of students' information:")
        post_path = 'students.txt'
        filename = os.path.join(pre_path, post_path)

        try:
            file = open(filename, 'r')
        except FileNotFoundError:
            print('You input a wrong file name, please try again.')
        with file:
            # cwid name major
            for line in file.readlines():
                cwid, name, major = line.split('\n')[0].split('\t')
                self.stu.append([cwid, name, major])

        # post_path = input("Please input the file of instructors' information:")
        post_path = 'instructors.txt'
        filename = os.path.join(pre_path, post_path)

        try:
            file = open(filename, 'r')
        except FileNotFoundError:
            print('You input a wrong file name, please try again.')
        with file:
            # ins_id name dept
            for line in file.readlines():
                ins_id, name, dept = line.split('\n')[0].split('\t')
                self.ins.append([ins_id, name, dept])

        # post_path = input("Please input the file of grades' information:")
        post_path = 'grades.txt'
        filename = os.path.join(pre_path, post_path)

        try:
            file = open(filename, 'r')
        except FileNotFoundError:
            print('You input a wrong file name, please try again.')
        with file:
            # cwid course grade ins_id
            for line in file.readlines():
                cwid, course, grade, ins_id = line.split('\n')[0].split('\t')
                self.gra.append([cwid, course, grade, ins_id])

        # post_path = input("Please input the file of grades' information:")
        post_path = 'majors.txt'
        filename = os.path.join(pre_path, post_path)

        try:
            file = open(filename, 'r')
        except FileNotFoundError:
            print('You input a wrong file name, please try again.')
        with file:
            for line in file.readlines():
                major, flag, course = line.split('\n')[0].split('\t')
                self.major.append([major, flag, course])

    def get_stu(self):
        for cwid, name, major in self.stu:
            stu_inf = StuInf()
            stu_inf.cwid = cwid
            stu_inf.name = name
            stu_inf.major = major
            for id, course, grade, ins_id in self.gra:
                if stu_inf.cwid == id:
                    if grade not in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']:
                        continue
                    else:
                        stu_inf.courses[course] = grade
            for major, flag, course in self.major:
                if stu_inf.major == major:
                    if flag == 'R':
                        stu_inf.required.add(course)
                    if flag == 'E':
                        stu_inf.electives.add(course)
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
        pt = PrettyTable(field_names=['CWID', 'Name', 'Completed Courses', 'Remaining Required', 'Remaining electives'])
        for stu in self.studic.values():
            pt.add_row([stu.cwid, stu.name, sorted(stu.courses.keys()), stu.req_c(), stu.ele_c()])
        print(pt)
        return pt

    def gen_ins_smy(self):
        pt = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        for ins in self.insdic.values():
            for course, stu_num in ins.course.items():
                pt.add_row([ins.ins_id, ins.name, ins.dept, course, stu_num])
        print(pt)
        return pt

    def gen_maj_smy(self):
        pt = PrettyTable(field_names=['Dept', 'Required', 'electives'])
        major = set()
        for stu in self.studic.values():
            major.add(stu.major)

        for maj in list(major):
            for stu in self.studic.values():
                if stu.major == maj:
                    pt.add_row([maj, sorted(list(stu.required)), sorted(list(stu.electives))])
                    break
        print(pt)
        return pt


class StuInf:
    __slots__ = ['cwid', 'name', 'major', 'courses', 'required', 'electives']
    def __init__(self):
        self.cwid = ''
        self.name = ''
        self.major = ''
        self.required = set()
        self.electives = set()
        self.courses = collections.defaultdict(str)

    def req_c(self):
        req_need = []
        for course in self.required:
            if course not in self.courses:
                req_need.append(course)
            elif self.courses[course] not in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']:
                req_need.append(course)
        return sorted(req_need) if req_need != [] else 'None'

    def ele_c(self):
        for course in self.electives:
            if course in self.courses and self.courses[course] in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']:
                return 'None'
        else:
            return sorted(list(self.electives))

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
    rep.gen_maj_smy()

if __name__ == '__main__':
    main()