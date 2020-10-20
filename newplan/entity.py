from abc import ABC, abstractmethod 

class Entity(ABC):
  def __init__(self, game):
    self.state = game.state
    game.clock.subscribe(self)
    self.behaviors = set()

  @property
  def location(self):
    return self._location
  @location.setter
  def location(self, val):
    self.location.entities.remove(self)
    self._location = val
    self.location.entities.add(self)

  @property
  def description(self):
    return self.get_description_strategy()
  @description.setter
  def description(self):
    raise("Cannot edit description directly. Use get_description_strategy method.")

  def on_tick(self):
    for behavior in self.behaviors:
      behavior.run(self)

  @abstractmethod
  def get_description_strategy(self):
    pass
