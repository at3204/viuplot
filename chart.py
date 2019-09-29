import sys
import os
from PyQt5.QtCore import QUrl, QFileInfo
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLineEdit, QDialog, QMainWindow, QAction, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QIcon
from random import randint
import plotly.express as px
import plotly.offline as po


class Chart(QMainWindow):

    def __init__(self, df, info):

        super().__init__()
        self.df = df

        self.resize(721, 600)
        self.setWindowTitle('Chart')
        self.setWindowIcon(QIcon('resource/icon.ico'))
        self.setWindowIconText('viuplot')

        self.view = QWebEngineView(self)

        if info['chart_type'] == 'scatter':
            self.fig = px.scatter(
                self.df,
                title = info['title'],
                x = info['x']['column'],
                log_x = info['x']['log'],
                marginal_x = info['x']['marginal'],
                error_x = info['x']['error'],
                error_x_minus = info['x']['error_minus'],
                range_x = info['x']['range'],
                facet_col = info['x']['facet'],
                y = info['y']['column'],
                log_y = info['y']['log'],
                marginal_y = info['y']['marginal'],
                error_y = info['y']['error'],
                error_y_minus = info['y']['error_minus'],
                range_y = info['y']['range'],
                facet_row = info['y']['facet'],
                trendline = info['trendline'],
                animation_frame = info['animation_frame'],
                animation_group = info['animation_group'],
                text = info['text'],
                hover_name = info['hover_name'],
                template = info['template'],
                #width = info['width'],
                #height = info['height'],
                #opacity = info['opacity'],
                color = info['color'],
                symbol = info['symbol'],
                size = info['size']
            )

        elif info['chart_type'] == 'scatter_3d':
            self.fig = px.scatter_3d(
                self.df,
                title = info['title'],
                x = info['x']['column'],
                log_x = info['x']['log'],
                error_x = info['x']['error'],
                error_x_minus = info['x']['error_minus'],
                range_x = info['x']['range'],
                y = info['y']['column'],
                log_y = info['y']['log'],
                error_y = info['y']['error'],
                error_y_minus = info['y']['error_minus'],
                range_y = info['y']['range'],
                z = info['z']['column'],
                log_z = info['z']['log'],
                error_z = info['z']['error'],
                error_z_minus = info['z']['error_minus'],
                range_z = info['z']['range'],
                animation_frame = info['animation_frame'],
                animation_group = info['animation_group'],
                text = info['text'],
                hover_name = info['hover_name'],
                template = info['template'],
                #width = info['width'],
                #height = info['height'],
                #opacity = info['opacity'],
                color = info['color'],
                symbol = info['symbol'],
                size = info['size']
            )

        elif info['chart_type'] == 'line':
            self.fig = px.line(
                self.df,
                title = info['title'],
                x = info['x']['column'],
                log_x = info['x']['log'],
                error_x = info['x']['error'],
                error_x_minus = info['x']['error_minus'],
                range_x = info['x']['range'],
                facet_col = info['x']['facet'],
                y = info['y']['column'],
                log_y = info['y']['log'],
                error_y = info['y']['error'],
                error_y_minus = info['y']['error_minus'],
                range_y = info['y']['range'],
                facet_row = info['y']['facet'],
                animation_frame = info['animation_frame'],
                animation_group = info['animation_group'],
                text = info['text'],
                hover_name = info['hover_name'],
                template = info['template'],
                #width = info['width'],
                #height = info['height'],
                #opacity = info['opacity'],
                color = info['color']
            )
        
        elif info['chart_type'] == 'bar':
            self.fig = px.bar(
                self.df,
                title = info['title'],
                x = info['x']['column'],
                log_x = info['x']['log'],
                error_x = info['x']['error'],
                error_x_minus = info['x']['error_minus'],
                range_x = info['x']['range'],
                facet_col = info['x']['facet'],
                y = info['y']['column'],
                log_y = info['y']['log'],
                error_y = info['y']['error'],
                error_y_minus = info['y']['error_minus'],
                range_y = info['y']['range'],
                facet_row = info['y']['facet'],
                animation_frame = info['animation_frame'],
                animation_group = info['animation_group'],
                text = info['text'],
                hover_name = info['hover_name'],
                template = info['template'],
                #width = info['width'],
                #height = info['height'],
                #opacity = info['opacity'],
                color = info['color']
            )
        
        elif info['chart_type'] == 'density_contour':
            self.fig = px.density_contour(
                self.df,
                title = info['title'],
                x = info['x']['column'],
                log_x = info['x']['log'],
                range_x = info['x']['range'],
                facet_col = info['x']['facet'],
                marginal_x = info['x']['marginal'],
                y = info['y']['column'],
                log_y = info['y']['log'],
                range_y = info['y']['range'],
                facet_row = info['y']['facet'],
                marginal_y = info['y']['marginal'],
                z = info['z']['column'],
                animation_frame = info['animation_frame'],
                animation_group = info['animation_group'],
                hover_name = info['hover_name'],
                template = info['template'],
                #width = info['width'],
                #height = info['height'],
                #opacity = info['opacity'],
                color = info['color'],
                histfunc = info['histfunc'],
                histnorm = info['histnorm'],
                nbinsx = info['nbinsx'],
                nbinsy = info['nbinsy']
            )
        
        elif info['chart_type'] == 'density_heatmap':
            self.fig = px.density_heatmap(
                self.df,
                title = info['title'],
                x = info['x']['column'],
                log_x = info['x']['log'],
                range_x = info['x']['range'],
                facet_col = info['x']['facet'],
                marginal_x = info['x']['marginal'],
                y = info['y']['column'],
                log_y = info['y']['log'],
                range_y = info['y']['range'],
                facet_row = info['y']['facet'],
                marginal_y = info['y']['marginal'],
                z = info['z']['column'],
                animation_frame = info['animation_frame'],
                animation_group = info['animation_group'],
                hover_name = info['hover_name'],
                template = info['template'],
                #width = info['width'],
                #height = info['height'],
                #opacity = info['opacity'],
                histfunc = info['histfunc'],
                histnorm = info['histnorm'],
                nbinsx = info['nbinsx'],
                nbinsy = info['nbinsy']
            )

        elif info['chart_type'] == 'histogram':
            self.fig = px.histogram(
                self.df,
                title = info['title'],
                x = info['x']['column'],
                log_x = info['x']['log'],
                range_x = info['x']['range'],
                facet_col = info['x']['facet'],
                marginal = info['x']['marginal'],
                y = info['y']['column'],
                log_y = info['y']['log'],
                range_y = info['y']['range'],
                facet_row = info['y']['facet'],
                animation_frame = info['animation_frame'],
                animation_group = info['animation_group'],
                hover_name = info['hover_name'],
                template = info['template'],
                #width = info['width'],
                #height = info['height'],
                #opacity = info['opacity'],
                color = info['color'],
                barmode = info['barmode'],
                barnorm = info['barnorm'],
                histfunc = info['histfunc'],
                histnorm = info['histnorm'],
                nbins = info['nbins'],
                cumulative = info['cumulative']
            )

        self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "temp.html"))
        po.plot(self.fig, filename=self.file_path, auto_open = False)
        url = QUrl(QUrl.fromLocalFile(self.file_path))
        self.view.resize(721, 800)
        self.view.load(url)

        self.create_menu()

        self.show()

    def create_menu(self):
        '''
        Make the menubar and add it to the QMainWindow
        '''
        # Create a menu for setting the GUI style.
        menubar = self.menuBar()

        # Create file menu ---

        saveAction = QAction('&Save as html', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.save)

        closeWinAction = QAction('&Close Chart Window', self)
        closeWinAction.setShortcut('Ctrl+Q')
        closeWinAction.triggered.connect(self.close)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(saveAction)
        fileMenu.addAction(closeWinAction)

    def save(self):
        filename = QFileDialog.getSaveFileName(self, '','./export/', ("html files (*.html)"))
        
        if filename != ('', ''):
            filedir = filename[0]
            po.plot(self.fig, filename=filedir, auto_open = True)

    def closeEvent(self, event):
        os.remove(self.file_path)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ch = Chart()
    sys.exit(app.exec_())