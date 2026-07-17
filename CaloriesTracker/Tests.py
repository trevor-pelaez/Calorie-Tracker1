import unittest
from MaleUser import *
from FemaleUser import *

class TestMaleBMI(unittest.TestCase):
    def test_bmi_calculation(self):

        sedentaryMale = {'bmr': 1455, 'maintenance': 1746, 'loss': 1246, 'gain': 2046}
        user_male = MaleUser(30, 60, 160, 1.2)
        user_male.BMIcalculator()
        result = user_male.get_bmi()
        self.assertEqual(result, sedentaryMale)



class TestFemaleBMI(unittest.TestCase):
    def test_bmi_calculation(self):

        sedentaryFemale = {'bmr': 1289, 'maintenance': 1547, 'loss': 1047, 'gain': 1847}
        user_female = FemaleUser(30, 60, 160, 1.2)
        user_female.BMIcalculator()
        result = user_female.get_bmi()
        self.assertEqual(result, sedentaryFemale)

if __name__ == '__main__':
    unittest.main()