'''



'''

__all__ = ('PropDictionary', )

from listeners import OnEntityDeleted

from .entity import Prop
from .transmit import no_transmit_indexes

#
#
#

class DeletionHandler(type):
    dictionaries = list()

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        cls.dictionaries.append(instance)
        return instance

class PropDictionary(dict, metaclass=DeletionHandler):
    "Dictionary to manage all props owned by a player."

    def __init__(self, owner, *args, **kwargs):
        "Initialize the helper dictionary."
        # Initialize python's built in dictionary.
        super().__init__(*args, **kwargs)
        # Store the owner which we use to define the props owners later.
        self.owner = owner

    def __missing__(self, name):
        "Call if item is missing from the dictionary."
        # Create the prop if non-existant.
        instance = self[name] = Prop.create_prop(name, self.owner)
        no_transmit_indexes.add(instance.index)
        return instance

    def __delitem__(self, name):
        "Delete item from the dictionary if existant."
        # No point to delete if not existant.
        if name not in self:
            return
        no_transmit_indexes.discard(self[name].index)
        super().__delitem__(name)

    def find_key_by_index(self, index):
        "Find an item from dictionary by their index."
        for instance in self.values():
            if instance.index == index:
                return instance.name
        return None

#
#
#

@OnEntityDeleted
def listener_on_entity_deleted(base_entity):
    if not base_entity.is_networked():
        return

    for prop_dictionary in DeletionHandler.dictionaries:
        name = prop_dictionary.find_key_by_index(base_entity.index)
        if name is None:
            continue
 
        del prop_dictionary[name]
        break