'''



'''

__all__ = (
    'player_dictionary',
    'PlayerDictionary',
    )

from players.dictionary import PlayerDictionary

from .entity import Player

#
#
#

player_dictionary = PlayerDictionary(Player)