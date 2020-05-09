from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox,
QFormLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QSpinBox, QVBoxLayout,
QFileDialog, QMessageBox, QMainWindow)
from PyQt5.QtCore import pyqtSlot

import os
import sys
import dict_utils
import roundrobin


class LargeMessageBox(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Round Robin unbiased interviewers'
        self.left = 10
        self.top = 10
        self.width = 1280
        self.height = 720
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(1240, 680)
        # TODO: get the text to be displayed multiline


class Gui(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self):
        super(Gui, self).__init__()
        self.title = 'Round Robin unbiased interviewers'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 180
        self.file = ""
        self.file_selected = QLineEdit(self)
        self.file_button = QPushButton('File', self)
        self.calc_button = QPushButton('Calculate', self)
        self.calc_title = "Roundrobin calculations"
        self.calc_data = "No data provided"
        self.int_per_cand = QSpinBox()
        self.int_per_cand.setValue(2)
        self.diag_textbox = LargeMessageBox()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Create Form
        self.createFormGroupBox()
        # Setup open and close buttons
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        # Setup Layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.calc_button)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        # Browse file button action
        self.file_button.clicked.connect(self.file_on_click)
        # Calculate results button action
        self.calc_button.clicked.connect(self.calculate_on_click)

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Requirements")
        layout = QFormLayout()
        layout.addRow(QLabel("Interviewers per candidate:"), self.int_per_cand)
        layout.addRow(QLabel("Browse directory:"), self.file_button)
        layout.addRow(QLabel("File selected:"), self.file_selected)
        self.formGroupBox.setLayout(layout)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.file = fileName
            self.file_selected.setText(fileName)

    @pyqtSlot()
    def file_on_click(self):
        self.openFileNameDialog()

    def calculate_roundrobin(self):
        doodle = roundrobin.Doodle(self.file, self.int_per_cand.value())
        doodle.get_cal_robin_dict()
        # Gets the round robin calendar sorted by date
        cal_by_date = dict_utils.reverse_dict(doodle.robin_cal)
        cal_by_data = dict_utils.clean_repeated_pairs(cal_by_date)
        self.calc_data = dict_utils.dict_to_string(cal_by_date)

    @pyqtSlot()
    def calculate_on_click(self):
        if os.path.isfile(self.file):
            self.calculate_roundrobin()
            self.diag_textbox.textbox.setText(self.calc_data)
            self.diag_textbox.show()
        else:
            QMessageBox.warning(self, self.calc_title, self.calc_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Gui()
    gui.show()
    sys.exit(app.exec_())
