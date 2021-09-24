# Dimension
# Jacob Miske

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtTest import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import sys
import time
import csv


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.experiment_counter_1 = 0
        self.experiment_counter_2 = 0
        self.experiment_settings_path = None
        self.experiment_save_path = None
        self.experiment_in_progress = False
        self.all_devices_serial_numbers = []

        def get_emergency_stop():
            group_box = QGroupBox("Emergency Stop")
            status_text0 = QLabel('Set output levels to zero')
            button0 = QPushButton('Emergency Stop')
            button0.clicked.connect(self.e_stop)
            vbox = QtWidgets.QVBoxLayout()
            vbox.addWidget(status_text0)
            vbox.addWidget(button0)
            vbox.addStretch(1)
            group_box.setLayout(vbox)
            # group_box.setFixedWidth(300)
            return group_box, button0

        def get_HV_safety_1():
            group_box = QGroupBox("Device 1 HV Safety")
            radio1 = QRadioButton("HV Disabled")
            radio2 = QRadioButton("POSITIVE HV Enabled")
            radio3 = QRadioButton("NEGATIVE HV Enabled")
            # Start device 1 HV as disabled
            radio1.setChecked(True)
            radio1.clicked.connect(lambda: self.radio_1(r=radio1))
            radio2.clicked.connect(lambda: self.radio_2(r=radio2))
            radio3.clicked.connect(lambda: self.radio_3(r=radio3))
            vbox = QtWidgets.QVBoxLayout()
            vbox.addWidget(radio1)
            vbox.addWidget(radio2)
            vbox.addWidget(radio3)
            vbox.addStretch(1)
            group_box.setLayout(vbox)
            # group_box.setFixedWidth(300)
            return group_box, radio1, radio2, radio3

        def get_HV_safety_2():
            group_box = QGroupBox("Device 2 HV Safety")
            radio4 = QRadioButton("HV Disabled")
            radio5 = QRadioButton("POSITIVE HV Enabled")
            radio6 = QRadioButton("NEGATIVE HV Enabled")
            # Start device 2 HV as disabled
            radio4.setChecked(True)
            radio4.clicked.connect(lambda: self.radio_4(r=radio4))
            radio5.clicked.connect(lambda: self.radio_5(r=radio5))
            radio6.clicked.connect(lambda: self.radio_6(r=radio6))
            vbox = QtWidgets.QVBoxLayout()
            vbox.addWidget(radio4)
            vbox.addWidget(radio5)
            vbox.addWidget(radio6)
            vbox.addStretch(1)
            group_box.setLayout(vbox)
            # group_box.setFixedWidth(300)
            return group_box, radio4, radio5, radio6

        def get_exp_run_widget():
            group_box = QGroupBox("Experiment Automation")
            status_text0 = QLabel('Load Experiment File')
            button0 = QPushButton('Load')
            button0.clicked.connect(self.openFileNameDialog)
            status_text1 = QLabel('Experiment Settings File')
            status_text2 = QLabel(self)
            button1 = QPushButton('Start Experiment')
            button1.clicked.connect(self.on_click_experiment)
            vbox = QtWidgets.QVBoxLayout()
            vbox.addWidget(status_text0)
            vbox.addWidget(button0)
            vbox.addWidget(status_text1)
            vbox.addWidget(status_text2)
            vbox.addWidget(button1)
            vbox.addStretch(1)
            group_box.setLayout(vbox)
            # group_box.setFixedWidth(400)
            return group_box, button0, status_text2, button1 #float1, float2, float3, float4, float5, float6, button1

        def get_plot_win_1():
            # Create Widget
            group_box = QGroupBox("Device 1")
            return group_box

        def get_save_and_clear_data():
            # Create Widget
            group_box = QGroupBox("Save and Clear Data")
            filename_text = QLabel('Output File Name')
            filename_entry = QLineEdit("FileName")
            status_text0 = QLabel('Output data header')
            info_entry = QLineEdit("Experimental details")
            button2 = QPushButton('Save All Results')
            button2.clicked.connect(self.on_click_save)
            status_text5 = QLabel('Clear Results')
            button3 = QPushButton('Clear 1')
            button3.clicked.connect(self.on_click_clear_1)
            button4 = QPushButton('Clear 2')
            button4.clicked.connect(self.on_click_clear_2)
            # Create VBox
            vbox = QtWidgets.QVBoxLayout()
            vbox.addWidget(filename_text)
            vbox.addWidget(filename_entry)
            vbox.addWidget(status_text0)
            vbox.addWidget(info_entry)
            vbox.addWidget(button2)
            vbox.addWidget(status_text5)
            vbox.addWidget(button3)
            vbox.addWidget(button4)
            vbox.addStretch(1)
            group_box.setLayout(vbox)
            # group_box.setFixedWidth(300)
            return group_box, info_entry, filename_entry

        def get_level_and_current():
            group_box = QGroupBox("Output")
            status_text1 = QLabel('Item 1')
            level_text1 = QLabel('Value 1')
            level_value1 = QLCDNumber()
            level_value1.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
            current_text1 = QLabel('Value 2')
            current_value1 = QLCDNumber()
            current_value1.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
            status_text2 = QLabel('Item 2')
            level_text2 = QLabel('Item 1')
            level_value2 = QLCDNumber()
            level_value2.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
            current_text2 = QLabel('Item 2')
            current_value2 = QLCDNumber()
            current_value2.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
            vbox = QtWidgets.QVBoxLayout()
            vbox.addWidget(status_text1)
            vbox.addWidget(level_text1)
            vbox.addWidget(level_value1)
            vbox.addWidget(current_text1)
            vbox.addWidget(current_value1)
            vbox.addWidget(status_text2)
            vbox.addWidget(level_text2)
            vbox.addWidget(level_value2)
            vbox.addWidget(current_text2)
            vbox.addWidget(current_value2)
            vbox.addStretch(1)
            group_box.setLayout(vbox)
            # group_box.setFixedWidth(300)
            return group_box, level_value1, current_value1, level_value2, current_value2

        def get_float_value():
            # Create Widget
            group_box = QGroupBox("Settings")
            status_text1 = QLabel('Item 1 Set')
            float1 = QLineEdit("0")
            button0 = QPushButton('Change Item')
            button0.clicked.connect(self.on_click_level_1)
            status_text2 = QLabel('Item 2  Set')
            float2 = QLineEdit("0")
            button1 = QPushButton('Change Item')
            button1.clicked.connect(self.on_click_level_2)
            # Create VBox
            vbox = QtWidgets.QVBoxLayout()
            vbox.addWidget(status_text1)
            vbox.addWidget(float1)
            vbox.addWidget(button0)
            vbox.addWidget(status_text2)
            vbox.addWidget(float2)
            vbox.addWidget(button1)
            vbox.addStretch(1)
            group_box.setLayout(vbox)
            # group_box.setFixedWidth(400)
            return group_box, float1, button0, float2, button1

        def get_plot_win_2():
            # Create Widget
            group_box = QGroupBox("Device 2")
            return group_box

        def get_graphics():
            # Create Widget
            group_box = QGroupBox("Graphics")
            status_text1 = QLabel('Device 1')
            cb1 = QComboBox()
            cb1.addItems(self.all_devices_serial_numbers)
            cb1.currentIndexChanged.connect(self.selection_change_1)
            status_text2 = QLabel('Device 2')
            cb2 = QComboBox()
            cb2.addItems(self.all_devices_serial_numbers)
            cb2.currentIndexChanged.connect(self.selection_change_2)
            # Create VBox
            vbox = QtWidgets.QVBoxLayout()
            vbox.addWidget(status_text1)
            vbox.addWidget(cb1)
            vbox.addWidget(status_text2)
            vbox.addWidget(cb2)
            vbox.addStretch(1)
            group_box.setLayout(vbox)
            # group_box.setFixedWidth(300)
            return group_box, cb1, cb2

        # Highest level layout object
        layout = QtWidgets.QVBoxLayout()
        # Grid out the components
        sublayout1 = QtWidgets.QVBoxLayout()
        sublayout2 = QtWidgets.QVBoxLayout()
        sublayout4 = QtWidgets.QVBoxLayout()
        sublayout5 = QtWidgets.QVBoxLayout()
        sublayout6 = QtWidgets.QVBoxLayout()
        sublayout8 = QtWidgets.QVBoxLayout()
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addLayout(sublayout1, 1)
        top_layout.addLayout(sublayout2, 2)
        mid_layout = QtWidgets.QHBoxLayout()
        mid_layout.addLayout(sublayout4, 4)
        mid_layout.addLayout(sublayout8, 4)
        bottom_layout = QtWidgets.QHBoxLayout()
        bottom_layout.addLayout(sublayout5, 1)
        bottom_layout.addLayout(sublayout6, 2)
        layout.addLayout(top_layout)
        layout.addLayout(mid_layout)
        layout.addLayout(bottom_layout)

        # Sections of application
        self.editor = QPlainTextEdit()  # Could also use a QTextEdit and set self.editor.setAcceptRichText(False)
        self.e_stop_button, self.e_stop_button_widget = get_emergency_stop()
        self.HV_radio_buttons_1, self.r1, self.r2, self.r3 = get_HV_safety_1()
        self.HV_radio_buttons_2, self.r4, self.r5, self.r6 = get_HV_safety_2()
        self.save_and_clear, self.info_header, self.save_filename = get_save_and_clear_data()
        self.item_output, self.level_value1, self.current_value1, self.level_value2, self.current_value2 = get_level_and_current()
        self.automation, self.open_button, self.text_exp_settings_path, self.exp_button = get_exp_run_widget() 
        self.float_input, self.level_set_value_1, self.level_set_button_1, self.level_set_value_2, self.level_set_button_2 = get_float_value()
        self.graphics, self.cb1, self.cb2 = get_graphics()

        # Setup the QTextEdit editor configuration (deprecated)
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        # change button
        # TODO: make larger, read docs
        self.e_stop_button_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding)
        self.e_stop_button_widget.resize(150, 50)

        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

        # Add widgets
        sublayout1.addWidget(self.e_stop_button)
        sublayout2.addWidget(self.automation)
        sublayout4.addWidget(self.save_and_clear)
        sublayout5.addWidget(self.item_output)
        sublayout6.addWidget(self.float_input)
        sublayout8.addWidget(self.graphics)
        sublayout8.addStretch()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.update_title()
        self.resize(1140, 760)
        self.show()

        def create_file_toolbar():
            file_toolbar = QToolBar("File")
            file_toolbar.setIconSize(QSize(14, 14))
            self.addToolBar(file_toolbar)
            file_menu = self.menuBar().addMenu("&File")

            open_file_action = QAction(QIcon(os.path.join('images', 'question.png')), "Settings", self)

            open_file_action.setStatusTip("Settings")
            open_file_action.triggered.connect(self.file_open)
            file_menu.addAction(open_file_action)
            file_toolbar.addAction(open_file_action)

            save_file_action = QAction(QIcon(os.path.join('images', 'disk.png')), "Save", self)
            save_file_action.setStatusTip("Save current page")
            save_file_action.triggered.connect(self.file_save)
            file_menu.addAction(save_file_action)
            file_toolbar.addAction(save_file_action)

            saveas_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save As...", self)
            saveas_file_action.setStatusTip("Save current page to specified file")
            saveas_file_action.triggered.connect(self.file_saveas)
            file_menu.addAction(saveas_file_action)
            file_toolbar.addAction(saveas_file_action)

        create_file_toolbar()

    def update(self):
        print("System Timer")
        print(round(time.time()))
        # subsection 1

    @pyqtSlot()
    def on_click_level_1(self):
        print('level Change Button 1')
        print("level: " + self.level_set_value_1.text())
        if self.r1.isChecked():
            print("item 1 Disabled, no change")
        elif self.r2.isChecked():
            if (float(self.level_set_value_1.text()) > 10000.0) | (float(self.level_set_value_1.text()) < 0.0):
                print("out of bounds level!")
                self.dialog_critical(s="Out of bounds level! ")
                return -1
            
        elif self.r3.isChecked():
            if (float(self.level_set_value_1.text()) > 0.0) | (float(self.level_set_value_1.text()) < -10000.0):
                print("out of bounds level!")
                self.dialog_critical(s="Out of bounds level!")
                return -1

    @pyqtSlot()
    def on_click_level_2(self):
        print('Level Change Button 2')
        print("level: " + self.level_set_value_2.text())
        if self.r4.isChecked():
            print("item 2 Disabled, no change")
        elif self.r5.isChecked():
            if (float(self.level_set_value_2.text()) > 10000.0) | (float(self.level_set_value_2.text()) < 0.0):
                print("out of bounds level!")
                self.dialog_critical(s="Out of bounds level! ")
                return -1
        elif self.r6.isChecked():
            if (float(self.level_set_value_2.text()) > 0.0) | (float(self.level_set_value_2.text()) < -10000.0):
                print("out of bounds level!")
                self.dialog_critical(s="Out of bounds level! ")
                return -1

    @pyqtSlot()
    def on_click_experiment(self):
        print('level Change Button 1')    

    @pyqtSlot()
    def on_click_save(self):
        print('Save button clicked')
        with open('./{}.csv'.format(self.save_filename.text()), mode='w') as outfile:
            outfile_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            outfile_writer.writerow(["V-I Measurements", str(time.time())])
            outfile_writer.writerow([str(self.info_header.text())])

    @pyqtSlot()
    def on_click_clear_1(self):
        print('Clearing data for item 1')

    @pyqtSlot()
    def on_click_clear_2(self):
        print('Clearing data for device 2')


    @pyqtSlot()
    def radio_1(self, r):
        # HV disabled
        if self.r1.isChecked():
            print("Device 1 HV disabled")
            QTest.qWait(500)


    @pyqtSlot()
    def radio_2(self, r):
        # HV positive enabled
        if self.r2.isChecked():
            # Both disabled, need to enable
            print("Device 1 HV Positive enabled")
            QTest.qWait(500)

    @pyqtSlot()
    def radio_3(self, r):
        # HV negative enabled
        if self.r3.isChecked():
            # Both disabled, need to enable
            print("Device 1 HV Negative enabled")
            QTest.qWait(500)

    @pyqtSlot()
    def radio_4(self, r):
        # HV negative enabled
        if self.r4.isChecked():
            # Both disabled, need to enable
            print("Device 2 HV disabled")
            QTest.qWait(500)

    @pyqtSlot()
    def radio_5(self, r):
        if self.r5.isChecked():
            # Both disabled, need to enable
            print("Device 2 HV Positive enabled")
            QTest.qWait(500)

    @pyqtSlot()
    def radio_6(self, r):
        if self.r6.isChecked():
            # Both disabled, need to enable
            print("Device 2 HV Negative enabled")
            QTest.qWait(500)

    @pyqtSlot()
    def selection_change_1(self):
        # Changing device 1
        print("device 1")

    @pyqtSlot()
    def selection_change_2(self):
        # Changing device 2
        print("device 2")

    @pyqtSlot()
    def e_stop(self):
        # TODO: finish e stop function
        print("e stop pressed")
        quit()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_open(self):
        self.dialog_critical(s="See README.txt in ")

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open a HV Experiment File", "", "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.experiment_settings_path = fileName

    def file_save(self):
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()

        self._save_to_path(self.path)

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt);All files (*.*)")

        if not path:
            # If dialog is cancelled, will return ''
            return

        self._save_to_path(path)

    def _save_to_path(self, path):
        text = self.editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.update_title()

    def update_title(self):
        self.setWindowTitle("Dimension")

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Dimension")
    app_icon = QtGui.QIcon()
    app_icon.addFile('arrow-continue.png')
    app.setWindowIcon(app_icon)
    window = MainWindow()
    app.exec_()