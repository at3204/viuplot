import sys
import os
import csv
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QTabWidget, QTableWidget, 
    QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QAction, 
    QDialog, QSplashScreen)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from plot_dialog import PlotDialog

class Sheet(QTableWidget):
    def __init__(self, type = "new", filename=None, df=None):
        super().__init__()
        if type == "new":
            col_headers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
            self.df = pd.DataFrame(index = range(30), columns = col_headers)

        elif type == "df":
            self.df = df
            col_headers = list(self.df.columns)
        
        self.setup_df(filename, self.df, col_headers)

        self.check_change = True
        self.init_ui()

    def init_ui(self):
        self.cellChanged.connect(self.c_current)
        self.show()

    def c_current(self):
        if self.check_change:
            row = self.currentRow()
            col = self.currentColumn()
            value = self.item(row, col)
            value = value.text()
            #print("The current cell is ", row, ", ", col)
            #print("In this cell we have: ", value)

            if value == '':
                df_value = np.nan
            else:
                try:
                    df_value = float(value)
                except ValueError:
                    df_value = value

            self.df.iloc[row, col] = df_value 
            #print(self.df.iloc[row, col], type(self.df.iloc[row, col]))

    def setup_df(self, filename, df, col_headers):
        self.setRowCount(len(df.index))
        self.setColumnCount(len(df.columns))
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                try:
                    df_value = float(df.iloc[i, j])
                except ValueError:
                    df_value = 0

                if np.isnan(df_value):
                    self.setItem(i,j,QTableWidgetItem(''))
                else:
                    #print(type(df.iloc[i, j]))
                    self.setItem(i,j,QTableWidgetItem(str(df.iloc[i, j])))

        self.setHorizontalHeaderLabels(col_headers)

class DataTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.setTabShape(QTabWidget.Triangular)
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setUsesScrollButtons(True)

        self.tab1 = QWidget()
        self.tabs.resize(300,200)

        self.tabs.tabCloseRequested.connect(self.closeTab)

        # index for create new dataframe
        self.new_name_index = 1
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Dataframe1")
        
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)

        self.form_widget = Sheet(type = "new")

        self.tab1.layout.addWidget(self.form_widget)
        self.tab1.setLayout(self.tab1.layout)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)

    def add_dataframe(self, filename, df):
        self.new_tab = QWidget()
        
        self.new_tab.layout = QVBoxLayout(self)

        self.form_widget = Sheet(type = "df", filename = filename, df = df)

        self.new_tab.layout.addWidget(self.form_widget)
        self.new_tab.setLayout(self.new_tab.layout)

        self.tabs.addTab(self.new_tab, filename)
        self.tabs.setCurrentWidget(self.new_tab)

    def add_new_dataframe(self):
        self.new_tab = QWidget()
        
        self.new_tab.layout = QVBoxLayout(self)

        self.new_name_index += 1
        filename = "Dataframe"+str(self.new_name_index)

        self.form_widget = Sheet(type = "new", filename = filename)

        self.new_tab.layout.addWidget(self.form_widget)
        self.new_tab.setLayout(self.new_tab.layout)

        self.tabs.addTab(self.new_tab, filename)
        self.tabs.setCurrentWidget(self.new_tab)

    def closeTab(self, index):
        if self.tabs.count() > 1:
            self.tabs.widget(index).deleteLater()
            self.tabs.removeTab(index)
        elif self.tabs.count() == 1:
            self.tabs.removeTab(0)
        
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.plot_dialog = []
        self.resize(1000, 750)

        self.setWindowTitle('viuplot')
        self.setWindowIcon(QIcon('resource/icon.ico'))
        self.setWindowIconText('viuplot')

        self.data_tab = DataTabWidget(self)
        self.setCentralWidget(self.data_tab)
        self.create_menu()

        self.show()

    def create_menu(self):
        '''
        Make the menubar and add it to the QMainWindow
        '''
        # Create a menu for setting the GUI style.
        menubar = self.menuBar()

        # Create file menu ---
        newAction = QAction('&New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.triggered.connect(self.new)

        openAction = QAction('&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.open)

        saveAction = QAction('&Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('File saved')
        saveAction.triggered.connect(self.save)

        plotAction = QAction('&Plot', self)
        plotAction.setShortcut('Ctrl+S')
        plotAction.triggered.connect(self.plot)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(plotAction)

    def new(self):
        self.data_tab.add_new_dataframe()

    # open file, load the file dir and update dataFrame --TODO: various file type | check os decide 'file://' or 'C://' | error alert
    def open(self):
        filetuple = QFileDialog.getOpenFileName(
            self, "Select file", "/", 
            "All files (*.xlsx *.xls *.csv *.hdf);;Excel files (*.xlsx *.xls);;csv (*.csv);;hdf (*.hdf)"
        )
        
        if filetuple != ('', ''):
            filedir = filetuple[0]
            filename_ex = filedir.split('/')[-1].split('.')
            filetype = filename_ex[-1]
            filename = filename_ex[-2]

            #read data
            if filetype == 'xls' or filetype == 'xlsx':
                df = pd.read_excel('file://'+filedir, index_col=None, na_values=['NA'])
            elif filetype == 'csv':
                df = pd.read_csv('file://'+filedir, index_col=None, na_values=['NA'])
            elif filetype == 'hdf':
                df = pd.read_hdf('file://'+filedir, index_col=None, na_values=['NA'])
            #print(df.head())

            self.data_tab.add_dataframe(filename, df)

    def save(self):
        currentI = self.data_tab.tabs.currentIndex()
        name = self.data_tab.tabs.tabText(currentI)

        filename = QFileDialog.getSaveFileName(self, '','./export/'+name, ("Excel files (*.xlsx *.xls);;csv (*.csv)"))
        
        if filename != ('', ''):
            filedir = filename[0]

            df = self.data_tab.tabs.currentWidget().layout.itemAt(0).widget().df

            print(df.head())

            writer = pd.ExcelWriter(filedir, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()

    def plot(self):
        df = self.data_tab.tabs.currentWidget().layout.itemAt(0).widget().df
        self.plot_dialog.append(PlotDialog(df))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash_pix = QPixmap('resource/splash.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    app.setApplicationDisplayName('viuplot')
    sheetWindow = MyWindow()
    splash.finish(sheetWindow)

    sys.exit(app.exec_())