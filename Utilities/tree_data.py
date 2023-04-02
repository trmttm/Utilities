from typing import Callable

import Utilities


class TreeData:
    _key_name = 'names'
    _key_data = 'data'
    _key_selected = 'selected'

    def __init__(self):
        self._data = {
            self._key_name: [],
            self._key_data: [],
            self._key_selected: (),
        }

    @property
    def names(self) -> tuple:
        return tuple(self._data[self._key_name])

    @property
    def data(self) -> tuple:
        return tuple(self._data[self._key_data])

    def add_data(self, name, data):
        self._data[self._key_name].append(name)
        self._data[self._key_data].append(data)

    def get_name(self, n: int):
        name = self.names
        return name[n] if len(name) >= n + 1 else None

    def get_data(self, n: int):
        data = self.data
        return data[n] if len(data) >= n + 1 else None

    def remove_selected(self):
        for n in tuple(reversed(self.selected_indexes)):
            self.remove(n)

    def remove(self, n: int):
        self._remove(self._data[self._key_data], n)
        self._remove(self._data[self._key_name], n)
        adjust_selection_upon_removing_data(n, self.selected_indexes, self.select_data_by_indexes)

    @staticmethod
    def _remove(list_passed: list, n: int):
        try:
            del list_passed[n]
        except IndexError:
            pass

    def select_data_by_indexes(self, indexes: tuple):
        verified_index = tuple(verified for verified in indexes if (0 <= verified <= len(self.names) - 1))
        self._data[self._key_selected] = verified_index

    def unselect_data_by_indexes(self, indexes: tuple):
        self._data[self._key_selected] = tuple(i for i in self.selected_indexes if i not in indexes)

    @property
    def selected_indexes(self) -> tuple:
        return self._data[self._key_selected]

    @property
    def selected_names(self) -> tuple:
        return tuple(d for (n, d) in enumerate(self.names) if n in self.selected_indexes)

    @property
    def selected_datas(self) -> tuple:
        return tuple(d for (n, d) in enumerate(self.data) if n in self.selected_indexes)

    def sort_data(self, shift: int):
        sort = Utilities.get_tuple_and_destinations_after_shifting_elements
        _, sorted_names = sort(self.names, self.selected_indexes, shift)
        destinations, sorted_data = sort(self.data, self.selected_indexes, shift)
        self._data[self._key_name] = list(sorted_names)
        self._data[self._key_data] = list(sorted_data)
        self.select_data_by_indexes(destinations)

    @property
    def state(self) -> dict:
        return self._data

    def set_state(self, state):
        self._data = state


def adjust_selection_upon_removing_data(n: int, initial_selection: tuple, select_by_idexes: Callable):
    new_selected_indexes = []
    for selected_n in initial_selection:
        if selected_n < n:
            new_selected_indexes.append(selected_n)
        elif selected_n == n:
            if selected_n > 0:
                new_selected_indexes.append(selected_n - 1)
        else:
            new_selected_indexes.append(selected_n - 1)

    if len(new_selected_indexes) > 0:
        next_indexes = min(new_selected_indexes),
    else:
        next_indexes = 0,
    select_by_idexes(next_indexes)
