from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Node(object):
    name: str
    parent: Optional["Node"] = None
    value: Optional = None
    _children: dict = field(init=False)

    def __post_init__(self):
        self._children = {}

    def add_child(self, child: "Node"):

        self._children[child.name] = child
        child._set_parent(self)

    def _set_parent(self, parent: "Node"):
        self.parent = parent

    def __getitem__(self, key):

        if key in self._children:
            if self._children[key].is_leaf:
                return self._children[key].value

            else:
                return self._children[key]

        else:
            raise RuntimeError("not one of my children")

    def __setitem__(self, key, value):

        if key in self._children:

            if self._children[key].is_leaf:

                self._children[key] = value

            else:

                raise RuntimeError("cannot set the value of a key!")

    @property
    def is_leaf(self):
        return len(self._children) == 0

    @property
    def is_root(self):
        return self.parent is None

    def _get_children(self):

        return [child for _, child in self._children.items()]

    def get_child_names(self):

        return [child for child, _ in self._children.items()]

    
    def __dir__(self):

        # Get the names of the attributes of the class
        l = list(self.__class__.__dict__.keys())

        # Get all the children
        l.extend([child.name for child in self._get_children()])

        return l

    def __getattribute__(self, name):


        try:
            if name in self._children:

                if self._children[name].is_leaf:
                    return self._children[name].value

                else:
                    return self._children[name]
            else:
                return super().__getattribute__(name)

        except:

            return super().__getattribute__(name)

    def __setattr__(self, name, value):

        # We cannot change a node
        # but if the node has a value
        # attribute, we want to call that

        if "_children" in self.__dict__:
            if name in self._children:

                if self._children[name].is_leaf:
                    self._children[name].value = value

                else:

                    raise RuntimeError("cannot set the value of a key!")

            else:
                return super().__setattr__(name, value)
        else:

            return super().__setattr__(name, value)
