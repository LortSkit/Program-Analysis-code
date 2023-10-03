class ArithmeticSignAnalysis:
    def __init__(self, initial_value):
        print(type(initial_value))
        if type(initial_value).__name__ == "int":
            self.ps = set(self.alpha(initial_value))
        elif type(initial_value).__name__ == "list":
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
                elif (
                    (sign1 == "0" and sign2 == "-")
                    or (sign1 == "-" and sign2 == "0")
                    or (sign1 == "-" and sign2 == "-")
                ):
                    self.ps = set().union(self.ps, {"-"})
                elif sign1 == "0" and sign2 == "0":
                    self.ps = set().union(self.ps, {"0"})

        return self

    #               +   | -        | 0
    #        + |{+}     | {+,-,0}  | {+}
    #        - |{-,0,+} | {-}      | {-}
    #        0 |{+}     | {-}      | {0}

    def abstr_negate(self):
        new_signs = set()
        for sign in self.ps:
            if sign == "-":
                new_signs.add("+")
            elif sign == "+":
                new_signs.add("-")
            elif sign == "0":
                new_signs.add("0")
        self.ps = new_signs
        return self

    def abstr_sub(self, signs):
        init_signs = self.ps
        for sign1 in init_signs:
            for sign2 in signs:
                if (sign1 == "+" and sign2 == "+") or (sign1 == "-" and sign2 == "-"):
                    self.ps = set().union(self.ps, {"+", "-", "0"})
                elif (
                    (sign1 == "-" and sign2 == "+")
                    or (sign1 == "0" and sign2 == "+")
                    or (sign1 == "-" and sign2 == "0")
                ):
                    self.ps = set().union(self.ps, {"-"})
                elif (
                    (sign1 == "+" and sign2 == "-")
                    or (sign1 == "+" and sign2 == "0")
                    or (sign1 == "0" and sign2 == "-")
                ):
                    self.ps = set().union(self.ps, {"+"})
                elif sign1 == "0" and sign2 == "0":
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
        print(self.ps)
        return str(self.ps)
