from graph import *
import random
import sys

next_var = 0

def var_name():
    global next_var
    if next_var < 26:
        ret = chr(ord('a') + next_var)
    else:
        ret = "var%s" % next_var
    next_var += 1
    return ret

def gen_one(complexity = 4):
    whats = ["constant", "simple1", "cond", "simple2", "cond"]
    what = whats[random.randint(0, complexity)]

    if what == "constant":
        x = random.randint(1, 100)
        return str(x), Constant(x)

    if what == "simple1":
        op = random.choice(["+", "-", "*"])
        xs, xg = gen_one(complexity - 1)
        ys, yg = gen_one(complexity - 1)
        return "(%s %s %s)" % (xs, op, ys), BinaryOp(op, xg, yg)

    if what == "simple2":
        op = random.choice(["+", "-", "*"])
        op2 = "+"
        xs, xg = gen_one(complexity - 1)
        ys, yg = gen_one(complexity - 1)
        zs, zg = gen_one(complexity - 1)
        xname, yname, zname = var_name(), var_name(), var_name()
        x = Var(xname)
        y = Var(yname)
        z = Var(zname)
        b1 = BinaryOp(op, x, y)
        b2 = BinaryOp(op, x, z)
        ret = Sequential(Assign(x, xg), Assign(y, yg), Assign(z, zg), BinaryOp(op2, b1, b2))
        
        return "((%s %s %s) %s (%s %s %s), where %s is %s, %s is %s and %s is %s)" % (xname, op, yname, op2, xname, op, zname, xname, xs, yname, ys, zname, zs), ret

    if what == "cond":
        ts, tg = gen_one(complexity - 1)
        es, eg = gen_one(complexity - 1)
        lhs, lhg = gen_one(1)
        rhs = random.randint(1, 100)
        op = random.choice(["<", ">"])

        return "(%s if %s %s %s, else %s)" % (ts, lhs, op, rhs, es), If(BinaryOp(op, lhg, Constant(rhs)), tg, eg)


def gen(complexity):
    while True:
        s, g = gen_one(complexity)
        lines, ret = g.to_python()
        func = 'def moo():\n' + '\n'.join(['    ' + x for x in lines]) + "\n    return %s" % ret
        try:
            exec(func)
        except:
            print func
            raise
        yield "Compute %s" % s, g, eval("moo()")


if __name__ == "__main__":
    import itertools
    for desc, graph, output in itertools.islice(gen(int(sys.argv[1])), 10):
        print desc
        print "Expected output: %s" % output
        lines, ret = graph.to_python()
        print '\n'.join(lines)
        print "return %s" % ret
        print "======================"



