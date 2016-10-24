'''



'''

__all__ = ('Turret', )

from engines.trace import engine_trace
from engines.trace import ContentMasks
from engines.trace import GameTrace
from engines.trace import Ray
from engines.trace import TraceFilterSimple
from filters.players import PlayerIter
from listeners import on_tick_listener_manager

from .entity import Prop

from time import time

#
#
#

class Turret(Prop):
    "Extensions of Prop, to add turret intelligence."

    # All intelligence, and damage management.
    tick_manager = on_tick_listener_manager
    last_fired = time()
    delay = 2
    ammunition = 200
    damage = 50

    def __init__(self, index):
        super(Prop, self).__init__(index)

        self.tick_manager.register_listener(self._tick)

    def _tick(self):
        "Generic intelligence handling for turrets. Do not override!"
        # Check the turret firstly has ammunition. If not then stop.
        if self.ammunition == 0:
            return

        # Should the turret be able to fire? If not then just delay.
        next_fire = self.last_fired + self.delay
        if next_fire > time():
            return

        # Try and find a local enemy, that we have vision on. If not then just delay again.
        enemy = self.get_closest_enemy()
        if not enemy:
            return

        # Cause the damage, and all changes to the turret.
        enemy.take_damage(self.damage, attacker_index=self.owner.index)
        self.last_fired = time()
        self.ammunition -= 1

        # To be implemented.
        self.animate()


    # Storing trace masks and filters for checking obstructions.
    mask = ContentMasks.ALL
    trace_filter = TraceFilterSimple()
    
    def get_ray(self, vector):
        "Returns a game engine ray between the turrets aim and the target <Vector>."
        return Ray(self.origin, vector)

    def can_see_location(self, vector):
        "Checks to see if the turret can see the <Vector> provided."
        trace = GameTrace()
        engine_trace.trace_ray(self.get_ray(vector), self.mask, self.trace_filter, trace)
        return not trace.did_hit()

    def can_see_entity(self, entity):
        "Checks to see if the turret can see the <Entity> provided."
        return self.can_see_location(entity.origin)


    # Setting defaults for targetting enemies.
    target = "t"
    radius = 350

    def get_surrounding_enemies(self):
        "Returns a list of all surrounding targets."
        return [player for player in PlayerIter(self.target)
            if self.origin.get_distance(player.origin) <= self.radius and
            self.can_see_entity(player)]

    def get_closest_enemy(self):
        "Returns the <Player> instance of the closest enemy."
        enemies = self.get_surrounding_enemies()
        if len(enemies) == 0:
            return None
        return sorted(enemies, key=lambda x: self.origin.get_distance(x.origin))[0]


    # Animation (TBC)
    def animate(self):
        "Not currently implemented."