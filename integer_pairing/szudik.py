from math import isqrt
from functools import partial 
from _interface import abstractPair, abstractUnpair

def _pair(m, n):
    return n*n+m if n > m else m*m+m*n

def _unpair(n):
   q = isqrt(n)
   l = n - q*q 
   return (l, q) if l < q else (q, l-q) 

pair = partial(abstractPair, pair_fun=_pair)
unpair = partial(abstractUnpair, unpair_fun=_unpair)