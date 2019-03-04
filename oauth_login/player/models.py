from oauth_login import db
from flask_login import UserMixin
import datetime


"""
추가해야할 사항
크루 영역:
영역번호
영역이름
영역 점수 - 시즌 종료시 종합될 점수
크루별 가진 티켓(점수)
점령시 포상
오너팀 - 크루별 티켓 현황.
"""


class User(db.Model, UserMixin):
    __tablename__ = '_users'

    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.VARCHAR(50), nullable=False, unique=True)
    user_reg_date = db.Column(db.TIMESTAMP, nullable=False)
    last_login = db.Column(db.TIMESTAMP, nullable=True)
    passwd = db.Column(db.VARCHAR(80), nullable=True)
    social_id = db.Column(db.VARCHAR(80), nullable=True, unique=True)
    verified = db.Column(db.INTEGER, nullable=True)
    verified_date = db.Column(db.TIMESTAMP, nullable=True)

    def __init__(self, user_email, passwd, social_id, verified):
        self.user_email = user_email
        self.user_reg_date = datetime.datetime.utcnow()
        self.passwd = passwd
        self.social_id = social_id
        self.verified = verified
        if social_id:
            self.verified_date = datetime.datetime.utcnow()


class Player(db.Model):
    __tablename__ = '_players'

    id = db.Column(db.Integer, primary_key=True)
    player_unique_id = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('_users.id'))
    affiliated_crew_id = db.Column(db.Integer, db.ForeignKey('crew.id'))
    player_nick = db.Column(db.VARCHAR(50), unique=True)
    player_highscore = db.Column(db.Integer)
    player_badge = db.Column(db.VARCHAR(100))
    player_rank = db.Column(db.Integer)
    player_lvl = db.Column(db.Integer)
    player_exp = db.Column(db.Integer)
    money_workers = db.Column(db.Integer)

    def __init__(self, player_unique_id, user_id, affiliated_crew_id
                 , player_nick, player_lvl=1, player_exp=0):
        self.player_unique_id = player_unique_id
        self.user_id = user_id
        self.affiliated_crew_id = affiliated_crew_id
        self.player_nick = player_nick
        self.player_highscore = 0
        self.player_badge = 'testing'
        self.player_rank = 14
        self.player_lvl = player_lvl
        self.player_exp = player_exp
        self.money_workers = 1


class Crew(db.Model):
    __tablename__ = 'crew'

    id = db.Column(db.Integer, primary_key=True)
    crew_name = db.Column(db.VARCHAR(50))
    crew_desc = db.Column(db.TEXT)
    crew_boundary = db.Column(db.FLOAT)
    crew_exist = db.Column(db.Integer)
    crew_logo = db.Column(db.VARCHAR(100))

    def __init__(self, crew_name, crew_desc, crew_boundary, crew_logo, crew_exist=True):
        self.crew_name = crew_name
        self.crew_desc = crew_desc
        self.crew_boundary = crew_boundary
        self.crew_exist = crew_exist
        # 파일위치 손봐야함.
        self.crew_logo = crew_logo


class PlayerCash(db.Model):
    __tablename__ = '_players_cash'

    player_unique_id = db.Column(db.Integer, db.ForeignKey('_players.player_unique_id')
                                 , primary_key=True)
    player_currency_scrap = db.Column(db.Integer)
    player_currency_manpower = db.Column(db.Integer)
    player_currency_net = db.Column(db.Integer)
    player_currency_cash = db.Column(db.Integer)

    def __init__(self, unique_id, cash1=0, cash2=0, cash3=0, cash4=0):
        self.player_unique_id = unique_id
        self.player_currency_scrap = cash1
        self.player_currency_manpower = cash2
        self.player_currency_net = cash3
        self.player_currency_cash = cash4


