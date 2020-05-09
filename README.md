# Unbiased interview scheduler using round robin to appoint interviewers
Theis short project came into fruition after a friend asked me how to quickly setup the Doodle availabilities of all the company interviewers in a way that every two interviewers would only match once when interviewing candidate.

The thought process was:
1) Based on a tournament round robin;
1) Afterwards, the availabilities of each pair of interviewers was matched with their availabilities to get the valid pairs;
1) Cleaned up repeating pairs giving priority to the slots with the least available interviewers to maximize the amount of available pairs.

## Setup libraries
You need to install:
- Python package installer

`sudo apt install python-pip`
- PyQt5

`sudo apt-get install python3-pyqt5;
apt-get install python3-pyqtgraph`
- pandas

`pip3 install pandas xlrd`

## Running the code
If you clone the repository run the files by running:

`python3 <path to script>/gui.py`
