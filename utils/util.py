import json
import os


def booleans(interpreter, b, v1, v2):
    flag = False
    if b["condition"] == "eq":
        if v1 == v2:
            interpreter.log(f"True {v1} == {v2}")
            flag = True
        else:
            interpreter.log(f"False {v1} == {v2}")
    elif b["condition"] == "ne":
        if v1 != v2:
            interpreter.log(f"True {v1} != {v2}")
            flag = True
        else:
            interpreter.log(f"False {v1} != {v2}")
    elif b["condition"] == "lt":
        if v1 < v2:
            interpreter.log(f"True {v1} < {v2}")
            flag = True
        else:
            interpreter.log(f"False {v1} < {v2}")
    elif b["condition"] == "ge":
        if v1 >= v2:
            interpreter.log(f"True {v1} >= {v2}")
            flag = True
        else:
            interpreter.log(f"False {v1} >= {v2}")
    elif b["condition"] == "gt":
        if v1 > v2:
            interpreter.log(f"True {v1} > {v2}")
            flag = True
        else:
            interpreter.log(f"False {v1} > {v2}")
    elif b["condition"] == "le":
        if v1 <= v2:
            interpreter.log(f"True {v1} <= {v2}")
            flag = True
        else:
            interpreter.log(f"False {v1} <= {v2}")

    elif b["condition"] == "is":
        if v1 is v2:
            interpreter.log(f"True {v1} is {v2}")
            flag = True
        else:
            interpreter.log(f"False {v1} is {v2}")

    elif b["condition"] == "isnot":
        if not (v1 is v2):
            interpreter.log(f"True {v1} isnot {v2}")
            flag = True
        else:
            interpreter.log(f"False {v1} isnot {v2}")

    return flag


def binaries(interpreter, b, v1, v2, va1, va2):
    res = None
    resa = None
    if b["operant"] == "add":
        interpreter.log(f"Add {v2} + {v1}")
        res = v1 + v2
        resa = va2.abstr_add(va1.ps)
    elif b["operant"] == "sub":
        interpreter.log(f"Sub {v2} - {v1}")
        res = v2 - v1
        resa = va2.abstr_sub(va1.ps)
    elif b["operant"] == "mul":
        interpreter.log(f"Mul {v2} * {v1}")
        res = v2 * v1
        resa = va2.abstr_mul(va1.ps)
    elif b["operant"] == "div":
        interpreter.log(f"Div {v2} / {v1}")
        res = v2 // v1
        resa = va2.abstr_div(va1.ps)
    elif b["operant"] == "rem":
        interpreter.log(f"Rem {v2} % {v1}")
        res = v2 % v1
        resa = va2.abstr_rem(va1.ps)
    if len(resa.error) > 0:
        for error in resa.error:
            print(error)
        raise Exception("The above exceptions were thrown")
    return (res, resa)


class Variable:
    def __init__(self, value):
        if type(value).__name__ == "int":
            self.value = value
            self.type = "int"
        elif type(value).__name__ == "tuple":
            array_type, length, array = value
            self.value = array
            self.type = array_type
            self.length = length
            if self.length > len(array):
                self.value = self.value + [0] * (self.length - len(array))

    def __repr__(self) -> str:
        return str(self.value)

    def __str__(self) -> str:
        return str(self.value)


def cleanByteCode(bytecofr):
    for b in bytecofr:
        del b["offset"]
        if b["opr"] == "return":
            b["opr"] = "return1"
        elif b["opr"] == "if":
            b["opr"] = "if1"
        elif b["opr"] == "get":
            b["opr"] = "get1"
    return bytecofr


def getMethod(methods, name):
    for method in methods:
        if method["name"] == name:
            return method


def getCleanMethods(data):
    methods = []
    for method in data["methods"]:
        for annotation in method["annotations"]:
            if annotation["type"] == "dtu/compute/exec/Case":
                methods.append(
                    {
                        "name": method["name"],
                        "bytecode": cleanByteCode(method["code"]["bytecode"]),
                        "max_stack": method["code"]["max_stack"],
                        "max_locals": method["code"]["max_locals"],
                    }
                )
                break

    return methods


def getHierarchy():
    cn = dict()
    project_location = "./course-02242-examples/decompiled/dtu/compute/exec/"

    for file in os.listdir(project_location):
        with open(project_location + file) as f:
            file_name = file.split(".json")[0]
            data = json.loads(f.read())
            methods = getCleanMethods(data)
            method_dict = {}
            for method in methods:
                method_dict.update({method["name"]: method})
                cn[file_name] = method_dict
                # cn[file["name"]]["file"] = file.split(".")[0]
    return cn