class Items(db.Model):
    __tablename__ = 'items_equip'

    id = db.Column(db.Integer, primary_key=True)
    itm_name = db.Column(db.VARCHAR(50), nullable=False)
    itm_desc = db.Column(db.VARCHAR(500), nullable=False)
    itm_image = db.Column(db.VARCHAR(50), nullable=False)
    itm_time_to_build = db.Column(db.Integer)
    is_board = db.Column(db.Integer)
    is_researchable = db.Column(db.Integer)
    is_consumable = db.Column(db.Integer)
    board_health = db.Column(db.Integer)
    itm_crew = db.Column(db.Integer)
    itm_season = db.Column(db.Integer)
    itm_currency_scrap = db.Column(db.Integer)
    itm_currency_manpower = db.Column(db.Integer)
    itm_currency_net = db.Column(db.Integer)
    itm_currency_cash = db.Column(db.Integer)
    itm_currency_special = db.Column(db.VARCHAR(100), nullable=True)
    itm_rank = db.Column(db.Integer)
    itm_stat_0 = db.Column(db.Float)
    itm_stat_1 = db.Column(db.Float)
    itm_stat_2 = db.Column(db.Float)
    itm_stat_3 = db.Column(db.Float)
    itm_stat_4 = db.Column(db.Float)
    itm_stat_5 = db.Column(db.Float)
    itm_stat_6 = db.Column(db.Float)
    itm_stat_7 = db.Column(db.Float)
    itm_stat_8 = db.Column(db.Float)
    itm_stat_9 = db.Column(db.Float)
    itm_stat_10 = db.Column(db.Float)
    itm_stat_11 = db.Column(db.Float)
    itm_stat_12 = db.Column(db.Float)
    itm_stat_13 = db.Column(db.Float)
    itm_stat_14 = db.Column(db.Float)
    itm_stat_15 = db.Column(db.Float)
    itm_stat_16 = db.Column(db.Float)
    itm_stat_17 = db.Column(db.Float)
    itm_stat_18 = db.Column(db.Float)
    itm_stat_19 = db.Column(db.Float)
    itm_stat_20 = db.Column(db.Float)

    def __init__(self, name, desc, image, ttb, is_board, is_researchable, is_consumable, season,
                 scrap, manpower, net, cash, rank, crew, itm_stat_0, itm_stat_1,
                 itm_stat_2, itm_stat_3, itm_stat_4, itm_stat_5, itm_stat_6,
                 itm_stat_7, itm_stat_8, itm_stat_9, itm_stat_10, itm_stat_11,
                 itm_stat_12, itm_stat_13, itm_stat_14, itm_stat_15, itm_stat_16,
                 itm_stat_17, itm_stat_18, itm_stat_19, itm_stat_20, itm_currency_special=0):
        self.itm_name = name
        self.itm_desc = desc
        self.itm_image = image
        self.itm_time_to_build = ttb
        self.is_board = is_board
        self.is_researchable = is_researchable
        self.is_consumable = is_consumable
        self.itm_crew = crew
        self.itm_season = season
        self.itm_currency_scrap = scrap
        self.itm_currency_manpower = manpower
        self.itm_currency_net = net
        self.itm_currency_cash = cash
        self.itm_currency_special = itm_currency_special
        self.itm_rank = rank
        self.itm_stat_0 = itm_stat_0
        self.itm_stat_1 = itm_stat_1
        self.itm_stat_2 = itm_stat_2
        self.itm_stat_3 = itm_stat_3
        self.itm_stat_4 = itm_stat_4
        self.itm_stat_5 = itm_stat_5
        self.itm_stat_6 = itm_stat_6
        self.itm_stat_7 = itm_stat_7
        self.itm_stat_8 = itm_stat_8
        self.itm_stat_9 = itm_stat_9
        self.itm_stat_10 = itm_stat_10
        self.itm_stat_11 = itm_stat_11
        self.itm_stat_12 = itm_stat_12
        self.itm_stat_13 = itm_stat_13
        self.itm_stat_14 = itm_stat_14
        self.itm_stat_15 = itm_stat_15
        self.itm_stat_16 = itm_stat_16
        self.itm_stat_17 = itm_stat_17
        self.itm_stat_18 = itm_stat_18
        self.itm_stat_19 = itm_stat_19
        self.itm_stat_20 = itm_stat_20


class ResearchedItems(db.Model):
    __tablename__ = '_player_researched_items'

    id = db.Column(db.Integer, primary_key=True)
    player_unique_id = db.Column(db.Integer, db.ForeignKey('_players.player_unique_id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items_equip.id'))

    def __init__(self, player_unique_id, item_id):
        self.player_unique_id = player_unique_id
        self.item_id = item_id


class QueueItem(db.Model):
    __tablename__ = '_player_queue_items'

    id = db.Column(db.Integer, primary_key=True)
    player_unique_id = db.Column(db.Integer, db.ForeignKey('_players.player_unique_id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items_equip.id'))
    is_board = db.Column(db.Integer)
    time_to_finish = db.Column(db.TIMESTAMP)

    def __init__(self, player_unique_id, item_id, is_board, ttf):
        self.player_unique_id = player_unique_id
        self.item_id = item_id
        self.is_board = is_board
        seconds = datetime.timedelta(seconds=ttf)
        current_time = datetime.datetime.utcnow() + seconds
        self.time_to_finish = current_time


