from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QDoubleSpinBox, QSpinBox,
    QGridLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QScrollArea, QTreeWidget, 
    QTreeWidgetItem, QTabWidget, QWidget, QLabel, QComboBox, QCheckBox, QApplication,
    QLineEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect, Qt
from functools import partial

from widgets.axis_box import (AxisBox, AxisBox_log_range, AxisBox_log_range_err, 
    AxisBox_log_range_fac, AxisBox_no_marg, AxisBox_full
)

class PlotSetting(QTabWidget):
    def __init__(self, parent, df):
        QTabWidget.__init__(self, parent)
        self.setGeometry(QRect(230, 20, 471, 481))

        # -- general tab
        self.general_tab = QWidget()
        
        self.general_scroll_area_content = QWidget()
        self.general_scroll_area = QScrollArea(self.general_tab)
        self.general_scroll_area.setGeometry(QRect(0, 0, 469, 471))

        # title
        self.title_label = QLabel()
        self.lineEdit = QLineEdit()

        self.general_hbox = QHBoxLayout()
        self.general_hbox.addStretch()
        self.general_hbox.addWidget(self.title_label)
        self.general_hbox.addWidget(self.lineEdit)
        self.general_hbox.addStretch()
        
        self.general_scroll_area.setWidget(self.general_scroll_area_content)

        self.addTab(self.general_tab, "")

        # advance tab
        self.advance_tab = QWidget()

        self.advance_scroll_area = QWidget(self.advance_tab)
        self.advance_scroll_area.setGeometry(QRect(0, 0, 469, 471))

        self.addTab(self.advance_tab, "")
        self.advance_vbox = QVBoxLayout()
        self.advance_vbox.addStretch()
        self.advance_scroll_area.setLayout(self.advance_vbox)

        # animation group box
        self.advance_group_box = QGroupBox()
        self.advance_group_box.setGeometry(QRect(50, 30, 321, 133))
        font = QFont()
        font.setPointSize(14)

        self.advance_group_box.setFont(font)
        
        self.advance_group_diff_by_gridLayout = QGridLayout(self.advance_group_box)

        self.animation_checkBox = QCheckBox(self.advance_group_box)
        self.advance_group_diff_by_gridLayout.addWidget(self.animation_checkBox, 0, 0, 1, 2)

        self.frame_label = QLabel(self.advance_group_box)
        self.advance_group_diff_by_gridLayout.addWidget(self.frame_label, 0, 2, 1, 1)

        self.frame_combo_box = QComboBox(self.advance_group_box)
        self.advance_group_diff_by_gridLayout.addWidget(self.frame_combo_box, 0, 3, 1, 1)
        self.addColToComBox(self.frame_combo_box, df)

        self.group_label = QLabel(self.advance_group_box)
        self.advance_group_diff_by_gridLayout.addWidget(self.group_label, 1, 2, 1, 1)

        self.group_combo_box = QComboBox(self.advance_group_box)
        self.advance_group_diff_by_gridLayout.addWidget(self.group_combo_box, 1, 3, 1, 1)
        self.addColToComBox(self.group_combo_box, df)

        self.frame_combo_box.setEnabled(False)
        self.group_combo_box.setEnabled(False)
        self.frame_label.setEnabled(False)
        self.group_label.setEnabled(False)

        self.animation_checkBox.stateChanged.connect(
            partial(self.checkBoxChangedAction, 
                    widgets = [self.frame_combo_box, self.group_combo_box, self.frame_label, self.group_label]
            )
        )

        self.advance_vbox.addWidget(self.advance_group_box)
        self.advance_vbox.addStretch()


        # data group box
        self.data_group_box = QGroupBox()
        self.data_group_box.setGeometry(QRect(50, 180, 321, 103))
        font = QFont()
        font.setPointSize(14)
        self.data_group_box.setFont(font)

        self.data_group_diff_by_gridLayout = QGridLayout(self.data_group_box)
        self.fixed_checkbox = QCheckBox(self.data_group_box)
        self.data_group_diff_by_gridLayout.addWidget(self.fixed_checkbox, 0, 0, 1, 1)

        self.column_label_fixed = QLabel(self.data_group_box)
        self.data_group_diff_by_gridLayout.addWidget(self.column_label_fixed, 0, 1, 1, 1)

        self.text_comboBox = QComboBox(self.data_group_box)
        self.data_group_diff_by_gridLayout.addWidget(self.text_comboBox, 0, 2, 1, 1)
        self.addColToComBox(self.text_comboBox, df)

        self.text_comboBox.setEnabled(False)
        self.column_label_fixed.setEnabled(False)

        self.fixed_checkbox.stateChanged.connect(
            partial(self.checkBoxChangedAction, 
                    widgets = [self.text_comboBox, self.column_label_fixed]
            )
        )

        self.hover_checkBox = QCheckBox(self.data_group_box)
        self.data_group_diff_by_gridLayout.addWidget(self.hover_checkBox, 1, 0, 1, 1)

        self.column_label_hover = QLabel(self.data_group_box)
        self.data_group_diff_by_gridLayout.addWidget(self.column_label_hover, 1, 1, 1, 1)

        self.hover_name_comboBox = QComboBox(self.data_group_box)
        self.data_group_diff_by_gridLayout.addWidget(self.hover_name_comboBox, 1, 2, 1, 1)
        self.addColToComBox(self.hover_name_comboBox, df)

        self.hover_name_comboBox.setEnabled(False)
        self.column_label_hover.setEnabled(False)

        self.hover_checkBox.stateChanged.connect(
            partial(self.checkBoxChangedAction, 
                    widgets = [self.hover_name_comboBox, self.column_label_hover]
            )
        )

        self.advance_vbox.addWidget(self.data_group_box)
        self.advance_vbox.addStretch()

        # view tab
        self.ViewTab = QWidget()

        # figure setting group box
        self.figure_setting_group_box = QGroupBox(self.ViewTab)
        self.figure_setting_group_box.setGeometry(QRect(40, 20, 381, 141))
        font = QFont()
        font.setPointSize(14)
        self.figure_setting_group_box.setFont(font)

        self.figure_setting_diff_by_gridLayout = QGridLayout(self.figure_setting_group_box)

        # self.opacity_doubleSpinBox = QDoubleSpinBox(self.figure_setting_group_box)
        # self.figure_setting_diff_by_gridLayout.addWidget(self.opacity_doubleSpinBox, 6, 2, 1, 1)

        # self.opacity_label = QLabel(self.figure_setting_group_box)
        # self.figure_setting_diff_by_gridLayout.addWidget(self.opacity_label, 6, 1, 1, 1)

        # self.height_label = QLabel(self.figure_setting_group_box)
        # self.figure_setting_diff_by_gridLayout.addWidget(self.height_label, 1, 3, 1, 1)

        # self.width_label = QLabel(self.figure_setting_group_box)
        # self.figure_setting_diff_by_gridLayout.addWidget(self.width_label, 1, 1, 1, 1)

        # self.width_spinBox = QSpinBox(self.figure_setting_group_box)
        # self.figure_setting_diff_by_gridLayout.addWidget(self.width_spinBox, 1, 2, 1, 1)

        # self.height_spinBox = QSpinBox(self.figure_setting_group_box)
        # self.figure_setting_diff_by_gridLayout.addWidget(self.height_spinBox, 1, 4, 1, 1)

        self.theme_label = QLabel(self.figure_setting_group_box)
        self.figure_setting_diff_by_gridLayout.addWidget(self.theme_label, 0, 1, 1, 1)

        self.theme_comboBox = QComboBox(self.figure_setting_group_box)
        self.theme_comboBox.addItem("plotly")
        self.theme_comboBox.addItem("plotly_white")
        self.theme_comboBox.addItem("plotly_dark")
        self.theme_comboBox.addItem("ggplot2")
        self.theme_comboBox.addItem("seaborn")
        self.theme_comboBox.addItem("none")
        
        self.figure_setting_diff_by_gridLayout.addWidget(self.theme_comboBox, 0, 2, 1, 3)

        self.diff_by_label = QGroupBox(self.ViewTab)
        self.diff_by_label.setGeometry(QRect(40, 170, 381, 191))
        font = QFont()
        font.setPointSize(14)
        self.diff_by_label.setFont(font)

        self.diff_by_gridLayout = QGridLayout(self.diff_by_label)

        # color
        self.color_checkBox = QCheckBox(self.diff_by_label)
        self.diff_by_gridLayout.addWidget(self.color_checkBox, 0, 0, 1, 1)

        self.color_label = QLabel(self.diff_by_label)
        self.diff_by_gridLayout.addWidget(self.color_label, 0, 1, 1, 1)

        self.color_comboBox = QComboBox(self.diff_by_label)
        self.diff_by_gridLayout.addWidget(self.color_comboBox, 0, 2, 1, 2)
        self.addColToComBox(self.color_comboBox, df)

        self.color_comboBox.setEnabled(False)
        self.color_label.setEnabled(False)

        self.color_checkBox.stateChanged.connect(
            partial(self.checkBoxChangedAction, 
                    widgets = [self.color_comboBox, self.color_label]
            )
        )

        # symbol
        self.symbol_checkBox = QCheckBox(self.diff_by_label)
        self.diff_by_gridLayout.addWidget(self.symbol_checkBox, 1, 0, 1, 1)

        self.symbol_label = QLabel(self.diff_by_label)
        self.diff_by_gridLayout.addWidget(self.symbol_label, 1, 1, 1, 1)

        self.symbol_comboBox = QComboBox(self.diff_by_label)
        self.diff_by_gridLayout.addWidget(self.symbol_comboBox, 1, 2, 1, 2)
        self.addColToComBox(self.symbol_comboBox, df)

        self.symbol_comboBox.setEnabled(False)
        self.symbol_label.setEnabled(False)

        self.symbol_checkBox.stateChanged.connect(
            partial(self.checkBoxChangedAction, 
                    widgets = [self.symbol_comboBox, self.symbol_label]
            )
        )

        # size
        self.size_checkBox = QCheckBox(self.diff_by_label)
        self.diff_by_gridLayout.addWidget(self.size_checkBox, 4, 0, 1, 1)

        self.size_label = QLabel(self.diff_by_label)
        self.diff_by_gridLayout.addWidget(self.size_label, 4, 1, 1, 1)

        self.size_cmoboBox = QComboBox(self.diff_by_label)
        self.diff_by_gridLayout.addWidget(self.size_cmoboBox, 4, 2, 1, 2)

        self.size_max_label = QLabel(self.diff_by_label)
        self.diff_by_gridLayout.addWidget(self.size_max_label, 5, 1, 1, 1)

        self.size_max_spinBox = QSpinBox(self.diff_by_label)
        self.diff_by_gridLayout.addWidget(self.size_max_spinBox, 5, 3, 1, 1)
        self.size_max_spinBox.setMaximum(100000)
        self.addColToComBox(self.size_cmoboBox, df)

        self.size_cmoboBox.setEnabled(False)
        self.size_max_spinBox.setEnabled(False)
        self.size_max_label.setEnabled(False)
        self.size_label.setEnabled(False)

        self.size_checkBox.stateChanged.connect(
            partial(self.checkBoxChangedAction, 
                    widgets = [self.size_cmoboBox, self.size_max_spinBox, self.size_label, self.size_max_label]
            )
        )

        self.addTab(self.ViewTab, "")

        # general tab
        self.title_label.setText("Title:")
        self.setTabText(self.indexOf(self.general_tab), "General")
        
        self.advance_group_box.setTitle("Advance")
        self.animation_checkBox.setText("animation")
        self.frame_label.setText("frame:")
        self.group_label.setText("group:")
        self.data_group_box.setTitle("Data Label")
        self.fixed_checkbox.setText("fixed label")
        self.column_label_fixed.setText("column:")
        self.hover_checkBox.setText("hover label")
        self.column_label_hover.setText("column:")
        self.setTabText(self.indexOf(self.advance_tab), "Advance")


        self.figure_setting_group_box.setTitle("Figure Setting")
        self.theme_label.setText("theme")
        # self.opacity_label.setText("opacity")
        # self.height_label.setText("height")
        # self.width_label.setText("width")
        self.diff_by_label.setTitle("Differentiate by:")
        self.size_checkBox.setText("size")
        self.color_checkBox.setText("color")
        self.symbol_label.setText("column:")
        self.size_max_label.setText("size max:")
        self.color_label.setText("column:")
        self.symbol_checkBox.setText("symbol")
        self.size_label.setText("column:")
        self.setTabText(self.indexOf(self.ViewTab), "View")

        self.setCurrentIndex(0)

    def addColToComBox(self, comboBox, df):
        for column in list(df.columns):
            comboBox.addItem(column)

    # func to enable and disable widgets when checkbox value changes
    def checkBoxChangedAction(self, state, widgets):
        if (Qt.Checked == state):
            for widget in widgets:
                widget.setEnabled(True)
        else:
            for widget in widgets:
                widget.setEnabled(False)

    def getCurrentInfo(self):
        info = {}
        info['title'] = self.lineEdit.text()
        info['x'] = self.x.getCurrentInfo()
        info['y'] = self.y.getCurrentInfo()

        if self.animation_checkBox.isChecked():
            info['animation_frame'] = self.frame_combo_box.currentText()
            info['animation_group'] = self.group_combo_box.currentText()
        else:
            info['animation_frame'] = None
            info['animation_group'] = None

        info['text'] = self.text_comboBox.currentText() if self.fixed_checkbox.isChecked() else None
        info['hover_name'] = self.column_label_hover.currentText() if self.hover_checkBox.isChecked() else None

        info['template'] = self.theme_comboBox.currentText()
        # info['width'] = self.width_spinBox.value()
        # info['height'] = self.height_spinBox.value()
        # info['opacity'] = self.opacity_doubleSpinBox.value()

        info['color'] = self.color_comboBox.currentText() if self.color_checkBox.isChecked() else None
        info['symbol'] = self.symbol_comboBox.currentText() if self.symbol_checkBox.isChecked() else None
        info['size'] = self.size_cmoboBox.currentText() if self.size_checkBox.isChecked() else None
        
        return info

