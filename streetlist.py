import sys

odds = dict()
evens = dict()
streets = set()

def print_row(io, street, start, stop, o, e):
    label = f"{street},{start or ''},{stop or ''}"
    if e is None:
        print(f"{label},odd,{o}", file=io)
    elif o is None:
        print(f"{label},even,{e}", file=io)
    elif o == e:
        print(f"{label},both,{o}", file=io)
    else:
        print(f"{label},odd,{o}", file=io)
        print(f"{label},even,{e}", file=io)

def run_street(io, street):
    os = odds.get(street, dict())
    es = evens.get(street, dict())
    ops = set(os.values())
    eps = set(es.values())
    ps = ops.union(eps)

    if len(ps) == 1:
        print(f"{street},,,,{list(ps)[0]}", file=io)
        return

    if len(ops) <= 1 and len(eps) <= 1:
        if len(ops) > 0:
            print(f"{street},,,odd,{list(ops)[0]}", file=io)
        if len(eps) > 0:
            print(f"{street},,,even,{list(eps)[0]}", file=io)
        return
    
    start = stop = e = o = None
    numbers = sorted(list(set(es.keys()).union(set(os.keys()))))
    for i in numbers:
        iseven = i&1 == 0
        newrow = False

        if start is None:
            start = stop = i
            if iseven:
                e = es[i]
            else:
                o = os[i]
        elif iseven:
            if e is None:
                stop = i
                e = es[i]
            elif e == es[i]:
                stop = i
            else:
                newrow = True
        else:
            if o is None:
                stop = i
                o = os[i]
            elif o == os[i]:
                stop = i
            else:
                newrow = True
                
        if newrow:
            print_row(io, street, start, stop, o, e)
            start = stop = i
            o = None if iseven else os[i]
            e = es[i] if iseven else None

    if start is not None:
        print_row(io, street, start, stop, o, e)

with open(sys.argv[1], "r") as f:
    skip = 1
    for line in f:
        if skip > 0:
            skip -= 1
            continue
        fields = line.split("|")
        street = fields[1]
        num = int(fields[2])
        pct = fields[12]

        streets.add(street)
        table = evens if num&1 == 0 else odds
        if street in table:
            streettable = table[street]
        else:
            streettable = dict()
            table[street] = streettable

        streettable[num] = pct
    
with open("streetlist.csv", "w") as io:
    for street in sorted(list(streets)):
        run_street(io, street)
