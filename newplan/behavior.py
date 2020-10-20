class Behavior:
  def __init__(self, entity, on_run, times=None):
    self.entity = entity
    self.on_run = on_run
    self.times = times
  
  def run(self):
    if self.times is not None:
      self.times -= 1
    self.on_run(self.entity)
    if self.times <= 0:
      self.entity.behaviors.remove(self)
