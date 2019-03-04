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
플레이 기록 저장
"""


@app.route('/record', methods=get_and_post)
def record():
    """
    플레이 기록 받으면 그게 최고기록을 갱신한 경우 넣는다.

    :return:
    """

    player = Player.query.filter_by(user_id=current_user.id).first()

    if not player:
        del player
        # print("return error(ERR_NO_CHAR)")
        return error(ERR_NO_CHAR)

    # 지금은 연습중이라 겟 포스트 방식 우선 둘다 넣음. 포스트로만 보내야 안전함.

    """
    존재하는거:
    점수, 깨는데 걸린 시간, 사용한 템 목록, 사용한 보드템 번호, 스테이지 번호?, 
    바리케이드 5종.
    """
    # # json을 뽑아본다.
    # try:
    #     # print('try')
    #     # 결과값은 무조건 포스트로 보낸다! 겟 쓰면 망함.
    #     res_json = json.loads(request.form['result'])
    # # json 코드에 에러가 발생한 경우(제대로된 json이 아닐 시.
    # except json.JSONDecodeError:
    #     return error(ERR_JSON_INCORRECT)
    # # 키에러 발생: 'result' 라는 변수가 아예 안들어왔다는 소리. 한마디로 결과값 반환이 안됨.
    # except KeyError:
    #     return error(ERR_NOT_FOUND)

    # 기존꺼 있나 확인.
    prev_rec = Records.query.filter_by(player_unique_id=player.player_unique_id).first()

    # return 'qwerty'
    # 테스트용
    res_json = json.loads("""{"record_score": 5154174, "record_time": 732.541, 
    "record_item": [ 5, 10, 8, 7, 2, 1, 3 ], "record_board": 15, "record_stage": 3241, 
    "record_barricade_1": [{"num": 1,  "stage_num": 3, "x_pos": 5.321,  "barricade_num": 3}, {"num": 2,  "stage_num": 3, "x_pos": 9.732,  "barricade_num": 5}, {"num": 3,  "stage_num": 3, "x_pos": 15.121,  "barricade_num": 2}], 
    "record_barricade_2": [{"num": 1,  "stage_num": 3, "x_pos": 5.321,  "barricade_num": 3}, {"num": 2,  "stage_num": 3, "x_pos": 10.1,  "barricade_num": 5}, {"num": 3,  "stage_num": 3, "x_pos": 15.21,  "barricade_num": 2}], "record_barricade_3": [{"num": 1,  "stage_num": 3, "x_pos": 5.321,  "barricade_num": 3}, {"num": 2,  "stage_num": 3, "x_pos": 8.31,  "barricade_num": 5}, {"num": 3,  "stage_num": 3, "x_pos": 15.321,  "barricade_num": 2}], "record_barricade_4": [{"num": 1,  "stage_num": 3, "x_pos": 5.321,  "barricade_num": 3}, {"num": 2,  "stage_num": 3, "x_pos": 11,  "barricade_num": 5}, {"num": 3,  "stage_num": 3, "x_pos": 15,  "barricade_num": 2}], "record_barricade_5": [{"num": 1,  "stage_num": 3, "x_pos": 5.321,  "barricade_num": 3}, {"num": 2,  "stage_num": 3, "x_pos": 10.921,  "barricade_num": 5}, {"num": 3,  "stage_num": 3, "x_pos": 15.521,  "barricade_num": 2}]}""")
    # print('rec')
    # print("res_json['record_score']", res_json['record_score'], type(res_json['record_score']))
    # print("res_json['record_item']", str(res_json['record_item']), type(str(res_json['record_item'])))
    # print("res_json['record_barricade_1']", res_json['record_barricade_1'], type(res_json['record_barricade_1']))

    # print('prev_rec', prev_rec)
    # 확인용도
    high_score = False
    # 만일 존재하면 점수를 비교한다.
    if prev_rec:
        # 만일 점수에서 신기록이 기존기록보다 높으면 기록을 진행한다.
        if prev_rec.record_score < res_json['record_score']:
            high_score = True
    # 기록이 아예 없으면 신기록이니 갱신.
    else:
        high_score = True
    # 기록갱신할 필요가 없으면 기록을 넣을 필요도 없으니.
    if not high_score:
        return error(ERR_NOT_HIGHSCORE)

    # 기존 값이 존재하면 수정
    if prev_rec:
        prev_rec.record_score = res_json['record_score']
        prev_rec.record_time = res_json['record_time']
        prev_rec.record_item = str(res_json['record_item'])
        prev_rec.record_board = res_json['record_board']
        prev_rec.record_stage = res_json['record_stage']
        prev_rec.record_barricade_1 = str(res_json['record_barricade_1'])
        prev_rec.record_barricade_2 = str(res_json['record_barricade_2'])
        prev_rec.record_barricade_3 = str(res_json['record_barricade_3'])
        prev_rec.record_barricade_4 = str(res_json['record_barricade_4'])
        prev_rec.record_barricade_5 = str(res_json['record_barricade_5'])

    # 존재하지 않으면 새로만든다.
    else:
        _record = Records(player.player_unique_id,
                          res_json['record_score'],
                          res_json['record_time'],
                          str(res_json['record_item']),
                          res_json['record_board'],
                          res_json['record_stage'],
                          str(res_json['record_barricade_1']),
                          str(res_json['record_barricade_2']),
                          str(res_json['record_barricade_3']),
                          str(res_json['record_barricade_4']),
                          str(res_json['record_barricade_5']))

    """
    record_score = 5154174 ;  // ( 점수 )
    record_time = 732.541 ;  // (초단위. 소수점 3자리까지)
    record_item = { 5, 10, 8, 7, 2, 1, 3 } ; // ( 선택한 아이템 아이디 )
    record_board = 15 ;  (보드 아이디 넘버)
    record_stage = 3241 ;   (스테이지 등장 순서 3번 2번 4번 1번 순서로 등장했을 경우.)
    record_barricade_1 =  ( 1번 장애물  - '스테이지 번호 : 3',  'x좌표 : 5.321',  '장애물 종류 넘버 : 3' ) , ( 2번 장애물  - '스테이지 번호 : 3',  'x좌표 : 8.5',  '장애물 종류 넘버 : 5' ) , ( 3번 장애물  - '스테이지 번호 : 3',  'x좌표 : 12.321',  '장애물 종류 넘버 : 2' ) , ~~~
    record_barricade_2 =  ( 1번 장애물  - '스테이지 번호 : 3',  'x좌표 : 5.321',  '장애물 종류 넘버 : 2' ) , ( 2번 장애물  - '스테이지 번호 : 3',  'x좌표 : 10.321',  '장애물 종류 넘버 : 5' ) , ( 3번 장애물  - '스테이지 번호 : 3',  'x좌표 : 12.314',  '장애물 종류 넘버 : 2' ) , ~~~
    record_barricade_3 =  ( 1번 장애물  - '스테이지 번호 : 3',  'x좌표 : 5.321',  '장애물 종류 넘버 : 0' ) , ( 2번 장애물  - '스테이지 번호 : 3',  'x좌표 : 9.314',  '장애물 종류 넘버 : 5' ) , ( 3번 장애물  - '스테이지 번호 : 3',  'x좌표 : 12.324',  '장애물 종류 넘버 : 2' ) , ~~~
    record_barricade_4 =  ( 1번 장애물  - '스테이지 번호 : 3',  'x좌표 : 5.321',  '장애물 종류 넘버 : 1' ) , ( 2번 장애물  - '스테이지 번호 : 3',  'x좌표 : 9.321',  '장애물 종류 넘버 : 5' ) , ( 3번 장애물  - '스테이지 번호 : 3',  'x좌표 : 12.214',  '장애물 종류 넘버 : 2' ) , ~~~
    record_barricade_5 =  ( 1번 장애물  - '스테이지 번호 : 3',  'x좌표 : 5.321',  '장애물 종류 넘버 : 4' ) , ( 2번 장애물  - '스테이지 번호 : 3',  'x좌표 : 11.34',  '장애물 종류 넘버 : 5' ) , ( 3번 장애물  - '스테이지 번호 : 3',  'x좌표 : 12.321',  '장애물 종류 넘버 : 2' ) , ~~~
    // 스테이지 번호 int, x좌표 float (소수점 3자리까지) , 장애물 종류 int. 
    장애물 개수는 스테이지 1개의 각 라인별로 500개 이하 
    = ( 스테이지 1개의 최대 장애물 개수는 500 * 5.  현재 평균 300 * 5개 이하. 
    스테이지 등장 개수는 4개 정도로 하기로 했는데 변경될수도 있음 )
    """
    print('add')
    if not prev_rec:
        db.session.add(_record)
    print('comm')
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return error(ERROR)

    return error(OK)

