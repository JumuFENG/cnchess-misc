# Python 3
# -*- coding: utf-8 -*-

from sql_helper.creator import create_sqlhelper

class ChessDb():
    def __init__(self):
        self.db = create_sqlhelper('sql_helper/db.config')
        
    def save_game(self, chess_game):
        if not self.db.is_exist_table('chess_qipu'):
            self.db.execute_sql_file('cnchess.sql')
            mxid = 0
        else:
            mxid, = self.db.select('chess_qipu', 'MAX(id)')
            if mxid is None:
                mxid = 0

        chess_info = {}
        chess_info['id'] = chess_game['id'] if 'id' in chess_game else mxid + 1
        chess_info['title'] = chess_game['title']
        if chess_game['binit'] is not None:
            chess_info['binit'] = chess_game['binit']
        if 'category' in chess_game:
            chess_info['category'] = chess_game['category']
        if 'tips' in chess_game:
            chess_info['tips'] = chess_game['tips']

        move_list_table = 'move_list_' + str(chess_info['id'])
        comments_table = 'comments_' + str(chess_info['id'])
        if len(chess_game['move_list']) > 0:
            self.save_move_list(move_list_table, chess_game['move_list'])
        if len(chess_game['comments']) > 0:
            self.save_comments(comments_table, chess_game['comments'])
        if self.db.is_exist_table_rows('chess_qipu', 'id=%s' % chess_info['id']):
            self.db.update('chess_qipu', chess_info, {'id':chess_info['id']})
        else:
            self.db.insert('chess_qipu', chess_info)

    def save_move_list(self, table, move_list):
        if not self.db.is_exist_table(table):
            max_step_len = 4 + len(max(move_list, key=lambda p: len(p['steps']))['steps'])
            self.db.create_table(table, {
                'id': 'INT NOT NULL DEFAULT 0',
                'baseid': 'INT NOT NULL DEFAULT 0',
                'start_node': 'INT NOT NULL DEFAULT 0',
                'steps': 'VARCHAR(%s) DEFAULT ""' % max_step_len
                }, 'PRIMARY KEY (id)')
        self.db.insert_many(table, datalist = move_list)

    def save_comments(self, table, comments):
        if not self.db.is_exist_table(table):
            max_comment_len = 4 + len(max(comments, key=lambda p: len(p['comment']))['comment'])
            self.db.create_table(table, {
                'id': 'INT AUTO_INCREMENT',
                'step_list_id': 'INT NOT NULL DEFAULT 0',
                'step': 'INT NOT NULL DEFAULT 0',
                'comment': 'VARCHAR(%s) DEFAULT ""' % max_comment_len
                }, 'PRIMARY KEY (id)')
        self.db.insert_many(table, datalist = comments)

    def get_all_qipu(self):
        if not self.db.is_exist_table('chess_qipu'):
            return None

        return self.db.select('chess_qipu', ['id', 'title'])

    def get_all_qipu_details(self):
        if not self.db.is_exist_table('chess_qipu'):
            return None

        all_game = self.db.select('chess_qipu', '*')
        for g in all_game:
            move_list_table = 'move_list_' + str(g['id'])
            g['move_list'] = self.db.select(move_list_table, '*') if self.db.is_exist_table(move_list_table) else []
            comments_table = 'comments_' + str(g['id'])
            g['comments'] = self.db.select(comments_table, '*') if self.db.is_exist_table(comments_table) else []
        return all_game

    def get_qipu(self, id):
        chess_game = self.db.select('chess_qipu', '*', 'id = %s' % id)[0]
        move_list_table = 'move_list_' + str(id)
        comments_table = 'comments_' + str(id)
        if self.db.is_exist_table(move_list_table):
            chess_game['move_list'] = self.db.select(move_list_table, '*')
        if self.db.is_exist_table(comments_table):
            chess_game['comments'] = self.db.select(comments_table, '*')
        return chess_game

if __name__ == '__main__':
    cd = ChessDb()
    # cd.save_game({'title':'test','binit':None, 
    #     'move_list':[{'id':0,'baseid':0,'start_node':0,'steps':'1234'},{'id':1,'baseid':0,'start_node':10,'steps':'2568'}],
    #     'comments':[{'step_list_id':0, 'step':15, 'comment':'test comment'}]})
    q = cd.get_all_qipu()
    print(q)