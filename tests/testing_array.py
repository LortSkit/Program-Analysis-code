import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.util import Variable, getCleanMethods, getMethod
import json
import unittest
from utils.interpreter import Interpreter
from utils.AbstractSignAnalysis import ArithmeticSignAnalysis

data = json.loads(
    open('./course-02242-examples/decompiled/dtu/compute/exec/Array.json').read())
methods = getCleanMethods(data)


class TestArray(unittest.TestCase):

    def test_first(self):
        intr = Interpreter(getMethod(methods, "first"), ArithmeticSignAnalysis)
        res = intr.run(([Variable(("int array", 3, [3, 2, 1]))], [], 0))
        self.assertEqual(res, 3)

    def test_access(self):
        intr = Interpreter(getMethod(methods, "access"),
                           ArithmeticSignAnalysis)
        res = intr.run(
            ([Variable(0), Variable(("int array", 3, [3, 2, 1]))], [], 0))
        self.assertEqual(res, 3)

    def test_newArray(self):
        intr = Interpreter(getMethod(methods, "newArray"),
                           ArithmeticSignAnalysis)
        res = intr.run(([], [], 0))
        self.assertEqual(res, 1)

    def test_new_array_out_of_bounds(self):
        intr = Interpreter(getMethod(methods, "newArrayOutOfBounds"),
                           ArithmeticSignAnalysis)
        try:
            res = intr.run(([], [], 0))
            self.assertFalse(True)
        except:
            self.assertTrue(True)

    def test_bubble_sort(self):
        intr = Interpreter(getMethod(methods, "bubbleSort"),
                           ArithmeticSignAnalysis)
        vals = [4, 3, 2, 1]
        res = intr.run(
            ([Variable(("int array", 4, vals))], [], 0))
        print(vals)
        print(res)
        self.assertEqual(vals, sorted(vals))

    def test_aWierdOneOutOfBounds(self):
        intr = Interpreter(getMethod(methods, "aWierdOneOutOfBounds"),
                           ArithmeticSignAnalysis)
        try:
            res = intr.run(([], [], 0))
            self.assertFalse(True)
        except:
            self.assertTrue(True)
    
    def test_aWierdOneWithinBounds(self):
        intr = Interpreter(getMethod(methods, "aWierdOneWithinBounds"),
                           ArithmeticSignAnalysis)
        res = intr.run(([], [], 0))
        self.assertEqual(res, 1)

        # elif method["name"] == "firstSafe":
        #     pass
        # elif method["name"] == "access":
        #     print(method["name"])

        #     res = intr.run(
        #         ([Variable(0), Variable(("int array", 3, [3, 2, 1]))], [], 0))
        #     print(res)
        # elif method["name"] == "newArray":
        #     print(method["name"])

        #     res = intr.run(
        #         ([], [], 0))
        #     print(res)
        # elif method["name"] == "accessSafe":
        #     pass
        # elif method["name"] == "bubbleSort":
        #     print(method["name"])
        #     res = intr.run(
        #         ([Variable(("int array", 4, [4, 3, 2, 1]))], [], 0))
        #     print(res)
        # elif method["name"] == "aWierdOneOutOfBounds":
        #     try:
        #         res = intr.run(([], [], 0))
        #     except:
        #         print("Error: Index out of bounds")
        # elif method["name"] == "aWierdOneWithinBounds":
        #     res = intr.run(([], [], 0))
        #     assert res == 1
        #     print("Succeded")


if __name__ == '__main__':
    unittest.main()