class PlotSetting_2d(PlotSetting):
    def __init__(self, parent, df):
        PlotSetting.__init__(self, parent=parent, df=df)
        self.general_scroll_area_content.setGeometry(QRect(0, 0, 460, 600))

        # x_axis
        self.x = AxisBox_full('X', df)

        self.general_hbox_x = QHBoxLayout()
        self.general_hbox_x.addSpacing(10)
        self.general_hbox_x.addWidget(self.x)
        self.general_hbox_x.addSpacing(10)

        # y axis
        self.y = AxisBox_full('Y', df)

        self.general_hbox_y = QHBoxLayout()
        self.general_hbox_y.addSpacing(10)
        self.general_hbox_y.addWidget(self.y)
        self.general_hbox_y.addSpacing(10)
        
        self.general_vbox = QVBoxLayout()
        self.general_vbox.addLayout(self.general_hbox)
        self.general_vbox.addLayout(self.general_hbox_x)
        self.general_vbox.addLayout(self.general_hbox_y)

        self.general_scroll_area_content.setLayout(self.general_vbox)

        self.trendline_checkBox = QCheckBox(self.advance_group_box)
        self.advance_group_diff_by_gridLayout.addWidget(self.trendline_checkBox, 2, 0, 1, 1)

        self.trendline_combo_box = QComboBox(self.advance_group_box)
        self.advance_group_diff_by_gridLayout.addWidget(self.trendline_combo_box, 2, 1, 1, 3)
        self.trendline_combo_box.addItem("Least Squares Regression")
        self.trendline_combo_box.addItem("Locally Weighted Smoothing")

        self.trendline_combo_box.setEnabled(False)

        self.trendline_checkBox.stateChanged.connect(
            partial(self.checkBoxChangedAction, 
                    widgets = [self.trendline_combo_box]
            )
        )
        self.trendline_checkBox.setText("trendline")

    def getCurrentInfo(self):
        info = super().getCurrentInfo()
        if self.trendline_checkBox.isChecked():
            if self.trendline_combo_box.currentText() == "Least Squares Regression":
                info['trendline'] = 'lowess'
            elif self.trendline_combo_box.currentText() == "Locally Weighted Smoothing":
                info['trendline'] = 'ols'
        else:
            info['trendline'] = None

        return info

