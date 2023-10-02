from utils import Variable
from interpreter import Interpreter
from AbstractSignAnalysis import ArithmeticSignAnalysis


def testingSimple():
    for method in methods:
        intr = Interpreter(method, ArithmeticSignAnalysis)
        print("Running method: " + method["name"])
        if method["name"] == "noop":
            res = (intr.run(([], [], 0)))
            assert res == None
            print("Succeded")
        elif method["name"] == "zero":
            res = (intr.run(([], [], 0)))
            assert res == 0
            print("Succeded")
        elif method["name"] == "min":
            res = intr.run(([Variable(1), Variable(2)], [], 0))
            assert res == 1
            print("Succedeed")
        elif method["name"] == "hundredAndTwo":
            res = (intr.run(([], [], 0)))
            assert res == 102
            print("Succeded")
        elif method["name"] == "identity":
            a = 2
            res = (intr.run(([Variable(a)], [], 0)))
            assert res == a
            print("Succeded")
        elif method["name"] == "add":
            a = 2
            b = 4
            res = (intr.run(([Variable(a), Variable(b)], [], 0)))
            assert res == (a+b)
            print("Succeded")
        elif method["name"] == "factorial":
            res = (intr.run(([Variable(5)], [], 0)))
            assert res == 120
            print("Succeded")


def testingArray():
    for method in methods:
        intr = Interpreter(method, ArithmeticSignAnalysis)
        if method["name"] == "first":
            print(method["name"])
            res = intr.run(([Variable(("int array", 3, [3, 2, 1]))], [], 0))
            print(res)
        elif method["name"] == "firstSafe":
            pass
        elif method["name"] == "access":
            print(method["name"])

            res = intr.run(
                ([Variable(0), Variable(("int array", 3, [3, 2, 1]))], [], 0))
            print(res)
        elif method["name"] == "newArray":
            print(method["name"])

            res = intr.run(
                ([], [], 0))
            print(res)
        elif method["name"] == "accessSafe":
            pass
        elif method["name"] == "bubbleSort":
            print(method["name"])
            res = intr.run(
                ([Variable(("int array", 4, [4, 3, 2, 1]))], [], 0))
            print(res)
        elif method["name"] == "aWierdOneOutOfBounds":
            try:
                res = intr.run(([], [], 0))
            except:
                print("Error: Index out of bounds")
        elif method["name"] == "aWierdOneWithinBounds":
            res = intr.run(([], [], 0))
            assert res == 1
            print("Succeded")
