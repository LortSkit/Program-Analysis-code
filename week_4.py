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
                methods.append({"name":method["name"], "bytecode": cleanByteCode(method["code"]["bytecode"])})
                break
            # return []
            
       

    return methods

methods = getCleanMethods(data)
# print(methods)

for dic in methods[0]["bytecode"]:
    if dic["opr"] == "binary":
        pass
    if dic["opr"] == "arraylength":
        pass
    if dic["opr"] == "return":
        pass
    if dic["opr"] == "nop":
        pass
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

    def __init__(self, p , verbose):
        self.program = p
        self.verbose = verbose
        # self.memory = {}
        self.stack = []

    def run(self, f):
        self.stack.append(f)
        # self.log_start()
        # self.log_state()
        while self.step():
            # self.log_state()
            continue
        # self.log_done()

    def step(self):
        (l, s, pc) = self.stack[-1]
        b = self.program["bytecode"][pc]
        if hasattr(self, b["opr"]):
            print("we are here: ")
            print(b["opr"])
            return getattr(self, b["opr"])(b)
        else:
            return False

    def pop(self, b):
        (l, s, pc) = self.stack.pop(-1)
        # Rule (pop_1)
        if b["words"] == 1:
            if len(s) < 1: return False
            self.stack.append((l, s[:-1], pc + 1))
        # Rule (pop_2)
        elif b["words"] == 2:
            if len(s) < 2: return False
            self.stack.append((l, s[:-2], pc + 1))
        else:
            return False

    # def invoke(self,b):
    #     return True

    def nop(self,b):
        (l, s, pc) = self.stack.pop(-1)
        pc += 1
        self.stack.append((l,s,pc))
        return True

    def binary(self,b):
        print(b)
        if b["operant"] == "add":
            (l,s1,pc) = self.stack.pop(-1)
            (l,s2,pc) = self.stack.pop(-1)
            self.append((l,s1+s2, pc + 1))
        return True
        # elif b["operant"] == "add":


    def load(self,b):
        print(b)
        (l, s, pc) = self.stack.pop(-1)
        print(b["index"])
        v = l[b["index"]]
        self.stack.append(l,s+v,pc+1)
        return True

    # def return1(self,b):
    #     pass

    # def arraylength(self,b):
    #     pass

# print(methods)

# for method in methods:
for method in methods:
    intr = Interpreter(method,None)
    print("      ")
    print(method)
    intr.run(([],[],0))  