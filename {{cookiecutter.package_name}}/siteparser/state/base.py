# -*- coding: utf-8 -*-
from copy import deepcopy


class State(object):

    def __init__(self):
        self.data = {}

    def _copy_to(self, other):
        other.data = deepcopy(self.data)

    def clone(self):
        state = self.__class__()
        self._copy_to(state)
        return state
