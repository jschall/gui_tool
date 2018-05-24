#
# Copyright (C) 2016  UAVCAN Development Team  <uavcan.org>
#
# This software is distributed under the terms of the MIT License.
#
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import uavcan
from functools import partial
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel, QDialog, QSlider, QSpinBox, QDoubleSpinBox, \
    QPlainTextEdit
from PyQt5.QtCore import QTimer, Qt
from logging import getLogger
from ..widgets import make_icon_button, get_icon, get_monospace_font

__all__ = 'PANEL_NAME', 'spawn', 'get_icon'

PANEL_NAME = 'CANOpen Panel'


logger = getLogger(__name__)

_singleton = None


class ESCPanel(QDialog):
    #DEFAULT_INTERVAL = 0.1

    #CMD_BIT_LENGTH = uavcan.get_uavcan_data_type(uavcan.equipment.esc.RawCommand().cmd).value_type.bitlen
    #CMD_MAX = 2 ** (CMD_BIT_LENGTH - 1) - 1
    #CMD_MIN = -(2 ** (CMD_BIT_LENGTH - 1))

    def __init__(self, parent, node):
        super(ESCPanel, self).__init__(parent)
        self.setWindowTitle('CANOpen Panel')
        self.setAttribute(Qt.WA_DeleteOnClose)              # This is required to stop background timers!

        self._node = node

        self._buttons = [
            make_icon_button('play', 'Open handover bay', self, text='Open handover bay', on_clicked=self._do_open_handover),
            make_icon_button('play', 'Close handover bay', self, text='Close handover bay', on_clicked=self._do_close_handover),
            make_icon_button('hand-stop-o', 'E-stop', self, text='E-stop', on_clicked=self._do_estop)
        ]
        
        layout = QVBoxLayout(self)

        for b in self._buttons:
            layout.addWidget(b)

        self.setLayout(layout)
        self.resize(self.minimumWidth(), self.minimumHeight())

    def _do_estop(self):
        self._node._can_driver.send(0x605, b'\x23\x00\x24\x01\x01\x00\x00\x00')

    def _do_open_handover(self):
        self._node._can_driver.send(0x605, b'\x23\x00\x24\x01\x02\x00\x00\x00')
    
    def _do_close_handover(self):
        self._node._can_driver.send(0x605, b'\x23\x00\x24\x01\x03\x00\x00\x00')

    def __del__(self):
        global _singleton
        _singleton = None

    def closeEvent(self, event):
        global _singleton
        _singleton = None
        super(ESCPanel, self).closeEvent(event)


def spawn(parent, node):
    global _singleton
    if _singleton is None:
        _singleton = ESCPanel(parent, node)

    _singleton.show()
    _singleton.raise_()
    _singleton.activateWindow()

    return _singleton


get_icon = partial(get_icon, 'asterisk')
