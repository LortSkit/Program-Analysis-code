import json

data = json.loads(
    open('./course-02242-examples/decompiled/dtu/compute/exec/Simple.json').read())


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


class Interpreter:
    def __init__(self, p, verbose):
        self.program = p
        self.verbose = verbose
        # self.memory = {}
        self.stack = []

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
        if b["condition"] == "gt":
            v1 = s[-1]
            v2 = s[-2]
            if v1 > v2:
                self.log(f"True {v1} > {v2}")
                flag = True
            else:
                self.log(f"False {v1} > {v2}")
        if b["condition"] == "ge":
            v1 = s[-1]
            v2 = s[-2]
            if v1 >= v2:
                self.log(f"True {v1} >= {v2}")
                flag = True
            else:
                self.log(f"False {v1} >= {v2}")

        if b["condition"] == "le":
            v1 = s[-1]
            v2 = s[-2]
            if v1 <= v2:
                self.log(f"True {v1} <= {v2}")
                flag = True
            else:
                self.log(f"False {v1} <= {v2}")

        if flag:
            return self.goto(b)

        return False, s[-1]

    def ifz(self, b):
        flag = False
        (l, s, pc) = self.stack.pop(-1)
        self.stack.append((l, s, pc+1))
        if b["condition"] == "gt":
            v = s[-1]
            if v > 0:
                self.log(f"True {v}>0")
                flag = True
            else:
                self.log(f"False {v}>0")

        if b["condition"] == "le":
            v = s[-1]
            if v <= 0:
                self.log(f"True {v}<=0")
                flag = True
            else:
                self.log(f"False {v}<=0")

        if flag:
            return self.goto(b)

        return True, b

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
        if b["operant"] == "add":
            (l, s, pc) = self.stack.pop(-1)
            v1 = s[-1]
            v2 = s[-2]

            self.log("add " + str(v1) + " + " + str(v2))
            self.stack.append((l, s[:-2] + [v1+v2], pc + 1))

        elif b["operant"] == "sub":
            (l, s, pc) = self.stack.pop(-1)
            v1 = s[-1]
            v2 = s[-2]

            self.log("sub " + str(v1) + " - " + str(v2))
            self.stack.append((l, s[:-2] + [v1-v2], pc + 1))

        elif b["operant"] == "mul":
            (l, s, pc) = self.stack.pop(-1)
            v1 = s[-1]
            v2 = s[-2]

            self.log("mul " + str(v1) + " * " + str(v2))
            self.stack.append((l, s[:-2] + [v1*v2], pc + 1))

        elif b["operant"] == "div":
            (l, s, pc) = self.stack.pop(-1)
            v1 = s[-1]
            v2 = s[-2]
            if v2 == 0:
                raise("Division by zero")

            self.log("div " + str(v1) + " / " + str(v2))
            self.stack.append((l, s[:-2] + [v1/v2], pc + 1))

        elif b["operant"] == "rem":
            (l, s, pc) = self.stack.pop(-1)
            v1 = s[-1]
            v2 = s[-2]

            self.log("rem " + str(v1) + " % " + str(v2))
            self.stack.append((l, s[:-2] + [v1 % v2], pc + 1))
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


# testingSimple()


def testingArithmetics():
    for method in methods:
        intr = Interpreter(method, None)
        print("="*20)
        print("Running method: " + method["name"])
        if method["name"] == "alwaysThrows1":
            try:
                res = (intr.run(([][:method["max_locals"]], [], 0)))
                print("Failed")
            except:
                print("Succeded")
        print("="*20)


testingArithmetics()
