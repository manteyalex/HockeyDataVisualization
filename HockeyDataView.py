import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import seaborn as sns
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import matplotlib
import numpy as np
from CustomWidgets import CheckableComboBox, PandasTableModel
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,NavigationToolbar2QT
from matplotlib.figure import Figure

class HockeyDataView(object):

    def __init__(self, model, controller):
        self.model = model
        self.controller = controller
        self.window = QtWidgets.QMainWindow()
        self.setupUi(self.window)
        self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # self.mainlayout = QtWidgets.QGridLayout(self.centralwidget)
        # self.centralwidget.setLayout(self.mainlayout)



        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.dataTabs = QtWidgets.QTabWidget(self.centralwidget)
        # self.mainlayout.addWidget(self.tabWidget, 0, 0)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1500, 750))
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1500, 750))

        self.tabWidget.setObjectName("tabWidget")
        self.rinkTab = QtWidgets.QWidget()
        self.rinkTab.setObjectName("rinkTab")
        self.dataTab = QtWidgets.QWidget()
        self.dataTab.setObjectName("dataTab")
        self.tabWidget.addTab(self.rinkTab, "")
        self.tabWidget.addTab(self.dataTab, "")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.rinkTab)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1910, 990))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 20))
        self.menubar.setObjectName("menubar")
        self.menuHockey_Visualizer = QtWidgets.QMenu(self.menubar)
        self.menuHockey_Visualizer.setObjectName("menuHockey_Visualizer")
        self.menuData_Visualizer = QtWidgets.QMenu(self.menubar)
        self.menuData_Visualizer.setObjectName("menuData_Visualizer")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_Data_File = QtWidgets.QAction(MainWindow)
        self.actionLoad_Data_File.setObjectName("actionLoad_Data_File")
        self.actionSave_Image = QtWidgets.QAction(MainWindow)
        self.actionSave_Image.setObjectName("actionSave_Image")
        self.actionOpen_Data_Visualization_Tab = QtWidgets.QAction(MainWindow)
        self.actionOpen_Data_Visualization_Tab.setObjectName("actionOpen_Data_Visualization_Tab")
        self.actionGenerate_Report = QtWidgets.QAction(MainWindow)
        self.actionGenerate_Report.setObjectName("actionGenerate_Report")
        self.menuHockey_Visualizer.addAction(self.actionLoad_Data_File)
        self.menuHockey_Visualizer.addAction(self.actionSave_Image)
        self.menuHockey_Visualizer.addAction(self.actionGenerate_Report)
        self.menuData_Visualizer.addAction(self.actionOpen_Data_Visualization_Tab)
        self.menubar.addAction(self.menuHockey_Visualizer.menuAction())
        self.menubar.addAction(self.menuData_Visualizer.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #UI for team selection
        self.teamlabel = QtWidgets.QLabel("Team",self.centralwidget)
        team_xpos = 40
        team_ypos = 750
        x_spacing = 300
        self.teamlabel.setGeometry(QtCore.QRect(team_xpos, team_ypos, 200, 31))
        self.teamlabel.setFont(QtGui.QFont('Arial', 17))
        self.teamSelectionBox = QtWidgets.QComboBox(self.centralwidget)
        self.teamSelectionBox.setGeometry(QtCore.QRect(team_xpos, team_ypos+35, 255, 31))
        self.teamSelectionBox.currentTextChanged.connect(self.team_changed)
        # self.settingslayout.addWidget(self.teamSelectionBox,0)
        #UI elements for game selection
        self.gamelabel = QtWidgets.QLabel("Games", self.centralwidget)
        self.gamelabel.setGeometry(QtCore.QRect(team_xpos+x_spacing, team_ypos, 200, 31))
        self.gamelabel.setFont(QtGui.QFont('Arial', 17))
        self.gameSelectionBox = CheckableComboBox(self.centralwidget)
        self.gameSelectionBox.setGeometry(QtCore.QRect(team_xpos+x_spacing, team_ypos + 35, 325, 31))
        self.gameSelectionBox.model().dataChanged.connect(self.update_plot_table)

        self.scoringSummarylabel = QtWidgets.QLabel("Scoring Summary", self.centralwidget)
        self.scoringSummarylabel.setGeometry(QtCore.QRect(320, 620, 200, 31))
        self.scoringSummarylabel.setFont(QtGui.QFont('Arial', 15))
        self.goalTable = QtWidgets.QTableView(self.centralwidget)
        self.goalTable.setGeometry(200, 650, 420, 90)


        self.shotSummarylabel = QtWidgets.QLabel("Shots", self.centralwidget)
        self.shotSummarylabel.setGeometry(QtCore.QRect(1125, 620, 200, 31))
        self.shotSummarylabel.setFont(QtGui.QFont('Arial', 15))
        self.shotTable = QtWidgets.QTableView(self.centralwidget)
        self.shotTable.setGeometry(940, 650, 420, 90)

        self.detailedTable = QtWidgets.QTableView(self.centralwidget)
        self.detailedTable.setGeometry(1500,20,419,728)


        self.actionLoad_Data_File.triggered.connect(self.load_data_file)


        self.insert_plot_in_ui()

        self.actionSave_Image.triggered.connect(self.save_rink_plot)

        self.add_table()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hockey Data Visualizer"))
        self.tabWidget.setStatusTip(_translate("MainWindow", "View data overlayed on rink image"))
        self.dataTab.setWhatsThis(_translate("MainWindow", "View data in tables or graph format"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dataTab), _translate("MainWindow", "Data View"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.rinkTab), _translate("MainWindow", "Rink View"))
        self.menuHockey_Visualizer.setTitle(_translate("MainWindow", "File"))
        self.menuData_Visualizer.setTitle(_translate("MainWindow", "Data Visualizer"))
        self.actionLoad_Data_File.setText(_translate("MainWindow", "Load Data File"))
        self.actionLoad_Data_File.setStatusTip(_translate("MainWindow", "Load hockey data file"))
        self.actionLoad_Data_File.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave_Image.setText(_translate("MainWindow", "Save Image"))
        self.actionSave_Image.setStatusTip(_translate("MainWindow", "Save current image"))
        self.actionSave_Image.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionOpen_Data_Visualization_Tab.setText(_translate("MainWindow", "Open Data Visualization Tab"))
        self.actionGenerate_Report.setText(_translate("MainWindow", "Generate Report"))


    def add_table(self):
        df = pd.DataFrame({'':['',''],
                           '1st':[0,0],
                           '2nd':[0,0],
                           '3rd':[0,0],
                           'OT':['N/A','N/A'],
                           'Total':[0,0]
                           })
        dataModel = PandasTableModel(df)
        self.goalTable.setModel(dataModel)
        header = self.goalTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        
        df_shots = pd.DataFrame({'':['',''],
                           '1st':[0,0],
                           '2nd':[0,0],
                           '3rd':[0,0],
                           'OT':['N/A','N/A'],
                           'Total':[0,0]
                           })
        shotsModel = PandasTableModel(df_shots)
        self.shotTable.setModel(shotsModel)
        header = self.shotTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)

        df_detailed = pd.DataFrame({'':['Goals','Total Shots','SH%','Shot Attempts','Blocked Shots','Average Shot Distance (ft)','Average Goal Distance (ft)'],
                           'Team': [0,0,0,0,0,0,0],
                           'Opposition': [0,0,0,0,0,0,0],

                           })

        detailedModel = PandasTableModel(df_detailed)
        self.detailedTable.setModel(detailedModel)
        header = self.detailedTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        
    def update_tables(self,df_goals,df_shots,df_detailed):
        dataModel = PandasTableModel(df_goals)
        self.goalTable.setModel(dataModel)
        dataModel = PandasTableModel(df_shots)
        self.shotTable.setModel(dataModel)
        detailedModel = PandasTableModel(df_detailed)
        self.detailedTable.setModel(detailedModel)


    def load_data_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, 'Open data file',
                                            os.path.dirname(os.path.abspath(__file__)), "Data csv (*.csv)")
        self.model.load_data(fname[0])
        self.update_team_selection()
        # self.rink_shot_plot(self.model.recent_game, self.teamSelectionBox.currentText())

    def save_rink_plot(self):
        self.toolbar.save_figure()


    def update_team_selection(self):

        for i,t in enumerate(self.model.teams):
            self.teamSelectionBox.addItem(t)
            if t == self.model.recent_home_team:
                self.teamSelectionBox.setCurrentIndex(i)

    def team_changed(self,team):
        self.rink_ax.cla()
        self.add_rink_image()
        self.rink_canvas.draw()
        games = self.controller.get_games(team)
        self.gameSelectionBox.clear()
        self.gameSelectionBox.addItems(games)
        self.add_table()


    def update_plot_table(self):
        self.rink_ax.cla()
        self.add_rink_image()
        self.rink_canvas.draw()
        game_dates = [game.split(' ')[0] for game in self.gameSelectionBox.currentData()]

        if len(game_dates) > 0:
            team = self.teamSelectionBox.currentText()
            self.rink_shot_plot(game_dates,team)
            df = self.controller.get_summary(team,game_dates,event="Goal")
            df2 = self.controller.get_summary(team, game_dates, event="Shot")
            df3, _, _, _, _ = self.controller.get_detailed_shot_information(team, game_dates)

            goals_focused = df.iloc[0,-1]
            shots_focused = df2.iloc[0,-1]
            goals_opposition = df.iloc[1, -1]
            shots_opposition = df2.iloc[1, -1]
            shp_focused = goals_focused/shots_focused*100
            shp_opposition = goals_opposition/shots_opposition*100
            df3.iloc[0,1] = goals_focused
            df3.iloc[0,2] = goals_opposition
            df3.iloc[1, 1] = shots_focused
            df3.iloc[1, 2] = shots_opposition
            df3.iloc[2, 1] = shp_focused
            df3.iloc[2, 2] = shp_opposition
            df3.columns = ['',df.iloc[0,0],df.iloc[1,0]]
            self.update_tables(df,df2,df3)

        if len(game_dates) == 0:
            self.add_table()

        return

    def insert_plot_in_ui(self):
        self.rink_figure = plt.figure()
        self.rink_figure.set_size_inches(15, 6.375)
        self.rink_ax = self.rink_figure.add_subplot(111)
        self.rink_ax.invert_xaxis()

        self.add_rink_image()
        self.rink_canvas = FigureCanvasQTAgg(self.rink_figure)
        self.rink_canvas.setParent(self.rinkTab)



        self.rink_figure.tight_layout(pad=5)
        self.toolbar = NavigationToolbar2QT(self.rink_canvas, self.rinkTab)


    def add_rink_image(self):
        rink_image = mpimg.imread("rink_coords_cropped.png")
        self.rink_ax.imshow(rink_image, aspect='auto', extent=(200, 0, 0, 85), zorder=-1)
        self.rink_ax.set_ylabel('Attacking',fontsize=18)

    def rink_shot_plot(self,games,focused_team,heatmap=True):
        focused_team, opposition_team, teams = self.controller.get_shots_goals(focused_team,games)#

        focused_all, focused_shots, focused_goals = focused_team
        opposition_all, opposition_shots, opposition_goals = opposition_team

        cmap_focused = sns.cubehelix_palette(start=0, light=1, as_cmap=True)
        cmap_opposition = sns.cubehelix_palette(start=2, light=1, as_cmap=True)

        # home heatmap
        if heatmap:
            home_heatmap = sns.kdeplot(
                x=focused_all['X Coordinate'], y=focused_all['Y Coordinate'],
                cmap=cmap_focused, fill=True, clip=((100, 200), (0, 85)),
                thresh=0, levels=10,
                ax=self.rink_ax, alpha=0.5
            )
            # away heatmap
            away_heatmap = sns.kdeplot(
                x=200 - opposition_all['X Coordinate'], y=opposition_all['Y Coordinate'],
                cmap=cmap_opposition, fill=True, clip=((0, 100), (0, 85)),
                thresh=0, levels=10,
                ax=self.rink_ax, alpha=0.5
            )




        self.rink_ax.scatter(focused_shots['X Coordinate'], focused_shots['Y Coordinate'], marker='x', color='r',
                   label=teams['focused_team'])
        self.rink_ax.scatter(focused_goals['X Coordinate'], focused_goals['Y Coordinate'], marker='o', color='gold',
                   edgecolor='r')

        self.rink_ax.scatter(200 - opposition_shots['X Coordinate'], opposition_shots['Y Coordinate'], marker='x',
                   color='b', label=teams['opposition_team'])
        self.rink_ax.scatter(200 - opposition_goals['X Coordinate'], opposition_goals['Y Coordinate'], marker='o',
                   color='gold', edgecolor='b')


        # ax.hist2d(home_shot_locations['X Coordinate'],home_shot_locations['Y Coordinate'],bins=[20,9])
        self.rink_ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.10),
                  fancybox=True, shadow=True, ncol=2)

        self.rink_ax.set_xlabel('')
        self.rink_ax.set_ylabel('')
        self.rink_ax.set_ylabel('Attacking', fontsize=18)
        self.rink_canvas.draw()




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = HockeyDataView(1,1)
    # ui.setupUi(MainWindow)

    sys.exit(app.exec_())
