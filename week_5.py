import json
from copy import deepcopy

data = json.loads(
    open('./course-02242-examples/decompiled/dtu/compute/exec/Array.json').read())


class Pu(ZeroDivisionError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Variable:
    def __init__(self, value):
        if type(value).__name__ == "int":
            self.value = value
            self.type = "int"
        elif type(value).__name__ == "tuple":
            array_type, length, array = value
            self.value = array
            self.type = array_type
            print(length)
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
        interpreter.log(f"Add {v1} + {v2}")
        res = v1+v2
        resa = va1.abstr_add(va2.ps)
    elif b["operant"] == "sub":
        interpreter.log(f"Sub {v1} - {v2}")
        res = v1-v2
        resa = va1.abstr_sub(va2.ps)
    elif b["operant"] == "mul":
        interpreter.log(f"Mul {v1} * {v2}")
        res = v1*v2
        resa = va1.abstr_mul(va2.ps)
    elif b["operant"] == "div":
        interpreter.log(f"Div {v1} / {v2}")
        res = v1//v2
        resa = va1.abstr_div(va2.ps)
    elif b["operant"] == "rem":
        interpreter.log(f"Rem {v1} % {v2}")
        res = v1 % v2
        resa = va1.abstr_rem(va2.ps)
    if len(resa.error) > 0:
        for error in resa.error:
            print(error)
        raise Exception("The above exceptions were thrown")

    return (res, resa)


class ArithmeticSignAnalysis:
    def __init__(self, initial_value):
        if type(initial_value).__name__ == "int":
            self.ps = set(self.alpha(initial_value))
        elif type(initial_value) == "list":
            self.ps = set([])
            for val in initial_value:
                self.ps = set().union(self.ps, self.alpha(val))
        self.error = set([])

    def alpha(self, var):
        return self.sign(var)

    def sign(self, var):
        if var > 0:
            return {"+"}
        if var == 0:
            return {"0"}
        if var < 0:
            return {"-"}

    def abstr_add(self, signs):
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

        return self
#               +   | -        | 0
#        + |{+}     | {+,-,0}  | {+}
#        - |{-,0,+} | {-}      | {-}
#        0 |{+}     | {-}      | {0}

    def abstr_sub(self, signs):
        init_signs = self.ps
        for sign1 in init_signs:
            for sign2 in signs:
                if (sign1 == "+" and sign2 == "+") or (sign1 == "-" and sign2 == "-"):
                    self.ps = set().union(self.ps, {"+", "-", "0"})
                elif (sign1 == "-" and sign2 == "+") or (sign1 == "0" and sign2 == "+") or (sign1 == "-" and sign2 == "0"):
                    self.ps = set().union(self.ps, {"-"})
                elif (sign1 == "+" and sign2 == "-") or (sign1 == "+" and sign2 == "0") or (sign1 == "0" and sign2 == "-"):
                    self.ps = set().union(self.ps, {"+"})
                elif (sign1 == "0" and sign2 == "0"):
                    self.ps = set().union(self.ps, {"0"})
        return self
#               +   | -        | 0
#        + |{+,-,0} | {+}      | {+}
#        - |{-}     | {-,+,0}  | {-}
#        0 |{-}     | {+}      | {0}

    def abstr_mul(self, signs):
        init_signs = self.ps
        for sign1 in init_signs:
            for sign2 in signs:
                if (sign1 == "+" and sign2 == "+") or (sign1 == "-" and sign2 == "-"):
                    self.ps = set().union(self.ps, {"+"})
                elif sign1 == "0" or sign2 == "0":
                    self.ps = set().union(self.ps, {"0"})
                elif (sign1 == "-" and sign2 == "+") or (sign1 == "+" and sign2 == "-"):
                    self.ps = set().union(self.ps, {"-"})

        return self

#               +   | -        | 0
#        + |{+}     | {-}      | {0}
#        - |{-}     | {+}      | {0}
#        0 |{0}     | {0}      | {0}

    def abstr_div(self, signs):
        init_signs = self.ps
        for sign1 in init_signs:
            for sign2 in signs:
                if (sign1 == "+" and sign2 == "+") or (sign1 == "-" and sign2 == "-"):
                    self.ps = set().union(self.ps, {"+", "0"})
                elif (sign1 == "-" and sign2 == "+") or (sign1 == "+" and sign2 == "-"):
                    self.ps = set().union(self.ps, {"-", "0"})
                elif sign2 == "0":
                    self.error = set().union(self.error, "DivisionZeroException")
                elif sign1 == "0":
                    self.ps = set().union(self.ps, {"0"})
        return self

#               +       | -           | 0
#        + |{+,0}       | {-,0}       | {ø}
#        - |{-,0}       | {+,0}       | {ø}
#        0 |{0}         | {0}         | {ø}
    def abstr_rem(self, signs):
        init_signs = self.ps
        for sign1 in init_signs:
            for sign2 in signs:
                if (sign1 == "-" and sign2 == "+") or (sign1 == "-" and sign2 == "-"):
                    self.ps = set().union(self.ps, {"-", "0"})
                elif (sign1 == "+" and sign2 == "+") or (sign1 == "+" and sign2 == "-"):
                    self.ps = set().union(self.ps, {"+", "0"})
                elif sign2 == "0":
                    self.error = set().union(self.error, "DivisionZeroException")
                elif sign1 == "0":
                    self.ps = set().union(self.ps, {"0"})
        return self

#               +       | -           | 0
#        + |{+,0}       | {+,0}      | null
#        - |{-,0}       | {-,0}       | null
#        0 |{0}         | {0}         | null

    def __str__(self):
        return str(self.ps)

    def __repr__(self) -> str:
        return str(self.ps)


class Interpreter:
    def __init__(self, p, abrstraction_class):
        self.program = p
        # self.memory = {}
        self.stack = []
        self.Error = {}
        self.abstraction_class = abrstraction_class

    def log(self, mes):
        print(mes)

    def run(self, f):
        (l, s, pc) = f
        la = [self.abstraction_class(local.value) for local in l]

        sa = []
        f = (l, la, s, sa, pc)

        self.stack.append(f)
        while True:
            flag, ret = self.step()
            if not flag:
                print(l)
                return ret

    def step(self):
        (l, la, s, sa, pc) = self.stack[-1]
        b = self.program["bytecode"][pc]
        if hasattr(self, b["opr"]):
            return getattr(self, b["opr"])(b)
        else:
            print(f"IMPLEMENT {b['opr']} YOU FUCKING IDIOT")
            return False, None

    def pop(self, b):
        (l, la, s, sa, pc) = self.stack.pop(-1)
        # Rule (pop_1)
        if b["words"] == 1:
            if len(s) < 1:
                return False, None
            self.stack.append((l, la, s[:-1], sa[:-1], pc + 1))
        # Rule (pop_2)
        elif b["words"] == 2:
            if len(s) < 2:
                return False, None
            self.stack.append((l, la, s[:-2], sa[:-2], pc + 1))
        else:
            return False, None

    def nop(self, b):
        (l, la, s, sa, pc) = self.stack.pop(-1)
        pc += 1
        self.stack.append((l, la, s, sa, pc))
        return True, b

    def load(self, b):
        (l, la, s, sa, pc) = self.stack.pop(-1)
        type = b["type"]
        v = l[b["index"]]  # Variable
        va = la[b["index"]]
        if type == "int":
            self.log(f"Loading {v.value} from index {b['index']}")
            self.stack.append(
                (l, la, (s+[deepcopy(v)])[-self.program["max_stack"]:], (sa+[va])[-self.program["max_stack"]:], pc+1))
        elif type == "ref":
            self.log(f"Loading {v.value} from index {b['index']}")
            self.stack.append(
                (l, la, (s+[v])[-self.program["max_stack"]:], (sa+[va])[-self.program["max_stack"]:], pc+1))

        return True, b

    def store(self, b):
        (l, la, s, sa, pc) = self.stack.pop(-1)
        try:
            l[b["index"]] = s[-1]
            la[b["index"]] = sa[-1]
        except:
            l.append(s[-1])
            la.append(sa[-1])
        self.log(f"Storing {s[-1].value} at index {b['index']}")
        self.stack.append((l, la, s[:-1], sa, pc+1))
        return True, b

    def if1(self, b):
        flag = False
        (l, la, s, sa, pc) = self.stack.pop(-1)

        v2 = s[-1]
        v1 = s[-2]
        flag = booleans(self, b, v1.value, v2.value)

        self.stack.append((l, la, s[:-2], sa, pc+1))
        if flag:
            return self.goto(b)
        return True, b

    def ifz(self, b):
        flag = False
        (l, la, s, sa, pc) = self.stack.pop(-1)
        v1 = s[-1]
        self.stack.append((l, la, s[:-1], sa, pc+1))
        v2 = Variable(0)
        flag = booleans(self, b, v1.value, v2.value)

        if flag:
            return self.goto(b)
        return True, b

    def goto(self, b):
        (l, la, s, sa, pc) = self.stack.pop(-1)
        self.log(f"Going to {b['target']}")
        self.stack.append((l, la, s, sa, b["target"]))
        return True, b

    def incr(self, b):
        (l, la, s, sa, pc) = self.stack.pop(-1)
        self.log(f"Incrementing {l[b['index']].value} by {b['amount']}")
        l[b["index"]].value += b["amount"]
        amount_sign = self.abstraction_class(b["amount"])
        la[b["index"]] = (la[b["index"]]).abstr_add(amount_sign.ps)
        self.stack.append((l, la, s, sa, pc+1))
        return True, b

    def binary(self, b):
        (l, la, s, sa, pc) = self.stack.pop(-1)
        v1 = s[-1]
        v2 = s[-2]
        va1 = sa[-1]
        va2 = sa[-2]
        (res, resa) = binaries(self, b, v1.value, v2.value, va1, va2)
        self.stack.append(
            (l, la, s[:-2] + [Variable(res)], sa[:-2] + [resa], pc + 1))
        return True, b

    def return1(self, b):
        if b["type"] == None:
            self.log("return None")
            return False, None
        elif b["type"] == "int":
            (l, la, s, sa, pc) = self.stack.pop(-1)
            self.log("return " + str(s[-1].value))
            return False, s[-1].value
        else:
            return False, None

    def get1(self, b):  # This should get methods from other classes NOT DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        (l, la, s, sa, pc) = self.stack.pop(-1)
        self.log("FUNCTION get NOT IMPLEMENTED")
        self.stack.append((l, la, s, sa, pc + 1))
        return True, b

    def invoke(self, b):  # This should use methods from other classes NOT DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        (l, la, s, sa, pc) = self.stack.pop(-1)
        self.log("FUNCTION invoke NOT IMPLEMENTED")
        self.stack.append((l, la, s, sa, pc + 1))
        return True, b

    def push(self, b):
        v = b["value"]["value"]
        va = self.abstraction_class(v)
        (l, la, s, sa, pc) = self.stack.pop(-1)
        self.stack.append(
            (l, la, (s + [Variable(v)])[-self.program["max_stack"]:], (sa + [va])[-self.program["max_stack"]:], pc + 1))
        self.log(f'push {v}')
        return True, b

    def newarray(self, b):
        (l, la, s, sa, pc) = self.stack.pop(-1)
        dim = b["dim"]
        arr_type = b["type"]
        arr_length = s[-1].value
        if dim != 1:
            self.log(f"newarray dim {dim} not implemented")
            return False, None

        self.stack.append(
            (l, la, s[:-1] + [Variable(("int array", arr_length, []))], sa, pc+1))
        self.log(f"newarray of type {arr_type} and length {arr_length}")
        return True, b

    def dup(self, b):
        (l, la, s, sa, pc) = self.stack.pop(-1)
        if s[-1].type == "int array":
            s.append(s[-1])
        elif s[-1].type == "int":
            s.append(deepcopy(s[-1]))
        self.log("Dup")
        self.stack.append((l, la, s, sa, pc + 1))
        return True, b

    def array_store(self, b):
        (l, la, s, sa, pc) = self.stack.pop(-1)
        arr_val = s.pop()
        arr_index = s.pop()
        arr_ref = s.pop()
        arr_ref.value[arr_index.value] = arr_val.value

        self.log(f"array_store {arr_val} at {arr_index} in {arr_ref}")
        self.stack.append((l, la, s, sa, pc+1))
        return True, b

    def array_load(self, b):
        (l, la, s, sa, pc) = self.stack.pop(-1)

        index = s.pop().value
        array = s.pop().value
        result = Variable(array[index])

        self.stack.append((l, la, s + [result], sa, pc+1))
        self.log(f"array load {index} {array}")

        return True, b

    def arraylength(self, b):
        (l, la, s, sa, pc) = self.stack.pop(-1)

        array_ref = s.pop()
        self.stack.append((l, la, s + [Variable(array_ref.length)], sa, pc+1))
        self.log(f"array length {array_ref.length}")
        return True, b


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


# testingSimple()


for method in methods:
    intr = Interpreter(method, ArithmeticSignAnalysis)
    if method["name"] == "first":
        print(method["name"])

        res = intr.run(([Variable(("int array", 3, [3, 2, 1]))], [], 0))
        print(res)
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
    elif method["name"] == "bubbleSort":
        print(method["name"])
        res = intr.run(
            ([Variable(("int array", 2, [6, 5, 4, 3, 2, 1]))], [], 0))
        print(res)