class PlotSetting_3d(PlotSetting):
    def __init__(self, parent, df):
        PlotSetting.__init__(self, parent=parent, df=df)
        self.general_scroll_area_content.setGeometry(QRect(0, 0, 460, 600))

        # x axis
        self.x = AxisBox_log_range_err('X', df)

        self.general_hbox_x = QHBoxLayout()
        self.general_hbox_x.addSpacing(10)
        self.general_hbox_x.addWidget(self.x)
        self.general_hbox_x.addSpacing(10)

        # y axis
        self.y = AxisBox_log_range_err('Y', df)

        self.general_hbox_y = QHBoxLayout()
        self.general_hbox_y.addSpacing(10)
        self.general_hbox_y.addWidget(self.y)
        self.general_hbox_y.addSpacing(10)

        # z axis
        self.z = AxisBox_log_range_err('Z', df)

        self.general_hbox_z = QHBoxLayout()
        self.general_hbox_z.addSpacing(10)
        self.general_hbox_z.addWidget(self.z)
        self.general_hbox_z.addSpacing(10)

        self.general_vbox = QVBoxLayout()
        self.general_vbox.addLayout(self.general_hbox)
        self.general_vbox.addLayout(self.general_hbox_x)
        self.general_vbox.addLayout(self.general_hbox_y)
        self.general_vbox.addLayout(self.general_hbox_z)

        self.general_scroll_area_content.setLayout(self.general_vbox)

    def getCurrentInfo(self):
        info = super().getCurrentInfo()
        info['z'] = self.z.getCurrentInfo()

        return info

