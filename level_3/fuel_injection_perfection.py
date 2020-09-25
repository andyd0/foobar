# Fuel Injection Perfection

def solution(n):
  # Python will convert n to bignum if necessary so 309 digits should
  # be fine
  n = int(n)
  count = 0

  while n > 1:
    # Last bit of a binary number indicates whether the number is odd
    # if the last bit is 1, it's odd. n & to 1 will lead to either 1 or 0
    if n & 1 == 1:
      # if odd, +/- is based on whether the number is a multiple of 4
      # to ensure the subsequent number is still even and then on the even
      # path. 3 is a special case as we always want to choose 2 to avoid
      # the aditional step
      if n != 3 and ((n + 1) % 4 == 0):
        n += 1
      else:
        n -= 1
    else:
      # shifting the binary number by 1 to the right divides by 2.
      n >>= 1

    count += 1

  return count

assert solution('3') == 2
assert solution('15') == 5
assert solution('4') == 2
assert solution('16') == 4
assert solution('17') == 5
assert solution('18') == 5
assert solution('19') == 6
