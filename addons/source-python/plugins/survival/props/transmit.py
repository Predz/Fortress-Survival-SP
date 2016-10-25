'''



'''

__all__ = ('no_transmit_indexes', )

from entities import CheckTransmitInfo
from entities.helpers import index_from_edict
from entities.helpers import index_from_pointer
from entities.hooks import EntityCondition
from entities.hooks import EntityPreHook
from memory import make_object
from players.entity import Player
from players.teams import teams_by_number

#
#
#

no_transmit_indexes = set()

entity_condition = EntityCondition.equals_entity_classname('prop_dynamic')

@EntityPreHook(entity_condition, 'set_transmit')
def pre_set_transmit(args):
    index = index_from_pointer(args[0])
    edict = make_object(CheckTransmitInfo, args[1]).client
    player = Player(index_from_edict(edict))

    if index in no_transmit_indexes:
        if teams_by_number[player.team] == "t":
            return False