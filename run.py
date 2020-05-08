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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = gui.Gui()
    gui.exec_()

    doodle = roundrobin.Doodle(gui.file, gui.int_per_cand.value())
    doodle.get_cal_robin_dict()
    robin_cal_by_date = reverse_dict(doodle.robin_cal)
    # TODO: Find a pretty way to display this info
    for key in sorted(robin_cal_by_date):
        print (key, robin_cal_by_date[key])
    # Number of Candidates
    num_candidates = gui.num_candidates.value()
