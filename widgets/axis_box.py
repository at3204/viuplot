from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QDoubleSpinBox, QSpinBox,
    QGridLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QScrollArea, QTreeWidget, 
    QTreeWidgetItem, QTabWidget, QWidget, QLabel, QComboBox, QCheckBox, QApplication,
    QLineEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect, Qt
from functools import partial

class AxisBox(QGroupBox):
    def __init__(self, axis, df):
        
        super().__init__()
        font = QFont()
        font.setPointSize(14)
        self.setFont(font)

        # row 1
        self.column_label = QLabel(self)
        self.column_label.setGeometry(QRect(15, 44, 48, 16))

        self.column = QComboBox(self)
        self.column.setGeometry(QRect(118, 42, 251, 26))
        self.addColToComBox(self.column, df)

        self.setTitle(axis+" axis")
        self.column_label.setText("column:")

    def addColToComBox(self, comboBox, df):
        for column in list(df.columns):
            comboBox.addItem(column)

    def checkBoxChangedAction(self, state, widgets):
        if (Qt.Checked == state):
            for widget in widgets:
                widget.setEnabled(True)
        else:
            for widget in widgets:
                widget.setEnabled(False)

    def getCurrentInfo(self):
        info = {}
        info['column'] = self.column.currentText()

        return info



class AxisBox_log_range(AxisBox):
    def __init__(self, axis, df):
        AxisBox.__init__(self, axis, df)

        # row 2
        self.fixed_range_checkBox = QCheckBox(self)
        self.fixed_range_checkBox.setGeometry(QRect(13, 124, 93, 20))

        self.range_min = QDoubleSpinBox(self)
        self.range_min.setGeometry(QRect(121, 124, 68, 24))
        self.range_min.setMaximum(float('inf'))
        self.range_max = QDoubleSpinBox(self)
        self.range_max.setGeometry(QRect(268, 124, 68, 24))
        self.range_max.setMaximum(float('inf'))

        self.range_min.setEnabled(False)
        self.range_max.setEnabled(False)

        self.fixed_range_checkBox.stateChanged.connect(
            partial(self.checkBoxChangedAction, 
                    widgets = [self.range_min, self.range_max]
            )
        )

        # row 2
        self.log_checkbox = QCheckBox(self)
        self.log_checkbox.setGeometry(QRect(13, 85, 82, 20))

        self.log_checkbox.setText("log-scale")
        self.fixed_range_checkBox.setText("fixed range")

    def getCurrentInfo(self):
        info = super().getCurrentInfo()
        info['log'] = self.log_checkbox.isChecked()
        if self.fixed_range_checkBox.isChecked():
            info['range'] = [self.range_min.value(), self.range_max.value()]
        else:
            info['range'] = None

        return info

class AxisBox_log_range_err(AxisBox_log_range):
    def __init__(self, axis, df):
        AxisBox_log_range.__init__(self, axis, df)

        # row 4
        self.error_checkbox = QCheckBox(self)
        self.error_checkbox.setGeometry(QRect(13, 169, 79, 20))

        self.error_setting = QComboBox(self)
        self.error_setting.setGeometry(QRect(118, 169, 91, 26))

        self.error = QComboBox(self)
        self.error.setGeometry(QRect(218, 169, 151, 26))
        self.addColToComBox(self.error, df)

        self.error_setting.setEnabled(False)
        self.error.setEnabled(False)
        self.error_setting.addItem("one side")
        self.error_setting.addItem("both side")

        self.error_checkbox.stateChanged.connect(
            partial(self.checkBoxChangedAction, 
                    widgets = [self.error_setting, self.error]
            )
        )

        self.error_checkbox.setText("error bar")
    
    def getCurrentInfo(self):
        info = super().getCurrentInfo()

        if self.error_checkbox.isChecked():
            if self.error_setting.currentText() == "one side":
                info['error'] = self.error.currentText()
                info['error_minus'] = None
            elif self.error_setting.currentText() == "both side":
                info['error'] = self.error.currentText()
                info['error_minus'] = self.error.currentText()
        else:
            info['error'] = None
            info['error_minus'] = None
    
        return info

class AxisBox_log_range_fac(AxisBox_log_range):
    def __init__(self, axis, df):
        AxisBox_log_range.__init__(self, axis, df)

        # row 5
        self.faceted_checkBox = QCheckBox(self)
        self.faceted_checkBox.setGeometry(QRect(13, 169, 72, 20))

        self.faceted_by_label = QLabel(self)
        self.faceted_by_label.setGeometry(QRect(121, 169, 69, 16))

        self.facet = QComboBox(self)
        self.facet.setGeometry(QRect(218, 169, 151, 26))
        self.addColToComBox(self.facet, df)

        self.faceted_by_label.setEnabled(False)
        self.facet.setEnabled(False)

        self.faceted_checkBox.stateChanged.connect(
            partial(self.checkBoxChangedAction, 
                    widgets = [self.facet, self.faceted_by_label]
            )
        )

        self.faceted_checkBox.setText("faceted")
        self.faceted_by_label.setText("arrange by:")

    def getCurrentInfo(self):
        info = super().getCurrentInfo()
        info['facet'] = self.facet.currentText() if self.faceted_checkBox.isChecked() else None
        
        return info

class AxisBox_no_marg(AxisBox_log_range_err):
    def __init__(self, axis, df):
        AxisBox_log_range_err.__init__(self, axis, df)

        # row 5
        self.faceted_checkBox = QCheckBox(self)
        self.faceted_checkBox.setGeometry(QRect(13, 212, 72, 20))

        self.faceted_by_label = QLabel(self)
        self.faceted_by_label.setGeometry(QRect(121, 212, 69, 16))

        self.facet = QComboBox(self)
        self.facet.setGeometry(QRect(218, 210, 151, 26))
        self.addColToComBox(self.facet, df)

        self.faceted_by_label.setEnabled(False)
        self.facet.setEnabled(False)

        self.faceted_checkBox.stateChanged.connect(
            partial(self.checkBoxChangedAction, 
                    widgets = [self.facet, self.faceted_by_label]
            )
        )

        self.faceted_checkBox.setText("faceted")
        self.faceted_by_label.setText("arrange by:")

    def getCurrentInfo(self):
        info = super().getCurrentInfo()
        info['facet'] = self.facet.currentText() if self.faceted_checkBox.isChecked() else None

        return info


class AxisBox_full(AxisBox_no_marg):
    def __init__(self, axis, df):
        AxisBox_no_marg.__init__(self, axis, df)

        # row 2

        self.marginal_comboBox = QComboBox(self)
        self.marginal_comboBox.setGeometry(QRect(265, 85, 104, 26))
        self.marginal_comboBox.addItem('rug')
        self.marginal_comboBox.addItem('box')
        self.marginal_comboBox.addItem('violin')
        self.marginal_comboBox.addItem('histogram')

        self.dis_subplot_checkBox = QCheckBox(self)
        self.dis_subplot_checkBox.setGeometry(QRect(106, 85, 161, 20))

        self.marginal_comboBox.setEnabled(False)

        self.dis_subplot_checkBox.stateChanged.connect(
            partial(self.checkBoxChangedAction, 
                    widgets = [self.marginal_comboBox]
            )
        )

        self.dis_subplot_checkBox.setText("distrubution subplot")

    def getCurrentInfo(self):
        info = super().getCurrentInfo()
        info['marginal'] = self.marginal_comboBox.currentText() if self.dis_subplot_checkBox.isChecked() else None
        
        return info