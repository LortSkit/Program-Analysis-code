from utils.util import binaries, booleans, getCleanMethods, Variable, getHierarchy
from utils.interpreter import Interpreter
from utils.AbstractSignAnalysis import ArithmeticSignAnalysis
import json
from copy import deepcopy
import os

cn = getHierarchy()

res = Interpreter(cn["Array"]["bubbleSort"], ArithmeticSignAnalysis, True)
# res.run(([Variable(1), Variable(2)], [], 0))

# try:
res = res.run(([Variable(("int array", 3, [3, 2, 1]))], [], 0))
# except Exception as e:
#     print(e)
#     print(res.error)
