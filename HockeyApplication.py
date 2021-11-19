import sys
from PyQt5.QtWidgets import QApplication
from HockeyDataModel import HockeyDataModel
from HockeyDataController import HockeyDataController
from HockeyDataView import HockeyDataView
class HockeyApp(QApplication):
    def __init__(self,sys_argv):
        super(HockeyApp,self).__init__(sys_argv)
        self.model = HockeyDataModel()
        self.controller = HockeyDataController(self.model)
        self.view = HockeyDataView(self.model,self.controller)
        self.view.window.show()

if __name__ == '__main__':
    file = "olympic_womens_dataset.csv"
    app = HockeyApp(sys.argv)
    sys.exit(app.exec_())