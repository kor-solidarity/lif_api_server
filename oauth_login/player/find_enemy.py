from .views import *
from oauth_login import app, login_manager, db
from flask_login import login_required, login_user, logout_user, current_user
from ..o_auth import OAuthSignIn
from flask import redirect, url_for, flash, render_template, request
from ..player.models import *

from ..constants import *
from .pwd import *

import json
import random

"""
이 페이지의 목적: 멀티 상대방 찾는거. 


"""


# @login_required
@app.route('/find_enemy')
def find_enemy():
    """

    player_highscore 를 기준으로.
    거리 사용시간
    같은 크루 안됨.
    같은 레벨...? - 없으면 위로 하나 없으면 아래로 하나씩 확인해본다.

    :return:
    """

    # 플레이어
    player = Player.query.filter_by(user_id=current_user.id).first()

    # 타크루 모두 뽑는다.
    # other_players = Player.query.filter(Player.affiliated_crew_id != player.affiliated_crew_id).all()

    other_players = Player.query.filter(Player.affiliated_crew_id != 1).all()
    print('find')
    the_list = []
    for o in other_players:
        other_guy = {}
