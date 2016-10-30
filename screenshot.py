#!/usr/bin/env python
# Python screenshot tool (fullscreen/area selection)
# Tested on:
# Lubuntu 13.04 x86_64
# Gentoo 4.1.7-hardened-r1 x86_64

import sys
from PyQt4 import QtCore, QtGui
from commands import getoutput
from StringIO import StringIO
from Xlib import X, display, Xutil


# Documentation for python-xlib here:
# http://python-xlib.sourceforge.net/doc/html/index.html

class XSelect:
    def __init__(self, display):
        # X display
        self.d = display

        # Screen
        self.screen = self.d.screen()

        # Draw on the root window (desktop surface)
        self.window = self.screen.root

        # If only I could get this working...
        #cursor = xobject.cursor.Cursor(self.d, Xcursorfont.crosshair)
        #cursor = self.d.create_resource_object('cursor', Xcursorfont.X_cursor)
        cursor = X.NONE

        self.window.grab_pointer(1, X.PointerMotionMask|X.ButtonReleaseMask|X.ButtonPressMask,
                X.GrabModeAsync, X.GrabModeAsync, X.NONE, cursor, X.CurrentTime)

        self.window.grab_keyboard(1, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)

        colormap = self.screen.default_colormap
        color = colormap.alloc_color(0, 0, 0)
        # Xor it because we'll draw with X.GXxor function
        xor_color = color.pixel ^ 0xffffff

        self.gc = self.window.create_gc(
            line_width = 1,
            line_style = X.LineSolid,
            fill_style = X.FillOpaqueStippled,
            fill_rule  = X.WindingRule,
            cap_style  = X.CapButt,
            join_style = X.JoinMiter,
            foreground = xor_color,
            background = self.screen.black_pixel,
            function = X.GXxor,
            graphics_exposures = False,
            subwindow_mode = X.IncludeInferiors,
        )

        done    = False
        started = False
        start   = dict(x=0, y=0)
        end     = dict(x=0, y=0)
        last    = None
        drawlimit = 10
        i = 0

        while done == False:
            e = self.d.next_event()

            # Window has been destroyed, quit
            if e.type == X.DestroyNotify:
                sys.exit(0)

            # Mouse button press
            elif e.type == X.ButtonPress:
                # Left mouse button?
                if e.detail == 1:
                    start = dict(x=e.root_x, y=e.root_y)
                    started = True

                # Right mouse button?
                elif e.detail == 3:
                    sys.exit(0)

            # Mouse button release
            elif e.type == X.ButtonRelease:
                end = dict(x=e.root_x, y=e.root_y)
                if last:
                    self.draw_rectangle(start, last)
                done = True
                pass

            # Mouse movement
            elif e.type == X.MotionNotify and started:
                i = i + 1
                if i % drawlimit != 0:
                    continue

                if last:
                    self.draw_rectangle(start, last)
                    last = None

                last = dict(x=e.root_x, y=e.root_y)
                self.draw_rectangle(start, last)
                pass

            # Keyboard key
            elif e.type == X.KeyPress:
                sys.exit(0)

        self.d.flush()

        coords = self.get_coords(start, end)
        if coords['width'] <= 1 or coords['height'] <= 1:
            sys.exit(0)
        else:
            print "%d %d %d %d" % (coords['start']['x'], coords['start']['y'], coords['width'], coords['height'])

    def get_coords(self, start, end):
        safe_start = dict(x=0, y=0)
        safe_end   = dict(x=0, y=0)

        if start['x'] > end['x']:
            safe_start['x'] = end['x']
            safe_end['x']   = start['x']
        else:
            safe_start['x'] = start['x']
            safe_end['x']   = end['x']

        if start['y'] > end['y']:
            safe_start['y'] = end['y']
            safe_end['y']   = start['y']
        else:
            safe_start['y'] = start['y']
            safe_end['y']   = end['y']

        return {
            'start': {
                'x': safe_start['x'],
                'y': safe_start['y'],
            },
            'end': {
                'x': safe_end['x'],
                'y': safe_end['y'],
            },
            'width' : safe_end['x'] - safe_start['x'],
            'height': safe_end['y'] - safe_start['y'],
        }

    def draw_rectangle(self, start, end):
        coords = self.get_coords(start, end)
        self.window.rectangle(self.gc,
            coords['start']['x'],
            coords['start']['y'],
            coords['end']['x'] - coords['start']['x'],
            coords['end']['y'] - coords['start']['y']
        )


