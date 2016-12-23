#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import VkCheck

from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)

    pc = VkCheck.VkCheck()

    sys.exit(app.exec_())
