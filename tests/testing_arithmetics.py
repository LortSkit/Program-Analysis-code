import unittest
import json


# def testingArithmetics():
#     for method in methods:
#         intr = Interpreter(method, ArithmeticSignAnalysis)
#         print("="*20)
#         print("Running method: " + method["name"])
#         if method["name"] == "alwaysThrows1":
#             try:
#                 res = (intr.run(([][:method["max_locals"]], [], 0)))
#                 print("Failed")
#             except:
#                 print("Succeded")

#         elif method["name"] == "alwaysThrows2":
#             try:
#                 res = (intr.run(([Variable(1)][:method["max_locals"]], [], 0)))
#                 print("Failed")
#             except:
#                 print("Succeded")
#         print("="*20)


methods = json.loads(open(
    "./course-02242-examples/decompiled/eu/bogoe/dtu/exceptional/Arithmetics.json", "r").read())
print(methods)


class ArithmeticsTestCase(unittest.TestCase):
    def test_arithmetics(self):
        pass
