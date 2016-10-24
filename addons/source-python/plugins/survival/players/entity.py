'''



'''

__all__ = ('Player', )

from player.entity import Player as _Player

from ..props import PropDictionary

#
#
#

class Player(_Player):
    "Extension of Player, to add prop management."

    def __init__(self, *args, **kwargs):
        "Initialization of the Player object."
        super().__init__(*args, **kwargs)
        # Add private attributes for later use in properties.
        self._props = PropDictionary(self)
        self._credits = int()

    @property
    def props(self):
        "Dictionary to manage all props owned by a player."
        return self._props
    
    @property
    def credits(self):
        "The amount of usable credits a player has."
        return self._credits

    @credits.setter
    def credits(self, value):
        "Set the amount of usable credits the player has. Cannot be below 0."
        # Is the credit new value less than 0?
        if value < 0:
            self._credits = 0
            # No need to go further.
            return

        self._credits = value