class PlotSetting_line_bar(PlotSetting):
    def __init__(self, parent, df):
        PlotSetting.__init__(self, parent=parent, df=df)
        self.general_scroll_area_content.setGeometry(QRect(0, 0, 460, 600))

        # x axis
        self.x = AxisBox_no_marg('X', df)

        self.general_hbox_x = QHBoxLayout()
        self.general_hbox_x.addSpacing(10)
        self.general_hbox_x.addWidget(self.x)
        self.general_hbox_x.addSpacing(10)

        # y axis
        self.y = AxisBox_no_marg('Y', df)

        self.general_hbox_y = QHBoxLayout()
        self.general_hbox_y.addSpacing(10)
        self.general_hbox_y.addWidget(self.y)
        self.general_hbox_y.addSpacing(10)
        
        self.general_vbox = QVBoxLayout()
        self.general_vbox.addLayout(self.general_hbox)
        self.general_vbox.addLayout(self.general_hbox_x)
        self.general_vbox.addLayout(self.general_hbox_y)

        self.general_scroll_area_content.setLayout(self.general_vbox)

        self.symbol_checkBox.setEnabled(False)
        self.size_checkBox.setEnabled(False)

class PlotSetting_bar(PlotSetting_line_bar):
    def __init__(self, parent, df):
        PlotSetting_line_bar.__init__(self, parent=parent, df=df)

        # Other setting groupbox in advance tab
        self.other_group_box = QGroupBox(self.advance_tab)
        self.other_group_box.setGeometry(QRect(50, 300, 321, 103))
        font = QFont()
        font.setPointSize(14)
        self.other_group_box.setFont(font)
        self.other_group_box.setTitle("Other")

        self.other_group_gridLayout = QGridLayout(self.other_group_box)

        # barmode
        self.barmode_label = QLabel(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.barmode_label, 0, 0, 1, 1)
        self.barmode_label.setText('barmode')

        self.column_label_barmode = QLabel(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.column_label_barmode, 0, 1, 1, 1)
        self.column_label_barmode.setText('column:')

        self.barmode_comboBox = QComboBox(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.barmode_comboBox, 0, 2, 1, 1)
        self.barmode_comboBox.addItems(['relative','group','overlay'])

    def getCurrentInfo(self):
        info = super().getCurrentInfo()
        info['barmode'] = self.barmode_comboBox.currentText()

        return info
        

