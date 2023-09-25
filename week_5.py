import json

data = json.loads(
    open('./course-02242-examples/decompiled/dtu/compute/exec/Simple.json').read())


class Pu(ZeroDivisionError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


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


def getCleanMethods(data):
    methods = []
    for method in data["methods"]:
        for annotation in method["annotations"]:
            if annotation["type"] == "dtu/compute/exec/Case":
                methods.append(
                    {"name": method["name"], "bytecode": cleanByteCode(method["code"]["bytecode"]),
                     "max_stack": method["code"]["max_stack"], "max_locals": method["code"]["max_locals"]})
                break

    return methods


methods = getCleanMethods(data)

def booleans(interpreter,b,v1,v2):
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

def binaries(interpreter,b,v1,v2):
    res = None
    if b["operant"] == "add":
        interpreter.log(f"Add {v1} + {v2}")
        res = v1+v2
    elif b["operant"] == "sub":
        interpreter.log(f"Sub {v1} - {v2}")
        res = v1-v2
    elif b["operant"] == "mul":
        interpreter.log(f"Mul {v1} * {v2}")
        res = v1*v2
    elif v2 != 0:
        if b["operant"] == "div":
            interpreter.log(f"Div {v1} / {v2}")
            res = v1/v2
        elif b["operant"] == "rem":
            interpreter.log(f"Rem {v1} % {v2}")
            res = v1%v2
    return res

class SignAnalysis:
    def __init__(self ):
        self.ps = set([])
        self.error = set([])
    

    def add(self, signs):
        init_signs = self.ps
        for sign1 in init_signs:
            for sign2 in signs:
                if (sign1 == "+" and sign2 == "+") or (sign1 == "+" and sign2 == "0"):
                    self.ps = set().union(self.ps, {"+"})
                elif (sign1 == "-" and sign2 == "+") or (sign1 == "+" and sign2 == "-"):
                    self.ps = set().union(self.ps, {"+", "-", "0"})
                elif (sign1 == "0" and sign2 == "-") or (sign1 == "-" and sign2 == "0") or (sign1 == "-" and sign2 == "-"):
                    self.ps = set().union(self.ps, {"-"})
                elif (sign1 == "0" and sign2 == "0"):
                    self.ps = set().union(self.ps, {"0"})
           
#               +   | -        | 0 
#        + |{+}     | {+,-,0}  | {+}
#        - |{-,0,+} | {-}      | {-}
#        0 |{+}     | {-}      | {0}

    def sub(self, signs):
        init_signs = self.ps
        for sign1 in init_signs:
            for sign2 in signs:
                if (sign1 == "+" and sign2 == "+") or (sign1 == "-" and sign2 == "-"):
                    self.ps = set().union(self.ps, {"+","-","0"})
                elif (sign1 == "-" and sign2 == "+") or (sign1 == "0" and sign2 == "+") or (sign1 == "-" and sign2 == "0"):
                    self.ps = set().union(self.ps, {"-"})
                elif (sign1 == "+" and sign2 == "-") or (sign1 == "+" and sign2 == "0") or (sign1 == "0" and sign2 == "-"):
                    self.ps = set().union(self.ps, {"+"})
                elif (sign1 == "0" and sign2 == "0"):
                    self.ps = set().union(self.ps, {"0"})
                
#               +   | -        | 0   
#        + |{+,-,0} | {+}      | {+}
#        - |{-}     | {-,+,0}  | {-}
#        0 |{-}     | {+}      | {0}

    def mul(self, signs):
        init_signs = self.ps
        for sign1 in init_signs:
            for sign2 in signs:
                if (sign1 == "+" and sign2 == "+") or (sign1 == "-" and sign2 == "-"):
                    self.ps = set().union(self.ps, {"+"})
                elif sign1 == "0" or sign2 == "0":
                    self.ps = set().union(self.ps, {"0"})
                elif (sign1 == "-" and sign2 == "+") or (sign1 == "+" and sign2 == "-"):
                    self.ps = set().union(self.ps, {"-"})
        
#               +   | -        | 0 
#        + |{+}     | {-}      | {0}
#        - |{-}     | {+}      | {0}
#        0 |{0}     | {0}      | {0}

    def div(self, signs):
        init_signs = self.ps
        for sign1 in init_signs:
            for sign2 in signs:
                if (sign1 == "+" and sign2 == "+") or (sign1 == "-" and sign2 == "-"):
                    self.ps = set().union(self.ps, {"+", "0"})
                elif (sign1 == "-" and sign2 == "+") or (sign1 == "+" and sign2 == "-"):
                    self.ps = set().union(self.ps, {"-","0"})
                elif sign1 == "0":
                    self.ps = set().union(self.ps, {"0"})
                elif sign2 == "0":
                    self.error = set().union(self.error, "DivisionZeroException")
        
#               +       | -           | 0 
#        + |{+,0}       | {-,0}       | {ø}
#        - |{-,0}       | {+,0}       | {ø}
#        0 |{0}         | {0}         | {ø}
    
class Interpreter:
    def __init__(self, p, verbose):
        self.program = p
        self.verbose = verbose
        # self.memory = {}
        self.stack = []
        self.Error = {}

    def log(self, mes):
        print(mes)

    def run(self, f):
        self.stack.append(f)
        while True:
            flag, ret = self.step()
            if not flag:
                return ret

    def step(self):
        (l, s, pc) = self.stack[-1]
        b = self.program["bytecode"][pc]
        if hasattr(self, b["opr"]):
            return getattr(self, b["opr"])(b)
        else:
            print(f"IMPLEMENT {b['opr']} YOU FUCKING IDIOT")
            return False, None
        
    def abstract_step(self):
        (l, s, pc) = self.stack[-1]
        b = self.program["bytecode"][pc]
        if hasattr(self, b["opr"]):
            return getattr(self, b["opr"])(b)
        else:
            print(f"IMPLEMENT {b['opr']} YOU FUCKING ABSTRACT CUNT!")
            return False, None

    def pop(self, b):
        (l, s, pc) = self.stack.pop(-1)
        # Rule (pop_1)
        if b["words"] == 1:
            if len(s) < 1:
                return False, None
            self.stack.append((l, s[:-1], pc + 1))
        # Rule (pop_2)
        elif b["words"] == 2:
            if len(s) < 2:
                return False, None
            self.stack.append((l, s[:-2], pc + 1))
        else:
            return False, None

    def nop(self, b):
        (l, s, pc) = self.stack.pop(-1)
        pc += 1
        self.stack.append((l, s, pc))
        return True, b

    def load(self, b):
        (l, s, pc) = self.stack.pop(-1)
        v = l[b["index"]]
        self.log(f"Loading {v} at index {b['index']}")
        self.stack.append((l, (s+[v])[-self.program["max_stack"]:], pc+1))
        return True, b

    def store(self, b):
        (l, s, pc) = self.stack.pop(-1)
        l[b["index"]] = s[-1]
        self.log(f"Storing {s[-1]} at index {b['index']}")
        self.stack.append((l, s, pc+1))
        return True, b

    def if1(self, b):
        flag = False
        (l, s, pc) = self.stack.pop(-1)
        self.stack.append((l, s, pc+1))

        v1 = s[-1]
        v2 = s[-2]
        flag = booleans(self,b,v1,v2)

        if flag:
            return self.goto(b)
        return True,b
    
    def ifz(self, b):
        flag = False
        (l, s, pc) = self.stack.pop(-1)
        self.stack.append((l, s, pc+1))
        v1 = s[-1]
        v2 = 0
        flag = booleans(self,b,v1,v2)

        if flag:
            return self.goto(b)
        return True,b

    def goto(self, b):
        (l, s, pc) = self.stack.pop(-1)
        self.log(f"Going to {b['target']}")
        self.stack.append((l, s, b["target"]))
        return True, b

    def incr(self, b):
        (l, s, pc) = self.stack.pop(-1)
        self.log(f"Incrementing {l[b['index']]} by {b['amount']}")
        l[b["index"]] += b["amount"]
        self.stack.append((l, s, pc+1))
        return True, b

    def binary(self, b):
        (l, s, pc) = self.stack.pop(-1)
        v1 = s[-1]
        v2 = s[-2]
        res = binaries(self,b,v1,v2)
        self.stack.append((l, s[:-2] + [res], pc + 1))
        return True, b

    def return1(self, b):
        if b["type"] == None:
            self.log("return None")
            return False, None
        elif b["type"] == "int":
            (l, s, pc) = self.stack.pop(-1)
            self.log("return " + str(s[-1]))
            return False, s[-1]
        else:
            return False, None

    def get1(self, b):  # This should get methods from other classes NOT DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        (l, s, pc) = self.stack.pop(-1)
        self.log("FUNCTION get NOT IMPLEMENTED")
        self.stack.append((l, s, pc + 1))
        return True, b

    def invoke(self, b):  # This should use methods from other classes NOT DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        (l, s, pc) = self.stack.pop(-1)
        self.log("FUNCTION invoke NOT IMPLEMENTED")
        self.stack.append((l, s, pc + 1))
        return True, b

    def push(self, b):
        v = b["value"]["value"]
        (l, s, pc) = self.stack.pop(-1)
        self.stack.append((l, (s + [v])[-self.program["max_stack"]:], pc + 1))
        self.log("push " + str(v))
        return True, b


def testingSimple():
    for method in methods:
        intr = Interpreter(method, None)
        print("Running method: " + method["name"])
        if method["name"] == "noop":
            res = (intr.run(([5, 2, 3, 4][:method["max_locals"]], [], 0)))
            assert res == None
            print("Succeded")
        elif method["name"] == "zero":
            res = (intr.run(([][:method["max_locals"]], [], 0)))
            assert res == 0
            print("Succeded")
        elif method["name"] == "hundredAndTwo":
            res = (intr.run(([][:method["max_locals"]], [], 0)))
            assert res == 102
            print("Succeded")
        elif method["name"] == "identity":
            a = 2
            res = (intr.run(([a][:method["max_locals"]], [], 0)))
            assert res == a
            print("Succeded")
        elif method["name"] == "add":
            a = 2
            b = 4
            res = (intr.run(([a, b][:method["max_locals"]], [], 0)))
            assert res == (a+b)
            print("Succeded")
        elif method["name"] == "factorial":
            res = (intr.run(([3, 0][:method["max_locals"]], [], 0)))
            assert res == 6
            print("Succeded")


testingSimple()