class Screenshot(QtGui.QWidget):
    def __init__(self):
        super(Screenshot, self).__init__()

        self.screenshotLabel = QtGui.QLabel()
        self.screenshotLabel.setSizePolicy(QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Expanding)
        self.screenshotLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.screenshotLabel.setMinimumSize(240, 160)

        self.createOptionsGroupBox()
        self.createButtonsLayout()

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.screenshotLabel)
        mainLayout.addWidget(self.optionsGroupBox)
        mainLayout.addLayout(self.buttonsLayout)
        self.setLayout(mainLayout)

        self.area = None
        self.shootScreen()
        self.delaySpinBox.setValue(1)

        self.setWindowTitle("Screenshot")
        self.resize(300, 200)

    def resizeEvent(self, event):
        scaledSize = self.originalPixmap.size()
        scaledSize.scale(self.screenshotLabel.size(), QtCore.Qt.KeepAspectRatio)
        if not self.screenshotLabel.pixmap() or scaledSize != self.screenshotLabel.pixmap().size():
            self.updateScreenshotLabel()

    def selectArea(self):
        self.hide()

        resArea = getoutput('python %s -A' % sys.argv[0]) #TODO horrible 1/2 !
        if resArea and resArea != '0 0 0 0':
            self.area = xo, yo, x, y = resArea.split()
            self.areaLabel.setText("Area: x%s y%s to x%s y%s" % (xo, yo, x, y))
            self.shootScreen()
            # print 'OK', self.area #DEBUG
        elif self.area is not None:
            self.area = None
            self.areaLabel.setText("Area: fullscreen")
            self.shootScreen()

        self.show()

    def newScreenshot(self):
        if self.hideThisWindowCheckBox.isChecked():
            self.hide()
        self.newScreenshotButton.setDisabled(True)

        QtCore.QTimer.singleShot(self.delaySpinBox.value() * 1000, self.shootScreen)

    def saveScreenshot(self):
        format = 'png'
        initialPath = QtCore.QDir.currentPath() + "/untitled." + format

        fileName = QtGui.QFileDialog.getSaveFileName(self, "Save As",
                initialPath,
                "%s Files (*.%s);;All Files (*)" % (format.upper(), format))
        if fileName:
            self.originalPixmap.save(fileName, format)

    def shootScreen(self):
        if self.delaySpinBox.value() != 0:
            QtGui.qApp.beep()

        # Garbage collect any existing image first.
        self.originalPixmap = None
        self.originalPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())
        if self.area is not None:
            qi = self.originalPixmap.toImage()
            size = qi.size()
            qi = qi.copy(int(self.area[0]), int(self.area[1]), int(self.area[2]), int(self.area[3]))
            self.originalPixmap = None
            self.originalPixmap = QtGui.QPixmap.fromImage(qi)

        self.updateScreenshotLabel()

        self.newScreenshotButton.setDisabled(False)
        if self.hideThisWindowCheckBox.isChecked():
            self.show()

    def updateCheckBox(self):
        if self.delaySpinBox.value() == 0:
            self.hideThisWindowCheckBox.setDisabled(True)
        else:
            self.hideThisWindowCheckBox.setDisabled(False)

    def createOptionsGroupBox(self):
        self.optionsGroupBox = QtGui.QGroupBox("Options")

        self.delaySpinBox = QtGui.QSpinBox()
        self.delaySpinBox.setSuffix(" s")
        self.delaySpinBox.setMaximum(60)
        self.delaySpinBox.valueChanged.connect(self.updateCheckBox)

        self.delaySpinBoxLabel = QtGui.QLabel("Screenshot Delay:")

        self.hideThisWindowCheckBox = QtGui.QCheckBox("Hide This Window")
        self.hideThisWindowCheckBox.setChecked(True)
        
        self.areaLabel = QtGui.QLabel("Area: fullscreen")

        optionsGroupBoxLayout = QtGui.QGridLayout()
        optionsGroupBoxLayout.addWidget(self.delaySpinBoxLabel, 0, 0)
        optionsGroupBoxLayout.addWidget(self.delaySpinBox, 0, 1)
        optionsGroupBoxLayout.addWidget(self.hideThisWindowCheckBox, 1, 0)
        optionsGroupBoxLayout.addWidget(self.areaLabel, 1, 1)
        self.optionsGroupBox.setLayout(optionsGroupBoxLayout)

    def createButtonsLayout(self):
        self.selectAreaButton = self.createButton("Select Area",
                self.selectArea)

        self.newScreenshotButton = self.createButton("New Screenshot",
                self.newScreenshot)

        self.saveScreenshotButton = self.createButton("Save Screenshot",
                self.saveScreenshot)

        self.quitScreenshotButton = self.createButton("Quit", self.close)

        self.buttonsLayout = QtGui.QHBoxLayout()
        self.buttonsLayout.addStretch()
        self.buttonsLayout.addWidget(self.selectAreaButton)
        self.buttonsLayout.addWidget(self.newScreenshotButton)
        self.buttonsLayout.addWidget(self.saveScreenshotButton)
        self.buttonsLayout.addWidget(self.quitScreenshotButton)

    def createButton(self, text, member):
        button = QtGui.QPushButton(text)
        button.clicked.connect(member)
        return button

    def updateScreenshotLabel(self):
        self.screenshotLabel.setPixmap(self.originalPixmap.scaled(
                self.screenshotLabel.size(), QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation))


if __name__ == '__main__':

    import sys

    #TODO horrible 2/2 !
    if len(sys.argv) == 2 and sys.argv[1] == '-A':
        # Grab the display while hiding stdout to work around https://bugs.launchpad.net/listen/+bug/561707
        stdout = sys.stdout
        sys.stdout = StringIO()
        d = display.Display()
        sys.stdout = stdout
        XSelect(d)
    else:
        app = QtGui.QApplication(sys.argv)
        screenshot = Screenshot()
        screenshot.show()
        sys.exit(app.exec_())
