from collections import deque

class Element:
  def __init__(self, i, j):
    self.i = i
    self.j = j

  def __eq__(self, other):
    return self.i == other.i and self.j == other.j
  
  def __hash__(self):
    return hash((self.i, self.j))

class Map:
  def __init__(self, map):
    self.map = map
    self.height = len(map)
    self.width = len(map[0])

    self.wall = 1
    self.passable = 0

    self.src = Element(0, 0)
    self.dst = Element(self.height-1, self.width-1)

    self.walled_elements = self._get_walled_elements()
    self.valid_moves = [
      Element(1, 0), Element(-1, 0), Element(0, 1), Element(0, -1)
    ]


  def _get_walled_elements(self):
    '''
    Pre processing to know where all walled elements in the matrix are. This
    will be used to mark and unmark walled elements in the matrix while BFS
    processing. Since the max size of a side is 20, pre-processing should be fast
    '''

    walls = deque()
    for i in range(self.height):
      for j in range(self.width):
        if self.map[i][j] == self.wall:
          walls.append(Element(i, j))
    return walls


  def _is_valid(self, move):
    '''
    Checks if the next move is...
    1. Within the bounds of the matrix
    2. Not a wall
    '''

    return 0 <= move.i < self.height and 0 <= move.j < self.width \
    and self.map[move.i][move.j] != self.wall


  def _distance_to_dst(self):
    '''
    Gets the distance using BFS to find the shortest path from source to destination
    based on the current version of the matrix.
    '''

    queue = deque()
    queue.append(self.src)

    moves = 1
    visited = set()
    next_moves = deque()

    # Queue will have elements to process for the next level / next
    # neighbors
    while queue:
      element = queue.popleft()

      # Reached destination so return
      if element == self.dst:
        return moves

      # If not, get next moves from current element
      if element not in visited:
        visited.add(element)

        for move in self.valid_moves:
          next_move = Element(element.i + move.i, element.j + move.j)
          if self._is_valid(next_move):
            next_moves.append(next_move)

      # Got all the next moves so update the queue.
      # Also, moves incremented by 1 as the current "level" / immediate
      # neighbors have been processed
      if not queue:
        queue = next_moves
        next_moves = deque()
        moves += 1

    # Some paths may not reach destination so ensure distance returned
    # will not distort the shortest distance
    return float('inf')

  def shortest_distance(self):
    '''
    Gets the shortest distance. If there aren't any walled elements
    in the matrix, no need to iterate over. If there are, iterate over walled
    elements and mark / unmark while getting the shortest path for the current
    version of the matrix and get the minimum from that.
    '''

    shortest = float('inf')
    if not self.walled_elements:
      shortest = self._distance_to_dst()
    else:
      while self.walled_elements:
        element = self.walled_elements.popleft()
        self.map[element.i][element.j] = self.passable
        distance = self._distance_to_dst()
        shortest = min(distance, shortest)
        self.map[element.i][element.j] = self.wall
    return shortest

def solution(map):
  map_instance = Map(map)
  return map_instance.shortest_distance()


assert solution(
  [
    [0, 1, 1, 0],
    [0, 0, 0, 1],
    [1, 1, 0, 0],
    [1, 1, 1, 0]
  ]
) == 7

assert solution(
  [
    [0, 1, 1, 0],
    [0, 0, 0, 1],
    [1, 0, 0, 0],
    [0, 0, 1, 0]
  ]
) == 7

assert solution(
  [
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0]
  ]
) == 11
