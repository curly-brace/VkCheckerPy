#!/usr/bin/python3
# -*- coding: utf-8 -*-

import webbrowser

from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.uic import loadUi


class MainWindow(QDialog):

    def __init__(self):
        super().__init__()

        self.win = loadUi('window.ui', self)
        self.show()

        self.win.loadGroupsBtn.clicked.connect(self.load_groups)
        self.win.saveGroupsBtn.clicked.connect(self.save_groups)
        self.win.selectAllBtn.clicked.connect(self.select_all)
        self.win.selectNoneBtn.clicked.connect(self.select_none)
        self.win.commentsList.itemDoubleClicked.connect(self.show_comment)

        self.get_comments_groups = self.win.getCommGrpBtn
        self.get_discussions_groups = self.win.getDiscGrpBtn
        self.get_comments = self.win.getCommentsBtn
        self.get_discussions = self.win.getDiscussionsBtn

    def get_target(self):
        return self.win.targetTxt.text()

    def add_group(self, text, data):
        item = QListWidgetItem(text)
        item.setToolTip(str(data))
        self.win.groupsList.addItem(item)

    def clear_groups(self):
        self.win.groupsList.clear()

    def add_comment(self, text, url):
        item = QListWidgetItem(text)
        item.setStatusTip(url)
        self.win.commentsList.addItem(item)

    def clear_comments(self):
        self.win.commentsList.clear()

    def set_grp_progress(self, cur, total):
        self.win.groupsLbl.setText('Group {}/{}'.format(cur, total))
        self.win.groupsBar.setValue((cur/total)*100)

    def set_post_progress(self, cur, total):
        self.win.postsLbl.setText('Post {}/{}'.format(cur, total))
        self.win.postsBar.setValue((cur/total)*100)

    def load_groups(self):
        fname = QFileDialog.getOpenFileName(self, 'Load Groups')[0]
        print(fname)
        if len(fname) > 0:
            with open(fname, 'r') as f:
                self.clear_groups()
                lines = f.readlines()
                for i in lines:
                    l = i.split('((separator_nah))')
                    self.add_group(l[0], l[1][:-1])

    def save_groups(self):
        fname = QFileDialog.getSaveFileName(self,'Save Groups')[0]

        if len(fname) > 0:
            with open(fname, 'w') as f:
                for i in range(self.win.groupsList.count()):
                    f.write('{}((separator_nah)){}\n'.format(self.win.groupsList.item(i).text(), self.win.groupsList.item(i).toolTip()))

    def select_all(self):
        for i in range(self.win.groupsList.count()):
            self.win.groupsList.item(i).setSelected(True)

    def select_none(self):
        for i in range(self.win.groupsList.count()):
            self.win.groupsList.item(i).setSelected(False)

    def get_selected_groups(self):
        groups = []
        for i in range(self.win.groupsList.count()):
            if self.win.groupsList.item(i).isSelected():
                groups.append([self.win.groupsList.item(i).toolTip(), self.win.groupsList.item(i).text()])
        return groups

    def show_comment(self):
        url = self.win.commentsList.item(self.win.commentsList.currentRow()).statusTip()
        print(url)
        webbrowser.open_new(url)
