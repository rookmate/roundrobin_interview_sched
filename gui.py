from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox,
QFormLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QSpinBox, QVBoxLayout,
QFileDialog)
from PyQt5.QtCore import pyqtSlot

import sys

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
        self.file_selected = QLineEdit(self)
        self.file_button = QPushButton('File', self)
        self.int_per_cand = QSpinBox()
        self.int_per_cand.setValue(2)
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

        # Setup Google form
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        # Browse file button action
        self.file_button.clicked.connect(self.file_on_click)
        # Show GUI
        self.show()

    # TODO: Display info in a new textbox after pressing a button
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(gui.exec_())