class PlotSetting_density(PlotSetting):
    def __init__(self, parent, df):
        PlotSetting.__init__(self, parent=parent, df=df)

        self.general_scroll_area_content.setGeometry(QRect(0, 0, 460, 800))

        # x axis
        self.x = AxisBox_full('X', df)

        self.general_hbox_x = QHBoxLayout()
        self.general_hbox_x.addSpacing(10)
        self.general_hbox_x.addWidget(self.x)
        self.general_hbox_x.addSpacing(10)

        # y axis
        self.y = AxisBox_full('Y', df)

        self.general_hbox_y = QHBoxLayout()
        self.general_hbox_y.addSpacing(10)
        self.general_hbox_y.addWidget(self.y)
        self.general_hbox_y.addSpacing(10)

        # z axis
        self.z = AxisBox('Z', df)

        self.general_hbox_z = QHBoxLayout()
        self.general_hbox_z.addSpacing(10)
        self.general_hbox_z.addWidget(self.z)
        self.general_hbox_z.addSpacing(10)

        self.general_vbox = QVBoxLayout()
        self.general_vbox.addLayout(self.general_hbox)
        self.general_vbox.addLayout(self.general_hbox_x)
        self.general_vbox.addLayout(self.general_hbox_y)
        self.general_vbox.addLayout(self.general_hbox_z)

        self.general_scroll_area_content.setLayout(self.general_vbox)

        self.symbol_checkBox.setEnabled(False)
        self.size_checkBox.setEnabled(False)

        # Other setting groupbox in advance tab

        self.other_group_box = QGroupBox()
        self.other_group_box.setGeometry(QRect(50, 300, 321, 203))
        font = QFont()
        font.setPointSize(14)
        self.other_group_box.setFont(font)
        self.other_group_box.setTitle("Other")

        self.other_group_gridLayout = QGridLayout(self.other_group_box)

        # histfunc
        self.histfunc_label = QLabel(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.histfunc_label, 0, 0, 1, 1)
        self.histfunc_label.setText('histfunc')

        self.column_label_histfunc = QLabel(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.column_label_histfunc, 0, 1, 1, 1)
        self.column_label_histfunc.setText('column:')

        self.histfunc_comboBox = QComboBox(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.histfunc_comboBox, 0, 2, 1, 1)
        self.histfunc_comboBox.addItems(['count', 'sum', 'avg', 'min', 'max'])

        # histnorm
        self.histnorm_label = QLabel(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.histnorm_label, 1, 0, 1, 1)
        self.histnorm_label.setText('histnorm')

        self.column_label_histnorm = QLabel(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.column_label_histnorm, 1, 1, 1, 1)
        self.column_label_histnorm.setText('column:')

        self.histnorm_comboBox = QComboBox(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.histnorm_comboBox, 1, 2, 1, 1)
        self.histnorm_comboBox.addItems(['none', 'percent', 'probability', 'density', 'probability density'])

        # nbins
        self.nbinsx_checkBox = QCheckBox(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.nbinsx_checkBox, 2, 0, 1, 1)
        self.nbinsx_checkBox.setText('X: number of bins')

        self.nbinsx_spinBox = QSpinBox(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.nbinsx_spinBox, 2, 1, 1, 1)
        self.nbinsx_spinBox.setEnabled(False)
        self.nbinsx_spinBox.setMaximum(10000)

        self.nbinsx_checkBox.stateChanged.connect(
            partial(self.checkBoxChangedAction, 
                    widgets = [self.nbinsx_spinBox]
            )
        )

        self.nbinsy_checkBox = QCheckBox(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.nbinsy_checkBox, 3, 0, 1, 1)
        self.nbinsy_checkBox.setText('Y: number of bins')

        self.nbinsy_spinBox = QSpinBox(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.nbinsy_spinBox, 3, 1, 1, 1)
        self.nbinsy_spinBox.setEnabled(False)
        self.nbinsy_spinBox.setMaximum(10000)

        self.nbinsy_checkBox.stateChanged.connect(
            partial(self.checkBoxChangedAction, 
                    widgets = [self.nbinsy_spinBox]
            )
        )
        
        self.advance_vbox.addWidget(self.other_group_box)
        self.advance_vbox.addStretch()

    def getCurrentInfo(self):
        info = super().getCurrentInfo()
        info['z'] = self.z.getCurrentInfo()

        info['histfunc'] = self.histfunc_comboBox.currentText()

        if self.histnorm_comboBox.currentText() == 'none':
            info['histnorm'] = None
        else:
            info['histnorm'] = self.histnorm_comboBox.currentText()

        if self.nbinsx_checkBox.isChecked:
            info['nbinsx'] = self.nbinsx_spinBox.value()
        else:
            info['nbinsx'] = None

        if self.nbinsy_checkBox.isChecked:
            info['nbinsy'] = self.nbinsy_spinBox.value()
        else:
            info['nbinsy'] = None

        return info

