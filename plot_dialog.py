from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QDoubleSpinBox, QSpinBox,
    QGridLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QScrollArea, QTreeWidget, 
    QTreeWidgetItem, QTabWidget, QWidget, QLabel, QComboBox, QCheckBox, QApplication,
    QLineEdit, QMessageBox
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QRect, Qt, QMetaObject
from chart import Chart

from widgets.plot_setting import (PlotSetting_2d, PlotSetting_3d, PlotSetting_line_bar,
    PlotSetting_bar, PlotSetting_density_contour, PlotSetting_density_heatmap,
    PlotSetting_histogram
)

class PlotDialog(QDialog):

    def __init__(self, df=None):
        super().__init__()
        self.df = df
        self.resize(721, 586)

        # set up ok and cancel buttin box
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(360, 520, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        # set up chart select type tree widget in the left
        self.select_chart_type = QTreeWidget(self)
        self.select_chart_type.setGeometry(QRect(30, 30, 191, 471))
        self.select_chart_type.setObjectName("select_chart_type")

        self.scatter_plot = QTreeWidgetItem(self.select_chart_type)
        self.scatter = QTreeWidgetItem(self.scatter_plot)
        self.scatter_3d = QTreeWidgetItem(self.scatter_plot)

        self.line_plot = QTreeWidgetItem(self.select_chart_type)
        self.line = QTreeWidgetItem(self.line_plot)

        self.bar_plot = QTreeWidgetItem(self.select_chart_type)
        self.bar = QTreeWidgetItem(self.bar_plot)

        self.density_plot = QTreeWidgetItem(self.select_chart_type)
        self.density_contour = QTreeWidgetItem(self.density_plot)
        self.density_heatmap = QTreeWidgetItem(self.density_plot)
        self.histogram = QTreeWidgetItem(self.select_chart_type)

        self.select_chart_type.setCurrentItem(self.scatter)
        self.select_chart_type.currentItemChanged.connect(self.updateSetting)

        # set tab widget in the right
        self.scatter_tw = PlotSetting_2d(self, self.df)
        self.scatter_3d_tw = PlotSetting_3d(self, self.df)
        self.line_tw = PlotSetting_line_bar(self, self.df)
        self.bar_tw = PlotSetting_bar(self, self.df)
        self.density_contour_tw = PlotSetting_density_contour(self, self.df)
        self.density_heatmap_tw = PlotSetting_density_heatmap(self, self.df)
        self.histogram_tw = PlotSetting_histogram(self, self.df)

        self.scatter_tw.show()
        self.scatter_3d_tw.hide()
        self.line_tw.hide()
        self.bar_tw.hide()
        self.density_contour_tw.hide()
        self.density_heatmap_tw.hide()
        self.histogram_tw.hide()

        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)
        QMetaObject.connectSlotsByName(self)
        self.setText()

        self.setWindowTitle("Plot Setting")
        self.setWindowIcon(QIcon('resource/icon.ico'))
        self.setWindowIconText('viuplot')
        self.show()

    # set up tab with in each element
    def setText(self):

        # select_chart_type
        self.select_chart_type.headerItem().setText(0, "Chart type")
        __sortingEnabled = self.select_chart_type.isSortingEnabled()
        self.select_chart_type.setSortingEnabled(False)
        self.scatter_plot.setText(0, "scatter plot")
        self.scatter.setText(0, "scatter")
        self.scatter_3d.setText(0, "scatter 3d")
        self.line_plot.setText(0, "line plot")
        self.line.setText(0, "line")
        self.bar_plot.setText(0, "bar plot")
        self.bar.setText(0, "bar")
        self.density_plot.setText(0, "density plot")
        self.density_contour.setText(0, "density contour")
        self.density_heatmap.setText(0, "density heatmap")
        self.histogram.setText(0, "histogram")
        self.select_chart_type.setSortingEnabled(__sortingEnabled)

    # update func for tab widget view when current tree widget changes
    def updateSetting(self):
        if self.select_chart_type.currentItem() == self.scatter:
            self.scatter_tw.show()
            self.scatter_3d_tw.hide()
            self.line_tw.hide()
            self.bar_tw.hide()
            self.density_contour_tw.hide()
            self.density_heatmap_tw.hide()
            self.histogram_tw.hide()
            print("scatter")
        elif self.select_chart_type.currentItem() == self.scatter_3d:
            self.scatter_tw.hide()
            self.scatter_3d_tw.show()
            self.line_tw.hide()
            self.bar_tw.hide()
            self.density_contour_tw.hide()
            self.density_heatmap_tw.hide()
            self.histogram_tw.hide()
            print("scatter 3d")
        elif self.select_chart_type.currentItem() == self.line:
            self.scatter_tw.hide()
            self.scatter_3d_tw.hide()
            self.line_tw.show()
            self.bar_tw.hide()
            self.density_contour_tw.hide()
            self.density_heatmap_tw.hide()
            self.histogram_tw.hide()
            print("line")
        elif self.select_chart_type.currentItem() == self.bar:
            self.scatter_tw.hide()
            self.scatter_3d_tw.hide()
            self.line_tw.hide()
            self.bar_tw.show()
            self.density_contour_tw.hide()
            self.density_heatmap_tw.hide()
            self.histogram_tw.hide()
            print("bar")
        elif self.select_chart_type.currentItem() == self.density_contour:
            self.scatter_tw.hide()
            self.scatter_3d_tw.hide()
            self.line_tw.hide()
            self.bar_tw.hide()
            self.density_contour_tw.show()
            self.density_heatmap_tw.hide()
            self.histogram_tw.hide()
            print("density contour")
        elif self.select_chart_type.currentItem() == self.density_heatmap:
            self.scatter_tw.hide()
            self.scatter_3d_tw.hide()
            self.line_tw.hide()
            self.bar_tw.hide()
            self.density_contour_tw.hide()
            self.density_heatmap_tw.show()
            self.histogram_tw.hide()
            print("density heatmap")
        elif self.select_chart_type.currentItem() == self.histogram:
            self.scatter_tw.hide()
            self.scatter_3d_tw.hide()
            self.line_tw.hide()
            self.bar_tw.hide()
            self.density_contour_tw.hide()
            self.density_heatmap_tw.hide()
            self.histogram_tw.show()
            print("histogram")

    # func for creating chart when clicking ok
    def ok(self):
        currentItem = self.select_chart_type.currentItem()

        if currentItem == self.scatter:
            info = self.scatter_tw.getCurrentInfo()
            info['chart_type'] = 'scatter'

        elif currentItem == self.scatter_3d:
            info = self.scatter_3d_tw.getCurrentInfo()
            info['chart_type'] = 'scatter_3d'

        elif currentItem == self.line:
            info = self.line_tw.getCurrentInfo()
            info['chart_type'] = 'line'

        elif currentItem == self.bar:
            info = self.bar_tw.getCurrentInfo()
            info['chart_type'] = 'bar'

        elif currentItem == self.density_contour:
            info = self.density_contour_tw.getCurrentInfo()
            info['chart_type'] = 'density_contour'

        elif currentItem == self.density_heatmap:
            info = self.density_heatmap_tw.getCurrentInfo()
            info['chart_type'] = 'density_heatmap'

        elif currentItem == self.histogram:
            info = self.histogram_tw.getCurrentInfo()
            info['chart_type'] = 'histogram'

        print(info)
        try:
            self.chart = Chart(self.df, info)
            self.close()
        except (AttributeError, ValueError, TypeError) as e:
            self.err_msg = QMessageBox()
            self.err_msg.setIcon(QMessageBox.Critical)
            self.err_msg.setText("Error")
            self.err_msg.setInformativeText('Unable to plot with current setting.')
            self.err_msg.setWindowTitle("Error")
            self.err_msg.exec_()
    def cancel(self):
        self.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = PlotDialog()
    sys.exit(app.exec_())

