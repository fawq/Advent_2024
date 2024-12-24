init, text = open("/home/fawqfawq-ubuntu/Projects/DSA/Advent_2024/src/advent/day_24/data.txt").read().split("\n\n")

wires = {}

z_max = ""
for l in text.splitlines():
    vs = l.split()
    lhs = vs[0]
    op = vs[1]
    rhs = vs[2]
    out = vs[4]

    if out[0] == 'z' and z_max < out:
        z_max = out

    wires[out] = [lhs, op, rhs]
z_max = int(z_max[1:])


def evaluate(computed, lhs, op, rhs):
    lhsv = computed.get(lhs)
    if lhsv is None:
        lhsv = evaluate(computed, *wires[lhs])
        computed[lhs] = lhsv

    rhsv = computed.get(rhs)
    if rhsv is None:
        rhsv = evaluate(computed, *wires[rhs])
        computed[rhs] = rhsv

    if op == "AND":
        return lhsv & rhsv
    elif op == "OR":
        return lhsv | rhsv
    elif op == "XOR":
        return lhsv ^ rhsv
    else:
        assert(False)

def check_adder(z_id):
    # TODO This function is a mess lmao
    # For the full adder of zN, we expect in order (where order of args doesnt matter):
    # zN <- a XOR b
    #   a  <- xN XOR yN
    #   b  <- c OR d
    #      c <- xN-1 AND yN-1
    #      d <- e AND f
    #        e <- xN-1 XOR yN-1
    #        f <- g OR h
    #        ... repeats until z00
    # This function checks up to d, ie depth 2
    a0_id, op0, b0_id = wires[z_id]
    if op0 != "XOR":
        return z_id

    nid = None
    need_op = {"XOR", "OR"}
    a1_id, op1, b1_id = wires[a0_id]
    if op1 not in need_op:
        return a0_id
    elif op1 == "XOR" and {a1_id, b1_id} != {f"x{z_id[1:]}", f"y{z_id[1:]}"}:
        return a0_id
    elif op1 == "OR":
        nid = a1_id
        a3_id, op3, b3_id = wires[a1_id]
        a4_id, op4, b4_id = wires[a1_id]
    need_op.remove(op1)

    a2_id, op2, b2_id = wires[b0_id]
    if op2 not in need_op:
        return b0_id
    elif op2 == "XOR" and {a2_id, b2_id} != {f"x{z_id[1:]}", f"y{z_id[1:]}"}:
        return b0_id
    elif op2 == "OR":
        nid = a2_id
        a3_id, op3, b3_id = wires[a2_id]
        a4_id, op4, b4_id = wires[a2_id]

    # technically one of these ANDs might not AND the correct things, but this
    # captures everything in my input.
    if op3 != "AND" or (a3_id[0] in ('x', 'y') and a3_id[1:] != f"{int(z_id[1:])-1:02}"):
        return nid
    if op4 != "AND" or (a4_id[0] in ('x', 'y') and a4_id[1:] != f"{int(z_id[1:])-1:02}"):
        return nid

    return None

bads = []
# Start at 2 as we don't handle low-depth adders.
# If crossed wires in z00, z01, z45, we won't catch them.
for i in range(2, z_max):
    z_id = f"z{i:02}"
    bad = check_adder(z_id)
    if bad:
        print(z_id, bad, wires[bad])
        bads.append(bad)
print(','.join(sorted(bads)))