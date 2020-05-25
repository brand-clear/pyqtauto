import sys
import unittest
from PyQt4 import QtGui
from os.path import dirname
pyqtauto_import = dirname(dirname(__file__))
sys.path.insert(0, pyqtauto_import)
from pyqtauto.widgets import *

IMAGE = 'test.png'

class TestWidgetAppearance(object):
	"""Widget visual checks."""
	def __init__(self):
		# self.test_dialog()
		# self.test_orphanmessagebox()
		# self.test_genericbutton()
		# self.test_imagebutton()
		# self.tablewidgets = self.test_tablewidgets()
		self.test_combobox()
		# self.mainwindow = self.test_bars()

	def test_dialog(self):
		dialog = Dialog('Test')
		dialog.exec_()

	def test_orphanmessagebox(self):
		msg = OrphanMessageBox(
				'Test', 
				'Message', 
				'critical', 
				'okcancel')
		msg.exec_()

	def test_genericbutton(self):
		layout = QtGui.QVBoxLayout()
		btn = GenericButton('Test', layout, None)
		btn.show()

	def test_imagebutton(self):
		layout = QtGui.QVBoxLayout()
		btn = ImageButton(IMAGE, layout)
		btn.show()

	def test_tablewidgets(self):
		table = QtGui.QTableWidget()
		widgets = [TableItem, 
				TableCheckBox, 
				TableImageButton]
		table.setColumnCount(len(widgets))
		table.setRowCount(1)
		table.setItem(0, 0, TableItem('Test'))
		table.setCellWidget(0, 1, TableImageButton(IMAGE).widget)
		table.setCellWidget(0, 2, TableCheckBox().widget)
		table.show()
		return table

	def test_combobox(self):
		layout = QtGui.QVBoxLayout()
		btn = ComboBox(['test1', 'test2'], layout)
		btn.show()

	def test_bars(self):
		self.main = QtGui.QMainWindow()
		menubar = MenuBar(self.main)
		filemenu = menubar.add_menu('File')
		menubar.add_action(filemenu, '', 'Name')
		toolbar = ToolBar(self.main, 'Toolbar')
		toolbar.add_action('')
		self.main.show()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	app.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
	visual_checks = TestWidgetAppearance()
	sys.exit(app.exec_())