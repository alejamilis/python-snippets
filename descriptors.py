# Descriptor protocol
import ssl

import pandas as pd
from timeit import default_timer as timer


class lazy:
    """
    Non data descriptor to perform a lazy load of time-consuming properties.
    """
    def __init__(self, function):
        self.function = function
        self._name = function.__name__

    def __get__(self, obj, type=None) -> object:
        obj.__dict__[self._name] = self.function(obj)
        return obj.__dict__[self._name]


class NonZero:
    def __init__(self, attr_name):
        self.attr_name = attr_name
        self._name = None

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if value <= 0:
            message = self._name + " must be greater than 0"
            raise ValueError(message)
        instance.__dict__[self._name] = value


class Salary:

    amount = NonZero("amount")

    def __init__(self, amount: float):
        self.amount = amount

    @lazy
    def taxes(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        df = pd.read_csv(
            'https://www.econdb.com/api/series/OE_CSPCUBE.55304553FE.Y.CL/?format=csv',
            index_col='Date', parse_dates=['Date'])
        return df['OE_CSPCUBE.55304553FE.Y.CL'].iat[-1]


if __name__ == '__main__':
    """
    This is a non-data descriptor, when taxes attribute value is first accessed, .__get__() is automatically called and 
    executes .taxes() on the junior_salary object. The result is stored in the __dict__ attribute of junior_salary 
    itself. When taxes attribute value is accessed again, Python will use the lookup chain to find a value for 
    that attribute inside the __dict__ attribute, and that value will be returned.
    """
    junior_salary = Salary(2000)

    print(f'Junior salary: {junior_salary.amount}')
    start = timer()
    print(f'Tax percentage: {junior_salary.taxes}%')
    end = timer()
    first_timer = end - start

    start = timer()
    print(f'Again tax percentage: {junior_salary.taxes}%')
    end = timer()
    second_timer = end - start

    print(f'First tax call: {first_timer} - Second tax call: {second_timer}')

    wrong_salary = Salary(0)
