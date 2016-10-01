class Node(object):
    def __init__(self):
        pass


    def indent(self, arr):
        if len(arr) == 0:
            return ["    pass"]

        return ["    " + x for x in arr]


    def to_python(self):
        assert False, "Pure virtual"


class Constant(Node):
    def __init__(self, value):
        Node.__init__(self)
        self.value = value


    def to_python(self):
        return [], self.value


class NoOp(Node):
    def __init__(self):
        Node.__init__(self)


    def to_python(self):
        return ["pass"], "None"


class Var(Node):
    def __init__(self, name):
        Node.__init__(self)
        self.name = name


    def to_python(self):
        return [], self.name


class Assign(Node):
    def __init__(self, var, expr):
        Node.__init__(self)
        self.var = var
        self.expr = expr


    def to_python(self):
        assert type(self.var) in [Assign, Var], type(self.var)
        vc, va = self.var.to_python()
        ec, ea = self.expr.to_python()
        return vc + ec + ["%s = %s" % (va, ea)], va


class If(Node):
    def __init__(self, cond, then, else_):
        Node.__init__(self)
        self.cond = cond
        self.then = then
        self.else_ = else_


    def to_python(self):
        cc, ca = self.cond.to_python()
        tc, ta = self.then.to_python()
        ec, ea = self.else_.to_python()
        return cc + ["if %s:" % ca] + self.indent(tc) + ["else:"] + self.indent(ec), "%s if (%s) else %s" % (ta, ca, ea)


class While(Node):
    def __init__(self, cond, action):
        Node.__init__(self)
        self.cond = cond
        self.action = action


    def to_python(self):
        print self.cond
        cc, ca = self.cond.to_python()
        ac, aa = self.action.to_python()
        return cc + ["while %s:" % ca] + self.indent(ac), "None"


class BinaryOp(Node):
    def __init__(self, op, lhs, rhs):
        Node.__init__(self)
        self.op = op
        self.lhs = lhs
        self.rhs = rhs


    def to_python(self):
        lc, la = self.lhs.to_python()
        rc, ra = self.rhs.to_python()

        return lc + rc, "%s %s %s" % (la, self.op, ra)


class Sequential(Node):
    def __init__(self, *args):
        Node.__init__(self)
        self.arr = args


    def to_python(self):
        xx = [x.to_python() for x in self.arr]
        return sum([x[0] for x in xx], []), xx[-1][1]


if __name__ == "__main__":
    a = Var('a')
    b = Var('b')
    c = Var('c')
    idx = Var('idx')

    init = Sequential(*[
        Assign(a, Constant(1)),
        Assign(b, Constant(1)),
        Assign(idx, Constant(1))
    ])

    body = Sequential(*[
        Assign(c, BinaryOp('+', a, b)),
        Assign(a, b),
        Assign(b, c),
        Assign(idx, BinaryOp('+', idx, Constant(1)))
    ])

    loop = While(BinaryOp('<', idx, Constant(10)), body)

    full = Sequential(init, loop, c)

    code, ret = full.to_python()
    print '\n'.join(code)
    print "return %s" % ret

