import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.util import Variable, getCleanMethods, getMethod
import json
import unittest
from utils.interpreter import Interpreter
from utils.AbstractSignAnalysis import ArithmeticSignAnalysis


methods = json.loads(open(
    "./course-02242-examples/decompiled/eu/bogoe/dtu/exceptional/Arithmetics.json", "r").read())
print(methods)


class ArithmeticsTestCase(unittest.TestCase):
    def test_arithmetics(self):
        pass


if __name__ == '__main__':
    unittest.main()

