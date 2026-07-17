from User import *
from flask  import Flask, Response, flash, g, redirect, render_template, request, session, url_for


# Use inheritance to create a subclass of User for female users
class FemaleUser(User):
    def __init__(self, age, weight, height, activity):
        super().__init__(age, weight, height, activity)
        self.__BMI = [0, 0, 0, 0]

    def get_bmi(self):
        return self.__BMI

    def set_bmi(self, BMI):
        self.__BMI = BMI
        

    def BMIcalculator(self):
        """Estimate calorie targets using a simple BMR/TDEE calculator. This is a rough estimate."""
        result = None

        try:
         # Basic Mifflin-St Jeor BMR estimate.
            bmr = 10 * self._User__weight + 6.25 * self._User__height - 5 * self._User__age - 161

            maintenance = round(bmr * self._User__activity)
            result = {
                "bmr": round(bmr),
                "maintenance": maintenance,
                "loss": maintenance - 500,
                "gain": maintenance + 300,
                }

            self.set_bmi(result)
        except ValueError:
            flash("Enter valid calculator numbers.", "error")

        return result


