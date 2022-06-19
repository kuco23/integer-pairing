# integer-pairing

This library enables encodings of integer tuples as one integer. It implements two types of encodings - Cantor and Szudzik.
There is a [great article](https://www.vertexfragment.com/ramblings/cantor-szudzik-pairing-functions/) on those two types.

## Usage
The base example is
```python
from integer_pairing import cantor, szudzik

cantor.pair(11, 13) # 313
cantor.unpair(313) # (11, 13)

szudzik.pair(11, 13) # 180
szudzik.unpair(180) # (11, 13)
```
You pair tuples of any size, but have to imply the size when unpairing
```python
cantor.pair(11, 13, 17, 19, 23) # 1115111727200556569
cantor.unpair(1251, dim=5) # (11, 13, 17, 19, 23)
```
You can also include negative numbers, but need to imply that when decoding
```python 
cantor.pair(11, 13, -1) # 726618
cantor.unpair(726618, dim=3, neg=True) # (11, 13, -1)
```
Naive implementations of the above algorithms, fail to account for very large
integers, as they use numeric calculation of the square root. Python allows for 
integers of any size to be stored, but converts them to float (64 bits) when doing numeric operations, 
so this approximation ruins the unpairing. Luckily this can be (efficiently) solved and is implemented here.
```python
cantor.pair(655482261805334959278882253227, 730728447469919519177553911051)
# 960790065254702046274404114853633027146937669672812473623832
cantor.unpair(960790065254702046274404114853633027146937669672812473623832)
# (655482261805334959278882253227, 730728447469919519177553911051)
```

## Complexity
The pairing of n integers will result in an integer of the size of about their product.

## Examples of usage

### Pairing of real numbers
You can represent any computationally-realistic real number with a fraction, 
which is a pair of integers and can be encoded as one integer.

### Cryptographic salting
When encrypting messages deterministically, an attacker can always reproduce the encryption 
of any chosen messages. If those possibilities are few (like `0` / `1`), those kinds 
of algorithms are pretty useless. This is solved by appending a random number, called salt, 
to the message. Here it can be useful to implement this appending via pairing, as
```python
from random import getrandbites
from pairing import szudzik

salt = getrandbites(200)
message = 0
encoded = cantor.pair(message, salt)
```
