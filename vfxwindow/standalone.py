"""Window class for standalone use."""

from __future__ import absolute_import

import sys

from .base import BaseWindow
from .utils import setCoordinatesToScreen
from .utils.Qt import QtWidgets, IsPySide, IsPyQt4, IsPySide2, IsPyQt5


class StandaloneWindow(BaseWindow):
    """Window to use outside of specific programs."""
    def __init__(self, parent=None):
        super(StandaloneWindow, self).__init__(parent)
        self.standalone = True

    @classmethod
    def show(cls, **kwargs):
        """Start a standalone QApplication and launch the window.
        To launch another window, subprocess.Popen(["python", path]) must be used.
        """
        app = QtWidgets.QApplication(sys.argv)
        window = super(StandaloneWindow, cls).show()
        app.setActiveWindow(window)
        sys.exit(app.exec_())

    def setWindowPalette(self, program, version=None):
        """Override of the default setWindowPalette to also set style."""
        return super(StandaloneWindow, self).setWindowPalette(program, version, style=True)

    def windowPalette(self):
        currentPalette = super(StandaloneWindow, self).windowPalette()
        if currentPalette is None:
            if IsPySide or IsPyQt4:
                return 'Qt.4'
            elif IsPySide2 or IsPyQt5:
                return 'Qt.5'
        return currentPalette

    @classmethod
    def clearWindowInstance(self, windowID):
        """Close the last class instance."""
        previousInstance = super(StandaloneWindow, self).clearWindowInstance(windowID)
        if previousInstance is None:
            return

        #Shut down the window
        if not previousInstance['window'].isClosed():
            try:
                previousInstance['window'].close()
            except (RuntimeError, ReferenceError):
                pass

    def closeEvent(self, event):
        """Save the window location on window close."""
        self.saveWindowPosition()
        self.clearWindowInstance(self.ID)
        return super(StandaloneWindow, self).closeEvent(event)

    def saveWindowPosition(self):
        """Save the window location."""
        if 'standalone' not in self.windowSettings:
            self.windowSettings['standalone'] = {}
        if 'main' not in self.windowSettings['standalone']:
            self.windowSettings['standalone']['main'] = {}

        self.windowSettings['standalone']['main']['width'] = self.width()
        self.windowSettings['standalone']['main']['height'] = self.height()
        self.windowSettings['standalone']['main']['x'] = self.x()
        self.windowSettings['standalone']['main']['y'] = self.y()
        return super(StandaloneWindow, self).saveWindowPosition()

    def loadWindowPosition(self):
        """Set the position of the window when loaded."""
        try:
            x = self.windowSettings['standalone']['main']['x']
            y = self.windowSettings['standalone']['main']['y']
            width = self.windowSettings['standalone']['main']['width']
            height = self.windowSettings['standalone']['main']['height']
        except KeyError:
            super(StandaloneWindow, self).loadWindowPosition()
        else:
            x, y = setCoordinatesToScreen(x, y, width, height, padding=5)
            self.resize(width, height)
            self.move(x, y)
