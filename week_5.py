from utils.util import binaries, booleans, getCleanMethods, Variable
from utils.interpreter import Interpreter
from utils.AbstractSignAnalysis import ArithmeticSignAnalysis
import json
from copy import deepcopy
import os

cn = dict()

project_location = "./course-02242-examples/decompiled/dtu/compute/exec/"

for file in os.listdir(project_location):
    with open(project_location + file) as f:
        data = json.loads(f.read())
        methods = getCleanMethods(data)
        for method in methods:
            cn[method["name"]] = method
            cn[method["name"]]["file"] = file.split(".")[0]
