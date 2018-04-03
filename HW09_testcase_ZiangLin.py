from HW09_ZiangLin import Repository, InsInf, StuInf
import unittest

class HW09Test(unittest.TestCase):
    """test HW09 functions"""
    def test_get_ins(self):
        """test get_ins function"""
        rep = Repository()
        rep.get_inf()
        rep.get_ins()
        ins = [i for i in rep.insdic.values() if i.ins_id == '98765'][0] #the list only has one item
        id, name, dept, course = ins.ins_id, ins.name, ins.dept, ins.course
        self.assertEqual(id, '98765')
        self.assertEqual(name, 'Einstein, A')
        self.assertEqual(dept, 'SFEN')
        self.assertEqual(course, {'SSW 567' : 4, 'SSW 540' : 3})

    def test_get_stu(self):
        """test get_stu function"""
        rep = Repository()
        rep.get_inf()
        rep.get_stu()
        stu = [i for i in rep.studic.values() if i.cwid == '10103'][0] #the list only has one item
        cwid, name, major, courses = stu.cwid, stu.name, stu.major, stu.courses
        self.assertEqual(cwid, '10103')
        self.assertEqual(name, 'Baldwin, C')
        self.assertEqual(major, 'SFEN')
        self.assertEqual(courses, {'CS 501':'B', 'SSW 564':'A-', 'SSW 567':'A', 'SSW 687':'B'})