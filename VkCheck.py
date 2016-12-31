#!/usr/bin/python3
# -*- coding: utf-8 -*-

import MainWindow
import vk_api
import datetime
from PyQt5.QtWidgets import QApplication


class VkCheck:

    def __init__(self):
        self.win = MainWindow.MainWindow()

        login = ''
        password = ''
        vk_session = vk_api.VkApi(login, password)

        try:
            vk_session.authorization()
        except vk_api.AuthorizationError as error_msg:
            self.win.add_comment('auth error!', '')
            return

        self.vk = vk_session.get_api()
        self.target = 1

        self.win.get_comments_groups.clicked.connect(self.get_comments_groups)
        self.win.get_discussions_groups.clicked.connect(self.get_discussions_groups)
        self.win.get_comments.clicked.connect(self.get_comments)
        self.win.get_discussions.clicked.connect(self.get_discussions)

    def get_comments(self):
        self.target = self.vk.users.get(user_ids=self.win.get_target())[0]['id']
        self.win.clear_comments()
        groups = self.win.get_selected_groups()
        total_grp = len(groups)
        cur_grp = 0
        for group in groups:
            cur_grp += 1
            self.win.set_grp_progress(cur_grp, total_grp)

            posts = self.vk.wall.get(owner_id=-1*int(group[0]), count=100)
            total_posts = len(posts['items'])
            cur_post = 0
            group_name = group[1]
            group_name = (group_name[:8] + '..') if len(group_name) > 10 else group_name
            for post in posts['items']:
                cur_post += 1
                self.win.set_post_progress(cur_post, total_posts)

                if post['comments']['count'] == 0:
                    continue

                comments = self.vk.wall.getComments(owner_id=-1*int(group[0]), post_id=post['id'], count=100)
                total_comm = len(comments['items'])
                cur_comm = 0
                for comment in comments['items']:
                    cur_comm += 1
                    if comment['from_id'] == self.target:
                        url = 'https://vk.com/wall-{}_{}?reply={}'.format(group[0], post['id'], comment['id'])
                        date = datetime.datetime.fromtimestamp(int(comment['date'])).strftime('%d.%m.%y')
                        text = '[{}] {} ({}/{}) {}'.format(group_name, date, cur_comm, total_comm, comment['text'])
                        self.win.add_comment(text, url)
                    QApplication.processEvents()

    def get_discussions(self):
        self.target = self.vk.users.get(user_ids=self.win.get_target())[0]['id']
        self.win.clear_comments()
        groups = self.win.get_selected_groups()
        total_grp = len(groups)
        cur_grp = 0
        for group in groups:
            cur_grp += 1
            self.win.set_grp_progress(cur_grp, total_grp)

            group_name = group[1]
            group_name = (group_name[:8] + '..') if len(group_name) > 10 else group_name
            topics = self.vk.board.getTopics(group_id=group[0], count=100)
            total_topics = len(topics['items'])
            cur_topic = 0
            for topic in topics['items']:
                cur_topic += 1
                self.win.set_post_progress(cur_topic, total_topics)

                topic_id = topic['id']
                topic_name = topic['title']
                topic_name = (topic_name[:8] + '..') if len(topic_name) > 10 else topic_name
                total_comm = topic['comments']

                comments = self.vk.board.getComments(group_id=group[0], topic_id=topic_id, count=100, sort='desc')

                for comment in comments['items']:
                    if comment['from_id'] == self.target:
                        url = 'https://vk.com/wall-{}_{}?post={}'.format(group[0], topic_id, comment['id'])
                        date = datetime.datetime.fromtimestamp(int(comment['date'])).strftime('%d.%m.%y')
                        text = '[{}][{}] {} {}'.format(group_name, topic_name, date, comment['text'])
                        self.win.add_comment(text, url)
                    QApplication.processEvents()

    def get_comments_groups(self):
        self.target = self.vk.users.get(user_ids=self.win.get_target())[0]['id']

        self.win.clear_groups()
        self.win.clear_comments()

        grps = self.vk.groups.get(user_id=self.target)
        ids = ','.join(str(i) for i in grps['items'])
        groups = self.vk.groups.getById(group_ids=ids)
        total = len(groups)
        cur = 1
        for group in groups:
            try:
                post = self.vk.wall.get(owner_id=-1*group['id'], count=1)
                if post['count'] > 0:
                    post = post['items'][0]
                    if post['comments']['can_post'] == 1:
                        self.win.add_group(group['name'], group['id'])
            except vk_api.vk_api.ApiError:
                self.win.add_comment('{} seems closed'.format(group['name']), '')
            self.win.set_grp_progress(cur, total)
            cur += 1
            QApplication.processEvents()

    def get_discussions_groups(self):
        self.target = self.vk.users.get(user_ids=self.win.get_target())[0]['id']

        self.win.clear_groups()
        self.win.clear_comments()

        grps = self.vk.groups.get(user_id=self.target)
        ids = ','.join(str(i) for i in grps['items'])
        groups = self.vk.groups.getById(group_ids=ids)
        total = len(groups)
        cur = 1
        for group in groups:
            try:
                boards = self.vk.board.getTopics(group_id=group['id'], count=100)
                if boards['count'] > 0:
                    self.win.add_group(group['name'], group['id'])
            except vk_api.vk_api.ApiError:
                self.win.add_comment('{} seems closed'.format(group['name']), '')
            self.win.set_grp_progress(cur, total)
            cur += 1
            QApplication.processEvents()
