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
You can pair tuples of any size, but have to specify the size when unpairing
```python
cantor.pair(11, 13, 17, 19, 23) # 1115111727200556569
cantor.unpair(1115111727200556569, dim=5) # (11, 13, 17, 19, 23)
```
It is also possible to include negative numbers, but you need to imply that when decoding
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
You can also pair things in a way that encodes the tuple's dimension and its signs. 
This is called bundleing and is done by encoding each number in a tuple in binary, 
then prepending those encodings by the number 2 or 22, depending on its sign.
For space-efficiency, the string is then interpreted in a trinary base system.
```python
from integer_pairing import bundle

bundle.pair(*range(-8,8))
# 1061264631713144962268472871675
bundle.unpair(1061264631713144962268472871675)
# (-8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7)
```
The downside here is that `bundle.pair` is not surjective, so not every number can be unpaired. 
Calling unpair on those will produce an exception
```python
bundle.unpair(0)
              
Traceback (most recent call last):
  File "<pyshell#37>", line 1, in <module>
    bundle.unpair(0)
  File "C:\Users\kuco\integer-pairing\integer_pairing\_interface.py", line 66, in unpair
    return self._unbundle(n)
  File "C:\Users\kuco\integer-pairing\integer_pairing\_bundle.py", line 41, in _unbundle
    di = 1 if s[i+1] != '2' else 2
IndexError: string index out of range
```

## Complexity
The pairing of n integers will result in an integer of the size of about their product.

## Example usage from Cryptography
When encrypting messages deterministically, an attacker can always reproduce the encryption 
of any chosen messages. If those possibilities are few (like `0` / `1`), those kinds 
of algorithms are pretty useless. This is solved by appending a random number, called salt, 
to the message. It can be useful to implement this appending via pairing.
```python
from random import getrandbites

salt = getrandbites(200)
message = 0
encoded = szudzik.pair(message, salt)
```
