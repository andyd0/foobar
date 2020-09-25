# The Grandest Staircase of Them All

def solution(n):
  # since n will always be at least 3, no point in building cache
  # etc if we know it's going to be 1.
  if n == 3:
    return 1

  # memo is used to avoid retrying any sub solution that may
  # occur during recursion. +2 is needed for size as height is incremented
  # at each recursive step so need to ensure there is padded space that will
  # allow height > num_of_bricks to return 0
  memo = [[-1 for j in range(n+2)] for i in range(n+2)]
  return staircases_count(1, n, memo) - 1

def staircases_count(height, num_of_bricks, memo):
  # return the count known for this height and bricks
  if memo[height][num_of_bricks] != -1:
    return memo[height][num_of_bricks]
  # all bricks have been used up so we know
  # we have a valid staircase
  if num_of_bricks == 0:
    return 1
  # can't build to this height if not enough
  # bricks so it's an invalid staircase
  if height > num_of_bricks:
    return 0
  
  # Try to build a new stair with the remaining bricks
  new_stair = staircases_count(height + 1, num_of_bricks - height, memo)
  # Otherwise, try the next height
  next_height = staircases_count(height + 1, num_of_bricks, memo)

  memo[height][num_of_bricks] = new_stair + next_height
  return memo[height][num_of_bricks]


assert solution(3) == 1
assert solution(4) == 1
assert solution(5) == 2
assert solution(8) == 5
