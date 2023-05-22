import datetime
import math
import os
import platform
import shutil
import subprocess
import sys
from os import listdir
from os.path import isfile
from os.path import join
from typing import Iterable
from typing import Tuple

import os_identifier

from . import geometry

if os_identifier.is_windows:
    folder_save_file = desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    folder_documents = documents = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
else:
    folder_save_file = desktop = os.path.expanduser('~/Desktop/')
    folder_documents = documents = os.path.expanduser('~/Documents/')


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # for PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    return f'{os.getcwd()}/{relative_path.replace(".", "")}'


cwd = resource_path('src')

path_save = desktop

lines_intersect = geometry.lines_intersect
point_in_rectangle = geometry.point_in_rectangle
line_intersect_rectangle = geometry.line_intersect_rectangle
get_nearest_points = geometry.get_nearest_points
get_rectangle_edges = geometry.get_rectangle_edges


def remove_file(file_path):
    os.remove(file_path)


def remove_file_or_directory(path):
    if os.path.isfile(path):
        os.remove(path)
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)


def is_number(s):
    """ Returns True is string is a number. """
    try:
        float(s)
        return True
    except TypeError:
        return False
    except ValueError:
        return False


def convert_to_number_if_possible(s: str):
    if is_number(s):
        if '.' in s:
            return float(s)
        else:
            return int(s)
    elif s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        return s


def comma_separate_string_value(value, format_code: str = ''):
    value = str(value)
    if '.' in value:
        value = format(float(value), f',{format_code}')
    else:
        value = format(int(value), f',{format_code}')
    return value


def swap_tuple_data(destination: int, index_: int, data: tuple) -> tuple:
    total_datas = len(data)
    is_moving_up = destination <= index_
    mylist = list(data)

    if destination == -1:
        mylist += [mylist[index_]]
        del mylist[index_]
    elif is_moving_up:
        mylist.insert(destination, mylist[index_])
        del mylist[index_ + 1]
    else:
        if destination >= total_datas:
            mylist.insert(destination - total_datas, mylist[index_])
            del mylist[index_ + 1]
        else:
            mylist.insert(destination + 1, mylist[index_])
            del mylist[index_]
    return tuple(mylist)


def get_final_destinations_after_sorting(indexes: tuple, number_of_elements: int, shift: int) -> Tuple[tuple, tuple]:
    if (0 in indexes) and (shift < 0):  # Stop at the top
        new_destinations = indexes
    elif (number_of_elements - 1 in indexes) and (0 < shift):  # Stop at the bottom
        new_destinations = indexes
    else:
        new_destinations_list = []

        if shift > 0:
            indexes = tuple(reversed(indexes))

        for index_ in indexes:
            destination = index_ + shift
            if destination == -1:
                final_destination = number_of_elements - 1
            elif destination >= number_of_elements:
                final_destination = destination - number_of_elements
            elif destination < -1:
                final_destination = destination + 1
            else:
                final_destination = destination
            new_destinations_list.append(final_destination)

        new_destinations = tuple(new_destinations_list)
    return indexes, new_destinations


def move_tuple_element(existing_data_tuple: tuple, index_: int, destination: int) -> tuple:
    new_data_list = list(existing_data_tuple)
    if index_ < destination:
        new_data_list.insert(destination + 1, new_data_list[index_])
        del new_data_list[index_]
    elif destination < index_:
        new_data_list.insert(destination, new_data_list[index_])
        del new_data_list[index_ + 1]
    new_data = tuple(new_data_list)
    return new_data


def remove_item_from_tuple(existing_data, what_to_remove) -> tuple:
    new_data_list = []
    for a in existing_data:
        if a != what_to_remove:
            new_data_list.append(a)
    new_data = tuple(new_data_list)
    return new_data


def remove_item_from_tuple_by_index(existing_data, indexes):
    new_data_list = []
    for n, command in enumerate(existing_data):
        if n not in indexes:
            new_data_list.append(command)
    new_data = tuple(new_data_list)
    return new_data


def sort_lists(list_sorter, list_sorted) -> Tuple[list, list]:
    zipped_lists = zip(list_sorter, list_sorted)
    try:
        list_sorter_without_duplicate = [i + 0.0001 * n for (n, i) in enumerate(list_sorter)]
    except TypeError:
        list_sorter_without_duplicate = list_sorter

    try:
        sorted_pairs = sorted(zipped_lists)
    except TypeError:
        sorted_pairs = sorted(zip(list_sorter_without_duplicate, list_sorted))
    tuples = zip(*sorted_pairs)
    try:
        list_sorter, list_sorted = [list(tuple_) for tuple_ in tuples]
    except ValueError:
        list_sorter, list_sorted = [], []
    return list_sorter, list_sorted


def values_tuple_to_values_str(values, decimal: int = None):
    if values is None:
        return ''
    if decimal is not None:
        values = tuple(float(round(value, decimal)) for value in values)
    else:
        values = tuple(float(value) for value in values)
    return ','.join(str(values).split(',')).strip('(').strip(')')


def get_tuple_and_destinations_after_shifting_elements(existing_data_tuple, indexes, shift):
    number = len(existing_data_tuple)
    indexes_sorted, destinations = get_final_destinations_after_sorting(indexes, number, shift)
    new_data = existing_data_tuple
    for index_, destination in zip(indexes_sorted, destinations):
        new_data = move_tuple_element(existing_data_tuple, index_, destination)
        existing_data_tuple = new_data
    return destinations, new_data