class QueueCash(db.Model):
    __tablename__ = '_player_queue_cash'

    id = db.Column(db.Integer, primary_key=True)
    player_unique_id = db.Column(db.Integer, db.ForeignKey('_players.player_unique_id'))
    income_id = db.Column(db.Integer, db.ForeignKey('items_equip.id'))
    time_to_finish = db.Column(db.TIMESTAMP)

    def __init__(self, player_unique_id, income_id, ttf):
        self.player_unique_id = player_unique_id
        self.income_id = income_id
        seconds = datetime.timedelta(seconds=ttf)
        current_time = datetime.datetime.utcnow() + seconds
        self.time_to_finish = current_time


class PlayerItem(db.Model):
    __tablename__ = '_player_items'

    id = db.Column(db.Integer, primary_key=True)
    player_unique_id = db.Column(db.Integer, db.ForeignKey('_players.player_unique_id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items_equip.id'))
    item_quantity = db.Column(db.Integer)
    item_health = db.Column(db.Integer)
    is_board = db.Column(db.Integer)

    def __init__(self, player_unique_id, item_id
                 , item_quantity, item_health, is_board):
        self.player_unique_id = player_unique_id
        self.item_id = item_id
        self.item_quantity = item_quantity
        self.item_health = item_health
        self.is_board = is_board


class IncomeTab(db.Model):
    __tablename__ = 'income_tab'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(50))
    used_money = db.Column(db.VARCHAR(200))
    earned_money = db.Column(db.VARCHAR(200))
    earned_items = db.Column(db.VARCHAR(100))
    condition = db.Column(db.VARCHAR(100))
    crew = db.Column(db.Integer)
    time_to_finish = db.Column(db.Integer)

    def __init__(self, name, used_money, earned_money, earned_items
                 , condition, crew_id, time_to_finish):
        self.name = name
        self.used_money = used_money
        self.earned_money = earned_money
        self.earned_items = earned_items
        self.condition = condition
        self.crew = crew_id
        self.time_to_finish = time_to_finish


class GameMap(db.Model):
    __tablename__ = "game_map"

    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer)
    area_name = db.Column(db.VARCHAR(50))
    area_pts = db.Column(db.Integer)
    reward = db.Column(db.VARCHAR(200))
    crew_ticket = db.Column(db.VARCHAR(100))
    is_playable = db.Column(db.Integer)
    hq_of = db.Column(db.Integer)

    def __init__(self, area_id, area_name, area_pts, reward, crew_ticket, is_playable, hq_of):
        self.area_id = area_id
        self.area_name = area_name
        self.area_pts = area_pts
        self.reward = reward
        self.crew_ticket = crew_ticket
        self.is_playable = is_playable
        self.hq_of = hq_of


class Version(db.Model):
    __tablename__ = 'gameinfo'

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.VARCHAR(50))


# 경험치 테이블
class ExpTable(db.Model):
    __tablename__ = 'exp_table'

    lvl = db.Column(db.Integer, primary_key=True)
    exp = db.Column(db.Integer)


# 기록
class Records(db.Model):
    __tablename__ = 'records_best'

    player_unique_id = db.Column(db.Integer, primary_key=True)
    time_stamp = db.Column(db.TIMESTAMP)
    record_score = db.Column(db.Integer)
    record_time = db.Column(db.Float)
    record_item = db.Column(db.VARCHAR(100))
    record_board = db.Column(db.Integer)
    record_stage = db.Column(db.Integer)
    record_barricade_1 = db.Column(db.TEXT)
    record_barricade_2 = db.Column(db.TEXT)
    record_barricade_3 = db.Column(db.TEXT)
    record_barricade_4 = db.Column(db.TEXT)
    record_barricade_5 = db.Column(db.TEXT)

    def __init__(self, player_unique_id, record_score, record_time, record_item,
                 record_board, record_stage, record_barricade_1, record_barricade_2,
                 record_barricade_3, record_barricade_4, record_barricade_5):
        self.player_unique_id = player_unique_id
        # 언제 기록된건지 기록.
        self.time_stamp = datetime.datetime.utcnow()
        self.record_score = record_score
        self.record_time = record_time
        self.record_item = record_item
        self.record_board = record_board
        self.record_stage = record_stage
        self.record_barricade_1 = record_barricade_1
        self.record_barricade_2 = record_barricade_2
        self.record_barricade_3 = record_barricade_3
        self.record_barricade_4 = record_barricade_4
        self.record_barricade_5 = record_barricade_5

