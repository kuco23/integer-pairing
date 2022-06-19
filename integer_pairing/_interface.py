from functools import reduce

def _encodeNegatives(l):
    return [2*x if x>=0 else -2*x+1 for x in l]

def _decodeNegatives(l):
    return [x//2 if x%2==0 else -(x-1)//2 for x in l]

def abstractPair(*args, pair_fun):
    assert args, "you have to pair something"
    assert all(isinstance(x, int) for x in args)

    for x in args:
        if x < 0:
            args = _encodeNegatives(args)
            break

    if len(args) == 1: return args[0]
    return reduce(pair_fun, args)

def abstractUnpair(n, dim=2, neg=False, unpair_fun=False):
    assert isinstance(n, int)
    assert isinstance(dim, int)
    assert dim >= 1
    
    p = []
    for _ in range(dim-1):
        n, m = unpair_fun(n)
        p.append(m)
    p.append(n)
    
    p.reverse()
    if neg: p = _decodeNegatives(p)
    return tuple(p)