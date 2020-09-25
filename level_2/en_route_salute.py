def solution(s):
  right_walkers = 0
  salutes = 0

  for c in s:
    if c == '>':
      right_walkers += 1
    elif c == '<':
      salutes += (2 * right_walkers)

  return salutes


assert solution(">----<") == 2
assert solution("<<>><") == 4
assert solution("><<>><") == 10
assert solution("--->-><-><-->-") == 10
