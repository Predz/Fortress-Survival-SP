'''



'''

__all__ = ('Prop', )

from entities.entity import Entity

#
#
#

class Prop(Entity):
    "Extension of Entity, to add prop management."

	@classmethod
    def create_prop(cls, name, owner, *, **kwargs):
        "Creates a prop entity, and stores owner and name. Accepts **kwargs for setattr."
        # Use the builtin create classmethod from Entity.
        instance = cls.create('prop_dynamic')
        # Store the name of the prop and owner.
        instance.name = name
        instance.owner = owner
        # Create the attributes for managing stats.
        instance.level = 1
        # Instantly define any attributes requested in kwargs.
        for key, value in kwargs:
            instance.__setattr__(key, value)
        # Return the instance (obviously...).
        return instance