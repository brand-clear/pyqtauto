#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains standardized PyQt4 widgets that are designed to speed up the development process.

"""
import sys
from PyQt4 import QtGui, QtCore
import setters


class Dialog(QtGui.QDialog):
	"""
	Standardized ``QDialog`` window.

	Attributes
	----------
	layout : QLayout subclass

	Parameters
	----------
	title : str
	layout_type : {
		'QVBoxLayout', 'QHBoxLayout', 
		'QFormLayout', 'QGridLayout'
		}, optional

	"""

	def __init__(self, title, layout_type='QVBoxLayout'):
		super(Dialog, self).__init__()
		self.setWindowTitle(title)
		self.layout = setters.set_layout(self, layout_type)
		self.layout.setSpacing(25)
		setters.set_uniform_margins(self, 10)

	def keyPressEvent(self, event):
		"""Override ``QDialog`` method to ignore ESC button exit."""
		if event.key() == QtCore.Qt.Key_Escape:
			event.ignore()


class OrphanMessageBox(QtGui.QMessageBox):
	"""
	Standardized QMessageBox with no parent.
	
	Parameters
	----------
	title : str
	message : list[str]
		Text to be displayed. Each item in the list falls on a seperate line.
	icon : {'warning', 'question', 'critical', 'information'}, optional
	buttons : {'ok', 'okcancel', 'yesno'}, optional	

	"""

	def __init__(self, title, message, icon='warning', buttons='ok'):
		super(OrphanMessageBox, self).__init__()
		message = '\n'.join(message)
		self.setWindowTitle(title)
		self.setText(message)
		self._set_icon(icon)
		setters.set_buttons(self, buttons)

	def _set_icon(self, icon):
		if icon == 'warning':
			self.setIcon(QtGui.QMessageBox.Warning)
		elif icon == 'question':
			self.setIcon(QtGui.QMessageBox.Question)
		elif icon == 'critical':
			self.setIcon(QtGui.QMessageBox.Critical)
		elif icon == 'information':
			self.setIcon(QtGui.QMessageBox.Information)


class ExceptionMessageBox(OrphanMessageBox):
	"""
	``OrphanMessageBox`` designed for Exception feedback.
	
	Parameters
	----------
	exception : Exception subclass
	icon : {'warning', 'question', 'critical', 'information'}, optional

	"""

	def __init__(self, exception, icon='warning'):
		if len(exception.message) > 1:
			msg = exception.message
		else:
			msg = str(exception)

		try:
			icon = exception.icon
		except AttributeError:
				pass

		super(ExceptionMessageBox, self).__init__(
			type(exception).__name__, [msg], icon
			)


class Ask(OrphanMessageBox):
	"""
	Standardized ``QMessageBox`` implementation.

	Parameters
	----------
	message : list[str]
		Text (question) to be displayed. Each item in the list falls on a seperate line.

	"""
	def __init__(self, title, message):
		super(Ask, self).__init__(
			title, message, icon='warning', buttons='yesno'
		)
	
	def yes(self):
		"""Returns True if user selected Yes."""
		if self.exec_() == QtGui.QMessageBox.Yes:
			return True


class DialogButtonBox(QtGui.QDialogButtonBox):
	"""
	Standardized ``QDialogButtonBox``.
	
	Parameters
	----------
	parent : QLayout subclass
	buttons : {'ok', 'okcancel', 'yesno'}, optional

	"""

	def __init__(self, parent, buttons='ok'):
		super(DialogButtonBox, self).__init__()
		setters.set_parent(self, parent)
		setters.set_buttons(self, buttons)

	def add_custom_button(self, text, role="accept"):
		"""Add button with custom text.

		Parameters
		----------
		text : str
		role : {'accept', 'reject'}, optional
			Defines signal attached to button click.

		"""
		if role == 'accept':
			role = QtGui.QDialogButtonBox.AcceptRole
		elif role == 'reject':
			role = QtGui.QDialogButtonBox.RejectRole
		self.addButton(text, role)


class GenericButton(QtGui.QPushButton):
	"""
	Standardized button base class.
	
	Parameters
	----------
	text : str or None, optional
	parent : QLayout subclass or None, optional
	response : callable or None, optional

	"""

	def __init__(self, text=None, parent=None, response=None):
		super(GenericButton, self).__init__(text)
		setters.set_parent(self, parent)
		setters.set_button_response(self, response)


class ImageButton(GenericButton):
	"""
	Button with image in place of text.

	Attributes
	----------
	mysquare : bool or int
	mywidth : int
	myheight : int

	Parameters
	----------
	img : str
		Absolute path to button icon.
	parent : QLayout subclass or None, optional
	response : callable or None, optional
	tooltip : str, optional
	enabled : bool, optional
	flat : bool, optional

	"""

	def __init__(self, img,	parent=None, response=None, 
				tooltip=str(),enabled=True,flat=False):
		super(ImageButton, self).__init__(None, parent, response)
		img = QtGui.QIcon(QtGui.QPixmap(img))
		self.setIcon(img)
		self.setToolTip(tooltip)
		self.setEnabled(enabled)
		self.setFlat(flat)
		self._mysquare = False
		self._mywidth = self.width()
		self._myheight = self.height()

	@property
	def mysquare(self):
		"""int or bool: The size of the instance, if squared."""
		if self._mywidth == self._myheight:
			return self._mywidth
		else:
			return False

	@mysquare.setter
	def mysquare(self, size):
		self._mysquare = size
		self._mywidth = size
		self._myheight = size
		self.setFixedSize(size, size)
		self.setIconSize(QtCore.QSize(size-10, size-10))

	@property
	def mywidth(self):
		"""int: The instance width."""
		return self._mywidth

	@mywidth.setter
	def mywidth(self, width):
		self._mywidth = width
		self.setFixedWidth(width)

	@property
	def myheight(self):
		"""int: The instance height."""
		return self._myheight

	@myheight.setter
	def myheight(self, height):
		self._myheight = height
		self.setFixedHeight(height)
		self.setIconSize(QtCore.QSize(height-10, height-10))


class TableImageButton(ImageButton):
	"""
	``ImageButton`` designed for ``QTableWidget`` cells.

	Attributes
	----------
	widget : QWidget
	layout : QVBoxLayout

	Parameters
	----------
	img : str
		Absolute path to button icon.
	response : callable or None, optional

	Notes
	-----
	When calling QTableWidget.setCellWidget(), instance.widget is the target.

	"""

	def __init__(self, img, response=None):
		super(TableImageButton, self).__init__(img, None, response)
		self.widget = QtGui.QWidget()
		self.layout = QtGui.QVBoxLayout(self.widget)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.addWidget(self)


class TableCheckBox(QtGui.QCheckBox):
	"""
	``QCheckBox`` designed for ``QTableWidget`` cells.

	Attributes
	----------
	widget : QWidget
	layout : QVBoxLayout

	Parameters
	----------
	checked : bool, optional
	response : callable or None, optional

	Notes
	-----
	When calling QTableWidget.setCellWidget(), instance.widget is the target.
	
	"""

	def __init__(self, checked=False, response=None):
		super(TableCheckBox, self).__init__()
		setters.set_checkbox_response(self, response)
		self.setChecked(checked)
		self.widget = QtGui.QWidget()
		self.layout = QtGui.QVBoxLayout(self.widget)
		setters.set_uniform_margins(self.layout, 0)
		self.layout.setAlignment(QtCore.Qt.AlignCenter)
		self.layout.addWidget(self)


class TableItem(QtGui.QTableWidgetItem):
	"""
	Standardized ``QTableWidgetItem``.
	
	Parameters
	----------
	text : str

	"""

	def __init__(self, text):
		super(TableItem, self).__init__(text)
		self.setTextAlignment(QtCore.Qt.AlignVCenter)
		self.setTextAlignment(QtCore.Qt.AlignCenter)
		self.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)


class ComboBox(QtGui.QComboBox):
	"""
	Standardized ``QComboBox``.

	Attributes
	----------
	items : list

	Parameters
	----------------
	parent : QLayout subclass or None, optional
	editable : bool, optional

	"""

	def __init__(self, items=list(), parent=None, editable=False):
		super(ComboBox, self).__init__()
		self.setEditable(editable)
		setters.set_parent(self, parent)
		self.items = items

	@property
	def items(self):
		"""list: The list of ``str`` items in the ``QComboBox``."""
		return [str(self.itemText(i)) for i in range(self.count())]

	@items.setter
	def items(self, items):
		self.addItems(items)

	@items.deleter
	def items(self):
		self.clear()


class MenuBar(object):
	"""
	Standardized ``menuBar`` object.

	Attributes
	----------
	menubar : menuBar

	Parameters
	----------
	parent : QMainWindow

	"""

	def __init__(self, parent):
		self.parent = parent
		self.menubar = self.parent.menuBar()

	def add_menu(self, name):
		"""Add dropdown menu to menuBar.

		Parameters
		----------
		name : str

		Returns
		-------
		menu : QMenu

		"""
		menu = self.menubar.addMenu(name)
		return menu

	def add_action(self, menu, img, name, shortcut=None, response=None):
 		"""Add action to menu.

 		Parameters
 		----------
 		menu : QMenu
 			Receiver of this action.
 		img : str
			Absolute path to action icon.
 		name : str
 		shortcut : str or None, optional
 		response : callable or None, optional

 		Returns
 		-------
 		action : QAction

 		"""
 		action = QtGui.QAction(QtGui.QIcon(img), name, self.parent)
 		setters.set_action_shortcut(action, shortcut)
 		setters.set_action_response(action, response)
 		menu.addAction(action)
 		return action


class ToolBar(object):
	"""
	Standardized ``ToolBar`` object.

	Attributes
	----------
	toolbar : ToolBar

	Parameters
	----------
	parent : QMainWindow
	name : str
	icon_size : int, optional

	"""

	def __init__(self, parent, name, icon_size=35):
		self.parent = parent
		self.toolbar = self.parent.addToolBar(name)
		self.toolbar.setIconSize(QtCore.QSize(icon_size, icon_size))

	def add_action(self, img, tooltip=str(), response=None):
		"""Add action to toolbar.

		Parameters
		----------
		img : str
			Absolute path to action icon.
		tooltip : str, optional
		response : func or None, optional

		Returns
		-------
		action : QAction

		"""
		action = QtGui.QAction(QtGui.QIcon(img), tooltip, self.parent)
		setters.set_action_response(action, response)
		self.toolbar.addAction(action)
		return action


class Workspace(QtGui.QGroupBox):
	"""
	Collapsible ``QGroupbox``.

	Attributes
	----------
	layout : QLayout subclass

	Parameters
	----------
	parent : QLayout subclass
	title : str
	max_height : int
	layout_type : {
		'QVBoxLayout', 'QHBoxLayout', 
		'QFormLayout', 'QGridLayout'
		}, optional
	spacing : int, optional
	flat : bool, optional

	"""

	def __init__(self, parent, title, max_height, layout_type='QVBoxLayout',
				spacing=10, flat=True):
		super(Workspace, self).__init__()
		self.setTitle(title)
		self.setMaximumHeight(max_height)
		self.setFlat(flat)
		self.setCheckable(True)
		self.layout = setters.set_layout(self, layout_type)
		self.layout.setSpacing(spacing)
		self.toggled.connect(self._toggle)
		setters.set_parent(self, parent)

	def _toggle(self):
		"""Toggle child widget visibility."""
		if not self.isChecked():
			self._hide_widgets()
		else:
			self._show_widgets()

	def _hide_widgets(self):
		"""
		Notes
		-----
		AttributeError is raised (and ignored) when QSpacerItem is found.

		"""
		for i in range(self.layout.count()):
			try:
				self.layout.itemAt(i).widget().hide()
			except AttributeError:
				pass

	def _show_widgets(self):
		"""
		Notes
		-----
		AttributeError is raised (and ignored) when QSpacerItem is found.

		"""
		for i in range(self.layout.count()):
			try:
				self.layout.itemAt(i).widget().show()
			except AttributeError:
				pass


class Spacer(QtGui.QSpacerItem):
	"""
	Standardized ``QSpacerItem``.
	
	Parameters
	----------
	xpad : int, optional
		Minimum spacing along X axis (width).
	ypad : int, optional
		Minimum spacing along Y axis (height).
	xpolicy : {'expanding', 'fixed', 'min', 'max}, optional
		Resize behavior along X axis (width).
	ypolicy : {'expanding', 'fixed', 'min', 'max}, optional
		Resize behavior along Y axis (height).

	"""

	def __init__(self, xpad=20, ypad=20, xpolicy='expanding', 
				ypolicy='expanding'):
		xpolicy = self._get_size_policy(xpolicy)
		ypolicy = self._get_size_policy(ypolicy)
		super(Spacer, self).__init__(xpad, ypad, xpolicy, ypolicy)

	def _get_size_policy(self, policy):
		"""
		Parameters
		----------
		policy : {'expanding', 'fixed', 'min', 'max}
		
		Returns
		-------
		QSizePolicy

		"""
		policy = policy.lower()
		if policy == 'expanding':
			return QtGui.QSizePolicy.Expanding
		elif policy == 'fixed':
			return QtGui.QSizePolicy.Fixed
		elif policy == 'min':
			return QtGui.QSizePolicy.Minimum
		elif policy == 'max':
			return QtGui.QSizePolicy.Maximum


class Table(QtGui.QTableWidget):
	"""
	Standardized ``QTableWidget``.

	Parameters
	----------
	headers : list[str]
		Horizontal header items.
	widths : list[int] or None, optional
		A list of corresponding horizontal header item widths. An input of None
		equates to a list of zeros of size len(`headers`).

	Attributes
	----------
	headers

	"""
	def __init__(self, headers, widths=None):
		self.headers = headers
		self._widths = widths
		super(Table, self).__init__()
		self.setColumnCount(len(self.headers))
		self.setHorizontalHeaderLabels(self.headers)
		self.horizontalHeader().setStretchLastSection(True)
		self._validate_widths()
		self._set_header_widths()

	def _validate_widths(self):
		"""Define header widths if input is ``None``."""
		if self._widths == None:
			self._widths = [0]*len(self.headers)

	def _set_header_widths(self):
		"""Assign horizontal header widths."""
		for i in range(self.columnCount()):
			if self._widths[i] == 0:
				self.horizontalHeader().setResizeMode(
					i,
					QtGui.QHeaderView.Stretch)
			else:
				self.setColumnWidth(i, self._widths[i])
				self.horizontalHeader().setResizeMode(
					i,
					QtGui.QHeaderView.Fixed)


class Calendar(QtGui.QCalendarWidget):
	"""
	Standardized ``QCalendarWidget``.

	Parameters
	----------
	parent : QLayout subclass, optional

	"""
	def __init__(self, parent=None):
		super(Calendar, self).__init__()
		setters.set_parent(self, parent)

	@property
	def date(self):
		"""str: The selected date."""
		return str(self.selectedDate().toString('MM/dd/yyyy'))


class StatusBar(QtGui.QStatusBar):
	"""
	Standardized ``QStatusBar``.

	Parameters
	----------
	parent : QMainWindow

	"""
	# The length of time status messages are shown in milliseconds.
	# 2000 = 2 seconds
	_DURATION = 2000

	def __init__(self, parent):
		self._parent = parent
		super(StatusBar, self).__init__()
		self._parent.setStatusBar(self)

	def show_login_msg(self, user):
		"""Message displayed immediately after user login.

		Parameters
		----------
		user : str

		"""
		self.showMessage('Logged in as %s' % user, self._DURATION)
	
	def show_save_msg(self, data):
		"""Message displayed immediately after save.

		Parameters
		----------
		data : str
			A name describing the information that was saved.

		"""
		self.showMessage('%s saved successfully' % data, self._DURATION)


if __name__ == '__main__':
	pass