def str_to_int(text, if_error) -> int:
    try:
        digits = int(text)
    except ValueError:
        digits = if_error
    return digits


def str_to_float(text, if_error) -> float:
    try:
        digits = float(text)
    except ValueError:
        digits = if_error
    return digits


def create_folder(path):
    try:
        os.mkdir(path)
        feedback = 'success'
    except FileExistsError:
        feedback = f'success'
    except OSError:
        feedback = f'Cannot create folder there! {path}'
    return feedback


def is_directory(path) -> bool:
    return os.path.isdir(path)


def create_tree_data(parent: str, index: str, text: str, values: tuple, tags: tuple, select: bool, id_=None,
                     foreground: str = False, background: str = False, strikethrough=False, underline=False, bold=False
                     ) -> dict:
    tree_data = {
        'parent': parent,
        'index': index,
        'text': text,
        'values': values,
        'tags': tags,
        'select_this_item': select
    }
    if id_ is not None:
        tree_data['id'] = id_
    if foreground:
        tree_data['foreground_color'] = foreground
    if background:
        tree_data['background_color'] = background
    if strikethrough:
        tree_data['strikethrough'] = strikethrough
    if underline:
        tree_data['underline'] = underline
    if bold:
        tree_data['weight'] = 'bold'
    return tree_data


def create_view_model_tree(headings: tuple, widths: tuple, tree_datas: Iterable, stretches: tuple, scroll_v: bool,
                           scroll_h: bool) -> dict:
    return {'tree_datas': tree_datas, 'headings': headings, 'widths': widths, 'stretches': stretches,
            'scroll_v': scroll_v, 'scroll_h': scroll_h, }


def get_two_digit_str_from_int(n: int) -> str:
    return f'0{n}' if n < 10 else f'{n}'


def get_files_in_the_folder(folder_path: str, specified_extension: str = '') -> Tuple[str, ...]:
    files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    if specified_extension:
        files = [f for f in files if f[-1 * len(specified_extension):] == specified_extension]
    return tuple(sorted(files))


def get_proper_path_depending_on_development_or_distribution(relative_path):
    possible_overlap = relative_path.split('/')[0]
    folder_path = os.path.join(sys.path[0], relative_path)
    if possible_overlap != '':
        folder_path = remove_overlap(folder_path, possible_overlap)
    if not (os.path.exists(folder_path)):
        folder_path = os.path.join(os.getcwd(), relative_path)
    if possible_overlap != '':
        folder_path = remove_overlap(folder_path, possible_overlap)
    return folder_path


def remove_overlap(folder_path, possible_overlap):
    return folder_path.replace(f'{possible_overlap}/{possible_overlap}', possible_overlap)


def time_delta_str_to_time_delta(time_expected_str) -> datetime.timedelta:
    if 'day' in time_expected_str:
        try:
            str_before_days, str_rest = time_expected_str.split('day,')
        except ValueError:
            str_before_days, str_rest = time_expected_str.split('days,')
    else:
        str_before_days = '0'
        str_rest = time_expected_str
    days = int(str_before_days)
    hours_str, minutes_str, seconds_str = str_rest.split(':')
    hours, minutes, seconds = int(hours_str), int(minutes_str), int(seconds_str)
    total_seconds = 60 * 60 * hours + 60 * minutes + seconds

    return datetime.timedelta(days, total_seconds)


def datetime_to_str(d: datetime.datetime):
    f = int_to_str
    due_date_str = f'{d.year}/{f(d.month)}/{f(d.day)} {f(d.hour)}:{f(d.minute)}'
    return due_date_str


def datetime_to_str_no_time(d: datetime.datetime):
    f = int_to_str
    due_date_str = f'{d.year}/{f(d.month)}/{f(d.day)}'
    return due_date_str


def str_to_date_time(datetime_str) -> datetime.datetime:
    year_str, month_str, day_time_str = datetime_str.replace('-', '/').split('/')
    try:
        day_str, time_str = day_time_str.split(' ')
    except ValueError:
        return str_to_date_time_no_time(datetime_str)
    if len(time_str.split(':')) == 3:
        hour_str, minute_str, seconds_str = time_str.split(':')
    else:
        hour_str, minute_str = time_str.split(':')
    year, month, day = int(year_str), int(month_str), int(day_str)
    hour, minute = int(hour_str), int(minute_str)
    return datetime.datetime(year, month, day, hour, minute)


def str_to_date_time_no_time(datetime_str) -> datetime.datetime:
    year_str, month_str, day_str = datetime_str.replace('-', '/').split('/')
    day_str = day_str.split(' ')[0]  # datetime_str may contain time information such as '2023-05-18 09:00:00'
    year, month, day = int(year_str), int(month_str), int(day_str)
    return datetime.datetime(year, month, day)


def int_to_str(i: int) -> str:
    return f'0{i}' if i < 10 else f'{i}'


def copy_to_clipboard(text: str):
    try:
        subprocess.run("pbcopy", universal_newlines=True, input=text)
    except FileNotFoundError:
        subprocess.run("pbcopy", universal_newlines=True, input=text, shell=True)


def round_decimals_up(number: float, decimals: int = 2):
    """
    Returns a value rounded up to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.ceil(number)

    factor = 10 ** decimals
    return math.ceil(number * factor) / factor


def round_decimals_down(number: float, decimals: int = 2):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor


def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])
