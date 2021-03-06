import sys, pygame

class DisplayEngine(object):

  def __init__(self, resolution, depth=0, **flags):
    """
      Create the main display surface
    """

    try:
      pygame.init()

      pygame.display.set_caption('PyFrogger')

      # Create the display layers that we will need
      self.DisplayLayers = pygame.sprite.LayeredDirty()

      # Create a layer for maintaining player sprite groups
      self.PlayerDisplayLayers = pygame.sprite.LayeredDirty()

      # Create a list to hold all of the entities so we can execute their respond methods
      self.DisplayEntities = []

      # Create a list to hold all user controlled entities
      self.ControlledEntities = []

      # We are not using flags right now so just default flags to 0
      if len(flags) == 0:
        displayFlags = 0

      # Set the depth, should automatically default to current desktop
      intDepth = depth

      # Create the main display surface
      self.displaySurface = pygame.display.set_mode(
        (resolution[0], resolution[1]),
        displayFlags,
        intDepth
      )

      self.clock = pygame.time.Clock()

      self.States = {
        
        "freeze"  : False
      }
    except StandardError as Error:
      print Error

  def addUserControlledLayer(self, entLayer):
    groupLayer = pygame.sprite.Group(entLayer)
    self.PlayerDisplayLayers.add(groupLayer)
    self.ControlledEntities.append(entLayer)

  def addGameController(self, controller):
    self.ControlledEntities.append(controller)

  def addLayer(self, entLayer):
    """ Add a layer to the rendering engine """
    if isinstance(entLayer, list):
      for entity in entLayer:
        groupLayer = pygame.sprite.Group(entity)
        self.DisplayLayers.add(groupLayer)
    else:
      groupLayer = pygame.sprite.Group(entLayer)
      self.DisplayLayers.add(groupLayer)
      self.DisplayEntities.append(entLayer)

  def updateDisplay(self):
    """
      This method is responsible for constantly updating the main display surface.
      It also draws anything in the DisplayLayers layer to the screen in the order in which they were added
      Then we update only the updated layers, not the entire screen
    """
    if self.States['freeze'] == False:
      self.DisplayLayers.update()
      self.PlayerDisplayLayers.update()
      self.animate()

    self.respond()

    pygame.display.update()

    self.clock.tick(80)

  def setFreezeState(self, boolState):
    self.States['freeze'] = bool(boolState)

  def respond(self):
    for event in pygame.event.get():
      for entity in self.ControlledEntities:
        entity.respond(event)

  def animate(self):
    for entity in self.DisplayEntities:
      entity.animate()

  @property
  def Frog(self):
    return self.ControlledEntities[0]

  @property
  def Surface(self):
    return self.displaySurface
