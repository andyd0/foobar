from collections import deque

def to_decimal_string(n, b):
  n = int(n)
  to_decimal = 0
  exp = 0

  while n > 0:
    to_decimal += ((n % 10) * (b ** exp))
    exp += 1
    n //= 10

  return str(to_decimal)

def to_base_string(n, b):
  n = int(n)
  to_base = deque()

  while n > 0:
    to_base.appendleft(str(n % b))
    n //= b
    
  return  ''.join(to_base)

def pad_zeros(n, k):
  if len(n) != k:
    diff = k - len(n)
    n = ('0' * diff) + n
  return n

def compute_z_next(x, y, b):
  if b != 10:
    x = to_decimal_string(x, b)
    y = to_decimal_string(y, b)
    
  z_int = int(x) - int(y)
  return to_base_string(str(z_int), b) if b != 10 else str(z_int)


def solution(n, b):
  # keeps track of order of new computed elements for 
  # quick look up
  index = {}
  i = 0
  k = len(n)
  z_current = n
  z_next = None

  while True:
    y = ''.join(sorted(z_current))
    x = y[::-1]

    z_next = compute_z_next(x, y, b)
    z_next = pad_zeros(z_next, k)

    if z_next in index:
      index[z_current] = i
      break
    
    index[z_current] = i
    z_current = z_next
    i += 1

  # returns the position of the end position of the cycle
  return index[z_current] - index[z_next] + 1


assert solution('1211', 10) == 1
assert solution('210022', 3) == 3