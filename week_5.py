from utils import binaries, booleans, getCleanMethods, Variable
from interpreter import Interpreter
from AbstractSignAnalysis import ArithmeticSignAnalysis
import json
from copy import deepcopy
import os


cn = dict()


# project_location = "./course-02242-examples/decompiled/dtu/compute/exec"

# for file in os.listdir(project_location):
#     with open(file) as f:
#         pass  # TODO

data = json.loads(
    open('./course-02242-examples/decompiled/dtu/compute/exec/Simple.json').read())


methods = getCleanMethods(data)
