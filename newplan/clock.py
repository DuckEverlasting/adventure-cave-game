class clock:
  def __init__(self):
    self.time_passed = 0
    self.observers = set()
  
  def subscribe(self, entity):
    self.observers.add(entity)

  def unsubscribe(self, entity):
    self.observers.remove(entity)

  def tick(self):
    for entity in self.observers:
      entity.on_tick()
    self.time_passed += 1