class PlotSetting_density_heatmap(PlotSetting_density):
    def __init__(self, parent, df):
        PlotSetting_density.__init__(self, parent=parent, df=df)
        self.color_checkBox.setEnabled(False)

class PlotSetting_density_contour(PlotSetting_density):
    def __init__(self, parent, df):
        PlotSetting_density.__init__(self, parent=parent, df=df)
        self.trendline_checkBox = QCheckBox(self.advance_group_box)
        self.advance_group_diff_by_gridLayout.addWidget(self.trendline_checkBox, 2, 0, 1, 1)

        self.trendline_combo_box = QComboBox(self.advance_group_box)
        self.advance_group_diff_by_gridLayout.addWidget(self.trendline_combo_box, 2, 1, 1, 3)
        self.trendline_combo_box.addItem("Least Squares Regression")
        self.trendline_combo_box.addItem("Locally Weighted Smoothing")

        self.trendline_combo_box.setEnabled(False)

        self.trendline_checkBox.stateChanged.connect(
            partial(self.checkBoxChangedAction, 
                    widgets = [self.trendline_combo_box]
            )
        )
        self.trendline_checkBox.setText("trendline")

        self.color_checkBox.setEnabled(True)

    def getCurrentInfo(self):
        info = super().getCurrentInfo()
        if self.trendline_checkBox.isChecked():
            if self.trendline_combo_box.currentText() == "Least Squares Regression":
                info['trendline'] = 'lowess'
            elif self.trendline_combo_box.currentText() == "Locally Weighted Smoothing":
                info['trendline'] = 'ols'
        else:
            info['trendline'] = None
            
        return info

