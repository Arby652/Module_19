import pytest
from app.calculator import Calculator

class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_add(self):
        assert self.calc.adding(self, 2, 3) == 5
    
    def test_sub(self):
        assert self.calc.sub(self, 7, 2) == 5
    
    def test_multiply(self):
        assert self.calc.multiply(self, 1, 5) == 5
    
    def test_devision(self):
        assert self.calc.division(self, 25, 5) == 5