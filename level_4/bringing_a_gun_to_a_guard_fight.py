# Bringing a Gun to a Guard Fight

import math

class Coordinate:
  def __init__(self, x, y, role):
    self.x = x
    self.y = y
    self.role = role

class Room:
  player_label = 0
  guard_label = 1

  def __init__(self, dimensions, player, guard, distance):
    self.width = dimensions[0]
    self.height = dimensions[1]
    self.player = Coordinate(player[0], player[1], self.player_label)
    self.guard = Coordinate(guard[0], guard[1], self.guard_label)
    self.distance = distance
    self.num_vertical_reflections = math.ceil((self.player.y + self.distance + 1) / self.height)
    self.num_horizontal_reflections = math.ceil((self.player.x + self.distance + 1) / self.width)

  def __euclidean_distance_from_player(self, coordinate):
    return math.sqrt(((coordinate.x - self.player.x) ** 2) + ((coordinate.y - self.player.y) ** 2))

  def __angle_from_player(self, coordinate):
    return math.atan2(coordinate.x - self.player.x, coordinate.y - self.player.y)

  def __compute_vertical_coordinates(self, coordinates, player, guard):
    '''
    Computes coordinates for both player and guard for the y axis
    '''

    start = 0
    end = self.height
    reflections = self.num_vertical_reflections

    while reflections > 0:
      player_distance = end - player.y
      guard_distance = end - guard.y

      start = end
      end += self.height

      player = Coordinate(player.x, start + player_distance, self.player_label)
      guard = Coordinate(guard.x, start + guard_distance, self.guard_label)

      if self.__euclidean_distance_from_player(player) <= self.distance:
        coordinates.append(player)

      if self.__euclidean_distance_from_player(guard) <= self.distance:
        coordinates.append(guard)

      reflections -= 1

  def __compute_coordinates(self, coordinates):
    '''
    Computes coordinates for both player and guard for the 
    x axis with each new set vertical ones are computed above
    '''

    start = 0
    end = self.width
    player = self.player
    guard = self.guard
    reflections = self.num_horizontal_reflections

    coordinates.append(player)
    coordinates.append(guard)
    self.__compute_vertical_coordinates(coordinates, player, guard)

    while reflections > 0:
      player_distance = end - player.x
      guard_distance = end - guard.x

      start = end
      end += self.width

      player = Coordinate(start + player_distance, player.y, self.player_label)
      guard = Coordinate(start + guard_distance, guard.y, self.guard_label)

      if self.__euclidean_distance_from_player(player) <= self.distance:
        coordinates.append(player)

      if self.__euclidean_distance_from_player(guard) <= self.distance:
        coordinates.append(guard)
      
      self.__compute_vertical_coordinates(coordinates, player, guard)

      reflections -= 1

  def __compute_first_quadrant_coordinates(self):
    '''
    Compute coordinates for the first quadrant - i.e. where
    both x and y are positive
    '''

    coordinates = []
    self.__compute_coordinates(coordinates)
    return coordinates

  def __compute_reflect_coordinates(self, coordinates):
    '''
    Compute reflected coordinates for the other 3 quadrants.
    Reflection of coordinate is adjusting x or y or both by
    -1
    '''

    quardrant_reflections = [[-1, 1], [-1, -1], [1, -1]]
    reflected_coordinates = []
    for coordinate in coordinates:
      for reflection in quardrant_reflections:
        reflected_coordinate = Coordinate(
          coordinate.x * reflection[0],
          coordinate.y * reflection[1],
          coordinate.role
        )
        reflected_coordinates.append(reflected_coordinate)
    return coordinates + reflected_coordinates
  
  def __valid_beam_movements(self, coordinates):
    '''
    Valid movements are found using both distance and angle.
    Keep coordinates where the distance for the beam is shortest.
    A hash is used to keep track of valid movements of the beam
    using the angle as key. Regardless of whether the coordinate
    is from player to guard or player to player, if the angle is the
    same we want to keep the shortest. If coordinates share the same angle, 
    the one with the shortest distance will block the other.
    '''

    valid = {}

    for coordinate in coordinates:
      distance = self.__euclidean_distance_from_player(coordinate)
      angle = self.__angle_from_player(coordinate)
      if 0 < distance <= self.distance:
        if angle not in valid or valid[angle][1] > distance:
          valid[angle] = [coordinate, distance]

    return valid

  def __valid_count(self, coordinates):
    '''
    Count up the number of valid movements that are to the guard. Valid
    movementes will also contain player to player but these are blocking
    guards on the same angle so should be ignored.
    '''

    valid = self.__valid_beam_movements(coordinates)
    valid = filter(lambda element: element[1][0].role == self.guard_label, valid.items())
    return len(list(valid))

  def __get_coordinates(self):
    '''
    Get all quadrant coordinates
    '''

    coordinates = self.__compute_first_quadrant_coordinates()
    coordinates = self.__compute_reflect_coordinates(coordinates)
    return coordinates

  def get_count(self):
    '''
    Get the valid count. Driver of the app.
    '''

    coordinates = self.__get_coordinates()
    return self.__valid_count(coordinates)


def solution(dimensions, your_position, guard_position, distance):
  room = Room(dimensions, your_position, guard_position, distance)
  return room.get_count()


dimensions = [3, 2]
player = [1, 1]
guard = [2, 1]
distance = 4
assert solution(dimensions, player, guard, distance) == 7

dimensions = [300, 275]
player = [150, 150]
guard = [185, 100]
distance = 500
assert solution(dimensions, player, guard, distance) == 9