class PlotSetting_histogram(PlotSetting):
    def __init__(self, parent, df):
        PlotSetting.__init__(self, parent=parent, df=df)
        self.general_scroll_area_content.setGeometry(QRect(0, 0, 460, 600))

        # x_axis
        self.x = AxisBox_full('X', df)

        self.general_hbox_x = QHBoxLayout()
        self.general_hbox_x.addSpacing(10)
        self.general_hbox_x.addWidget(self.x)
        self.general_hbox_x.addSpacing(10)

        # y axis
        self.y = AxisBox_log_range_fac('Count of Y', df)

        self.general_hbox_y = QHBoxLayout()
        self.general_hbox_y.addSpacing(10)
        self.general_hbox_y.addWidget(self.y)
        self.general_hbox_y.addSpacing(10)
        
        self.general_vbox = QVBoxLayout()
        self.general_vbox.addLayout(self.general_hbox)
        self.general_vbox.addLayout(self.general_hbox_x)
        self.general_vbox.addLayout(self.general_hbox_y)

        self.general_scroll_area_content.setLayout(self.general_vbox)

        self.symbol_checkBox.setEnabled(False)
        self.size_checkBox.setEnabled(False)

        # Other setting groupbox in advance tab

        self.other_group_box = QGroupBox()
        self.other_group_box.setGeometry(QRect(50, 300, 321, 203))
        font = QFont()
        font.setPointSize(14)
        self.other_group_box.setFont(font)
        self.other_group_box.setTitle("Other")

        self.other_group_gridLayout = QGridLayout(self.other_group_box)

        # barmode
        self.barmode_label = QLabel(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.barmode_label, 0, 0, 1, 1)
        self.barmode_label.setText('barmode')

        self.column_label_barmode = QLabel(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.column_label_barmode, 0, 1, 1, 1)
        self.column_label_barmode.setText('column:')

        self.barmode_comboBox = QComboBox(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.barmode_comboBox, 0, 2, 1, 1)
        self.barmode_comboBox.addItems(['relative','group','overlay'])

        # barnorm
        self.barnorm_label = QLabel(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.barnorm_label, 1, 0, 1, 1)
        self.barnorm_label.setText('barnorm')

        self.column_label_barnorm = QLabel(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.column_label_barnorm, 1, 1, 1, 1)
        self.column_label_barnorm.setText('column:')

        self.barnorm_comboBox = QComboBox(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.barnorm_comboBox, 1, 2, 1, 1)
        self.barnorm_comboBox.addItems(['none', 'fraction', 'percent'])

        # histfunc
        self.histfunc_label = QLabel(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.histfunc_label, 2, 0, 1, 1)
        self.histfunc_label.setText('histfunc')

        self.column_label_histfunc = QLabel(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.column_label_histfunc, 2, 1, 1, 1)
        self.column_label_histfunc.setText('column:')

        self.histfunc_comboBox = QComboBox(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.histfunc_comboBox, 2, 2, 1, 1)
        self.histfunc_comboBox.addItems(['count', 'sum', 'avg', 'min', 'max'])

        # histnorm
        self.histnorm_label = QLabel(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.histnorm_label, 3, 0, 1, 1)
        self.histnorm_label.setText('histnorm')

        self.column_label_histnorm = QLabel(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.column_label_histnorm, 3, 1, 1, 1)
        self.column_label_histnorm.setText('column:')

        self.histnorm_comboBox = QComboBox(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.histnorm_comboBox, 3, 2, 1, 1)
        self.histnorm_comboBox.addItems(['none', 'percent', 'probability', 'density', 'probability density'])

        # nbins
        self.cumulative_checkBox = QCheckBox(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.cumulative_checkBox, 4, 0, 1, 1)
        self.cumulative_checkBox.setText('cumulative')

        self.nbins_checkBox = QCheckBox(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.nbins_checkBox, 4, 1, 1, 1)
        self.nbins_checkBox.setText('number of bins')

        self.nbins_spinBox = QSpinBox(self.other_group_box)
        self.other_group_gridLayout.addWidget(self.nbins_spinBox, 4, 2, 1, 1)
        self.nbins_spinBox.setEnabled(False)
        self.nbins_spinBox.setMaximum(10000)

        self.nbins_checkBox.stateChanged.connect(
            partial(self.checkBoxChangedAction, 
                    widgets = [self.nbins_spinBox]
            )
        )
        
        self.advance_vbox.addWidget(self.other_group_box)
        self.advance_vbox.addStretch()

    def getCurrentInfo(self):
        info = super().getCurrentInfo()
        info['barmode'] = self.barmode_comboBox.currentText()
        
        if self.barnorm_comboBox.currentText() == 'none':
            info['barnorm'] = None
        else:
            info['barnorm'] = self.barnorm_comboBox.currentText()

        info['histfunc'] = self.histfunc_comboBox.currentText()

        if self.histnorm_comboBox.currentText() == 'none':
            info['histnorm'] = None
        else:
            info['histnorm'] = self.histnorm_comboBox.currentText()

        if self.nbins_checkBox.isChecked:
            info['nbins'] = self.nbins_spinBox.value()
        else:
            info['nbins'] = None

        info['cumulative'] = self.cumulative_checkBox.isChecked()

        return info