from utils.util import binaries, booleans, getCleanMethods, Variable
from copy import deepcopy


class Interpreter:
    def __init__(self, p, abrstraction_class, verbose=False):
        self.program = p
        self.verbose = verbose
        # self.memory = {}
        self.stack = []
        self.error = {}
        self.abstraction_class = abrstraction_class

    def log(self, mes):
        if self.verbose:
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
        if type == "int":
            v = l[b["index"]]  # Variable
            va = la[b["index"]]
            self.log(f"Loading {v.value} from index {b['index']}")
            self.stack.append(
                (l, la, (s+[deepcopy(v)])[-self.program["max_stack"]:], (sa+[va])[-self.program["max_stack"]:], pc+1))
        elif type == "ref":
            try:
                v = l[b["index"]]  # Variable
                va = la[b["index"]]
            except:
                raise Exception("Index out of bounds")
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
        if b["operant"] == "div" and v1.value == 0:
            raise Exception("Division by zero")
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
