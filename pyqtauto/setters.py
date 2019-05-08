"""
This module contains PyQt4 assignment functions that were designed specifically 
for the standardized widgets found in pyqtauto.widgets.
These functions are intended to be called at the instantiation of standardized 
widgets without raising errors due to fluctuating parameters.
"""


from PyQt4 import QtGui


def set_layout(parent, layout_type='QVBoxLayout'):
	"""
	Parameters
	----------
	parent : QWidget or subclass
	layout_type : {QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout}, optional 
		Name of QLayout subclass.

	Returns
	-------
	QLayout subclass
	"""
	for layout in QtGui.QBoxLayout.__subclasses__():
		if layout.__name__ == layout_type:
			return layout(parent)
	for layout in QtGui.QLayout.__subclasses__():
		if layout.__name__ == layout_type:
			return layout(parent)


def set_parent(child, parent):
	"""
	Parameters
	----------
	child : QWidget or subclass
	parent : QLayout subclass
	"""
	try:
		parent.addWidget(child)
	except AttributeError:
		pass


def set_uniform_margins(widget, margin):
	"""
	Parameters
	----------
	widget : QWidget or subclass
	margin : int
	"""
	widget.setContentsMargins(margin, margin, margin, margin)


def set_buttons(widget, buttons=None):
    """
    Parameters
    ----------
    widget : DialogButtonBox or subclass, OrphanMessageBox or subclass
    buttons : {None, 'ok', 'okcancel', 'yesno'}, optional
    """
    if buttons is not None:
            if buttons == 'ok':
                    widget.setStandardButtons(widget.Ok)
            elif buttons == 'okcancel':
                    widget.setStandardButtons(widget.Ok | widget.Cancel)
            elif buttons == 'yesno':
                    widget.setStandardButtons(widget.Yes | widget.No)


def set_button_response(button, response=None):
	"""
	Parameters
	----------
	button : GenericButton or subclass
	response : func or None, optional
	"""
	try:
		button.clicked.connect(response)
	except TypeError:
		pass


def set_checkbox_response(checkbox, response=None):
	"""
	Parameters
	----------
	checkbox : CheckBox or subclass
	response : func or None, optional
	"""
	try:
		checkbox.stateChanged.connect(response)
	except TypeError:
		pass


def set_action_shortcut(action, shortcut):
	"""
	Parameters
	----------
	action : QAction
	shortcut : str
		QAction response trigger (Ex. 'Ctrl+N').
	"""
	try:
		action.setShortcut(shortcut)
	except TypeError:
		pass


def set_action_response(action, response=None):
	"""
	Parameters
	----------
	action : QAction
	response : func or None, optional
	"""
	try:
		action.triggered.connect(response)
	except TypeError:
		pass


if __name__ == '__main__':
	pass