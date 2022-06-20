from abc import ABC
from functools import reduce
from collections import deque


class Pairing(ABC):
    def __init__(self, pair_fun, unpair_fun):
        self._pair = pair_fun
        self._unpair = unpair_fun

    @staticmethod
    def _encodeNegatives(l):
        return [2 * x if x >= 0 else -2 * x + 1 for x in l]

    @staticmethod
    def _decodeNegatives(l):
        return [x // 2 if x % 2 == 0 else -(x - 1) // 2 for x in l]

    @staticmethod
    def _containsNegatives(l):
        for x in l:
            if x < 0:
                return True
        return False

    def pair(self, *args):
        assert args, "you have to pair something"
        assert all(isinstance(x, int) for x in args)

        if self._containsNegatives(args):
            args = self._encodeNegatives(args)

        return reduce(self._pair, args) if len(args) > 1 else args[0]

    def unpair(self, n, dim=2, neg=False):
        assert isinstance(n, int)
        assert isinstance(dim, int)
        assert isinstance(neg, bool)
        assert dim >= 1

        p = deque([])
        for _ in range(dim - 1):
            n, m = self._unpair(n)
            p.appendleft(m)
        p.appendleft(n)

        if neg:
            p = self._decodeNegatives(p)
        return tuple(p)


class Bundle(ABC):
    def __init__(self, bundle_fun, unbundle_fun):
        self._bundle = bundle_fun
        self._unbundle = unbundle_fun

    def pair(self, *args):
        assert args, "you have to pair something"
        assert all(isinstance(x, int) for x in args)
        return self._bundle(args)

    def unpair(self, n, neg=False):
        assert isinstance(n, int)
        assert isinstance(neg, bool)
        assert n >= 0
        return self._unbundle(n)