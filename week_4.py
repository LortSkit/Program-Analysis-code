import json

data = json.loads(open('./decompiled/dtu/compute/exec/Simple.json').read())


def cleanByteCode(bytecofr):
    for b in bytecofr:
        del b["offset"]
        if b["opr"] == "return":
            b["opr"] = "return1"
    return bytecofr


def getCleanMethods(data):
    methods = []
    # print(data['methods'])
    for method in data["methods"]:
        for annotation in method["annotations"]:
            if annotation["type"] == "dtu/compute/exec/Case":
                methods.append(
                    {"name": method["name"], "bytecode": cleanByteCode(method["code"]["bytecode"])})
                break
            # return []

    return methods


methods = getCleanMethods(data)
# print(methods)

# for dic in methods[0]["bytecode"]:
#     if dic["opr"] == "binary":
#         pass
#     if dic["opr"] == "arraylength":
#         pass
#     if dic["opr"] == "return":
#         pass
#     if dic["opr"] == "nop":
#         pass
# if dic["operant"] == "add":
#     pass
# if dic["operant"] == "mul":
#     pass
# if dic["operant"] == "add":
#     pass


class Interpreter:
    # operants = ["add", "mul", "sub", "div", "rem"]
    # op = {
    #     "add": (),
    #     "mul": (),
    #     "sub": (),
    #     "div": (),
    #     "rem": ()
    # }

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

        return None

        # self.log_done()

    def step(self):
        (l, s, pc) = self.stack[-1]
        b = self.program["bytecode"][pc]
        if hasattr(self, b["opr"]):
            # print("we are here: ")
            # print(b["opr"])
            return getattr(self, b["opr"])(b)
        else:
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

    # def invoke(self,b):
    #     return True

    def nop(self, b):
        (l, s, pc) = self.stack.pop(-1)
        pc += 1
        self.stack.append((l, s, pc))
        return True, b

    def load(self, b):
        (l, s, pc) = self.stack.pop(-1)
        v = l[b["index"]]
        self.log("Loading at index " + str(v))
        self.stack.append((l, s+[v], pc+1))
        return True, b

    def binary(self, b):
        if b["operant"] == "add":
            (l, s, pc) = self.stack.pop(-1)
            v1 = s[-1]
            v2 = s[-2]

            self.log("add " + str(v1) + " + " + str(v2))
            self.stack.append((l, s[:-2] + [v1+v2], pc + 1))
        return True, b
        # elif b["operant"] == "add":

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

    def push(self, b):
        v = b["value"]["value"]
        (l, s, pc) = self.stack.pop(-1)
        self.stack.append((l, s + [v], pc + 1))
        self.log("push " + str(v))
        return True, b


# for method in methods:
for method in methods:
    intr = Interpreter(method, None)
    print("Running method: " + method["name"])
    res = (intr.run(([1, 2], [], 0)))
    print("Return: " + str(res))
