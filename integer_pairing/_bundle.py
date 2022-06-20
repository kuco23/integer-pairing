from ._interface import Bundle


def tobase(n, b, sym):
    s = ''
    while n > 0:
        kl = n % b
        n //= b
        s += sym(kl)
    return s[::-1] if s else sym(0)

def frombase(s, b, idx):
    n = 0
    bl = 1
    for a in reversed(s):
        n += idx(a) * bl
        bl *= b
    return n

base3 = ['0', '1', '2']
base3e = lambda n: tobase(n, 3, base3.__getitem__)
base3d = lambda w: frombase(w, 3, base3.index)

base2 = ['0', '1']
base2e = lambda n: tobase(n, 2, base2.__getitem__)
base2d = lambda w: frombase(w, 2, base2.index)


def _bundle(nums):
    s = ''
    for n in nums:
        prepend = '2' if n >= 0 else '22'
        s += prepend + base2e(abs(n))
    return base3d(s)


def _unbundle(n):
    s = base3e(n)
    i, j, l = 0, 0, []
    while i < len(s):
        di = 1 if s[i+1] != '2' else 2
        j = i + di
        while j < len(s) and s[j] != '2': 
            j += 1
        sign = 1 if di == 1 else -1
        m = sign * base2d(s[i+di:j])
        l.append(m)
        i = j
    return tuple(l)

bundle = Bundle(_bundle, _unbundle)
