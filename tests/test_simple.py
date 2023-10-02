import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.AbstractSignAnalysis import ArithmeticSignAnalysis
from utils.interpreter import Interpreter
import unittest
import json
from utils.util import Variable, getCleanMethods, getMethod

data = json.loads(
    open('./course-02242-examples/decompiled/dtu/compute/exec/Simple.json').read())
methods = getCleanMethods(data)


class TestSimple(unittest.TestCase):
    def test_noop(self):
        intr = Interpreter(getMethod(methods, "noop"), ArithmeticSignAnalysis)
        res = intr.run(([], [], 0))
        self.assertEqual(res, None)

    def test_zero(self):
        intr = Interpreter(getMethod(methods, "zero"), ArithmeticSignAnalysis)
        res = intr.run(([], [], 0))
        self.assertEqual(res, 0)

    def test_min(self):
        intr = Interpreter(getMethod(methods, "min"), ArithmeticSignAnalysis)
        res = intr.run(([Variable(1), Variable(2)], [], 0))
        self.assertEqual(res, 1)

    def test_hundredAndTwo(self):
        intr = Interpreter(
            getMethod(methods, "hundredAndTwo"), ArithmeticSignAnalysis)
        res = intr.run(([], [], 0))
        self.assertEqual(res, 102)

    def test_identity(self):
        intr = Interpreter(getMethod(methods, "identity"),
                           ArithmeticSignAnalysis)
        a = 2
        res = intr.run(([Variable(a)], [], 0))
        self.assertEqual(res, a)

    def test_add(self):
        intr = Interpreter(getMethod(methods, "add"), ArithmeticSignAnalysis)
        a = 2
        b = 4
        res = intr.run(([Variable(a), Variable(b)], [], 0))
        self.assertEqual(res, (a+b))

    def test_factorial(self):
        intr = Interpreter(getMethod(methods, "factorial"),
                           ArithmeticSignAnalysis)
        res = intr.run(([Variable(5)], [], 0))
        self.assertEqual(res, 120)


if __name__ == '__main__':
    unittest.main()
