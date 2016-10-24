'''



'''

__all__ = (
    'player_dictionary',
    'PlayerDictionary',
    'Player',
    )

from listeners import OnClientFullyConnect
from listeners import OnClientDisconnect

from .dictionary import PlayerDictionary
from .dictionary import player_dictionary
from .entity import Player

@OnClientFullyConnect
def init_player(index):
    "Create player instance upon joining."
    player = player_dictionary[index]

@OnClientDisconnect
def remove_player(index):
    "Remove player instance upon leaving."
    del player_dictionary[index]