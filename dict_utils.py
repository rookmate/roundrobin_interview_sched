import gui
import sys
import roundrobin
import collections

from PyQt5.QtWidgets import QApplication


def reverse_dict(d):
    reversed_dict = collections.defaultdict(list)
    for key, values in d.items():
        for value in values:
            reversed_dict[value].append(key)
    return reversed_dict


def get_keys_by_value(d, value_to_find):
    keys = list()
    for key, values in d.items():
        if value_to_find in values:
            keys.append(key)
    return  keys


def clean_empty_lists(d):
    clean_d = {}
    for key, value in d.items():
        if not value:
            continue
        clean_d[key] = d[key]
    return clean_d


def clean_repeated_pairs(d):
    clean_d = {}
    aux_d = d.copy()
    # find shortest list that contains a specific pair
    # delete all the identical pairs in the other keys
    while clean_d.keys() < d.keys():
        shortest_key = ''
        shortest_values = 0
        for key, values in aux_d.items():
            if shortest_key == '':
                shortest_key = key
                shortest_values = len(values)
                continue
            if len(values) >= shortest_values:
                continue
            shortest_key = key
            shortest_values = len(values)

        # Delete duplicates from all other keys
        for value in aux_d[shortest_key]:
            keys = get_keys_by_value(aux_d, value)
            for key in keys:
                if key == shortest_key:
                    continue
                values = aux_d[key]
                values.remove(value)
                aux_d[key] = values
        clean_d[shortest_key] = aux_d[shortest_key]
        del aux_d[shortest_key]

    clean_d = clean_empty_lists(clean_d)
    return clean_d


def dict_to_string(d):
    str_dict = ""
    for key in sorted(d):
        str_dict = str_dict + key + "\t|\t" + str(d[key]) + "\n"
    return str_dict


if __name__ == '__main__':
    doodle = roundrobin.Doodle("Doodle.xls", 2)
    doodle.get_cal_robin_dict()
    robin_cal_by_date = reverse_dict(doodle.robin_cal)
    robin_cal_by_date_clean = clean_repeated_pairs(robin_cal_by_date)
    print(dict_to_string(robin_cal_by_date))
