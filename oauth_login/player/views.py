from .queues import *
from oauth_login import app, login_manager, db, mail, mail_serial
from flask_login import login_required, login_user, logout_user, current_user
from ..o_auth import OAuthSignIn
from flask import redirect, url_for, flash, render_template, request
from ..player.models import *
from ..constants import *
from .pwd import *
import json
import random
from flask_mail import Message


# PROLETOJ DE LA MONDO, UNUIĜU!
# todo 추후 관리자 페이지도 필요함.


def load_player():
    return Player.query.filter_by(user_id=current_user.id).first()


# the base page of the server.
# I really have nothing to put in here,
# so i think I could just try and add in anything?
@app.route('/')
def index():
    print(current_user)
    print(current_user.is_anonymous)
    if current_user.is_anonymous:
        print('anonymous_user')
    else:
        print('not anonymous_user')
    return render_template('index.html')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# 로그인 만들때.
@login_manager.unauthorized_handler
def unauthorized_callback():
    return error(ERR_NOT_LOGGED_IN)


@app.route('/is_server_on')
def is_server_on():
    return 'yes'


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    print('check1')
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    print('wtf2')
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        # if it's here it's just a failure it seems.
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        # todo 이건 어찌 넣는가??? 여기서 가입을 바로 하고 드가는거인듯.
        # 또한 이메일 중복에 대한 조치도 필요함.
        user = User(social_id=social_id, user_email=email, passwd=None, verified=1)
        db.session.add(user)
        db.session.commit()
    # todo 로그인 할 시 기록관리는 어떻게? 여기뿐 아니라 일반 로그인도 좀 생각해봐야 하는 부분.
    login_user(user, True)
    return redirect(url_for('index'))


@app.route('/logout/')
def logout():
    logout_user()
    # todo change this
    # return redirect(url_for('index'))
    return error(OK)


# 회원가입. 연동로그인이 아닐 시.
@app.route('/register/', methods=['POST', 'GET'])
def register_manually():
    """
    여기서 기초적인 회원가입을 실시한다.
    회원가입에 쓰일 테이블은 _users

    :return:
    """

    # af. 180524 - verification required. - NULLIFIED

    passwd = request.args.get('pwd')
    # 이메일이라고는 써져있지만 그냥 아이디. 이메일은 이제 안쓰고 단순 아이디로 가는상황.
    email = request.args.get('email')

    # 네이버·지메일은 연동로그인 대상임. 일반로그인으로 들어오려고 하면 안됨.
    # if ('naver.com' or 'gmail.com') in email.split('@')[1]:
    #     return error(ERR_NOT_USING_OAUTH)
    # print('pwd: {}, email: {}'.format(passwd, email))

    # 비번 암호화.
    passwd = crypt_pass(passwd)

    # 중복확인
    newb = User.query.filter_by(user_email=email).first()
    # 이메일이 존재한다?
    if newb:
        return error(ERR_EMAIL_EXIST)

    # 여기까지 온다면 끝. 오케이 리턴됨

    # encrypt mail.

    # token = mail_serial.dumps(email, salt='salt-upon_wounds')

# 이메일로 확인메세지 보내는거지만... 이제 안쓴다.
    try:
        user = User(user_email=email, passwd=passwd, social_id=None, verified=1)

        db.session.add(user)

        # 확인메일. 이제 안쓴다.
#         msg = Message('확인 메일', sender='autobot@LIFGAMES.com', recipients=[email])
#         link = url_for('confirm', token=token, _external=True)
#         welcome_html = \
#             '''<p>리프게임즈의 레일로드에 가입하신것을 환영합니다!</p>
# <p>계정을 활성화하려면 다음 링크를 클릭해주세요!</p>
# <a href="{0}">{0}</a>
# <p>링크를 클릭해도 아무 반응이 없으면 해당 링크를 복사해 브라우저 창에 붙여넣거나 직접 입력해주세요.</p>
# <p>감사합니다.</p>'''.format(link)
#
#         msg.html = welcome_html
#
#         mail.send(msg)

        db.session.commit()
        # 끝나면 이제 로그인.
        login_user(user, True)
    except Exception as e:
        db.session.rollback()

        print(e.args)
        print(e.__class__)
        print(e)

        return error(ERROR)

    return error(OK)


# 이메일 확인인데... 이제 의미가 없다.
@app.route('/confirm_email/<token>')
def confirm(token):

    email = mail_serial.loads(token, salt='salt-upon_wounds')

    the_user = User.query.filter_by(user_email=email).first()

    # todo 이거 고객들이 봐야하는거라 시각화 바꿔야함
    if not the_user:
        return error(ERR_NOT_A_MEMBER)

    the_user.verified = 1
    db.session.commit()

    return error(OK)


@app.route('/reg_player/', methods=['POST', 'GET'])
@login_required
def reg_player():
    """
    플레이어 등록.
    여기서 받아와야 하는 사항: 플레이어 닉, 소속크루 번호, 계정아이디

    보드1 equip3
    기본 템도 가지고 있는 상태로 시작해야 함.

    :return:
    """
    try:
        # 계정아이디
        user_num = current_user.id
        # print('userid: {}'.format(current_user.id))
        # 쓰려는 닉과 소속크루
        nick = request.args.get('nick')
        crew_id = request.args.get('crew_id')

        # print('nick: {} | crew {}'.format(nick, crew_id))

        # 크루 또는 별명등록이 안된 상태로 여기 들어왔을 경우. 애초에 클라에서 걸러져야함.
        if not nick or not crew_id:
            return error(ERR_NOT_FOUND)

        # is the id already made?
        user_exist = Player.query.filter_by(user_id=user_num).first()

        # 유저가 이미 존재하면 굳이 만들필요가 없음. 사실 걸리면 안됨.
        if user_exist:
            return error(ERR_SAME_ID)

        # 1. is same nick exist?
        # 2. does crew exist?
        # 3. if not, then go on.
        nick_exist = Player.query.filter_by(player_nick=nick).first()
        if nick_exist:
            del nick_exist
            return error(ERR_SAME_NICK)
        # 확인작업 끝나면 바로바로 삭제
        del nick_exist

        crew_exist = Crew.query.filter_by(id=crew_id, crew_exist=1).first()
        print(crew_exist)
        # does such crew exist? 없으면 잘못된거임.
        if not crew_exist:
            del crew_exist
            return error(ERR_NO_CREW)

        del crew_exist

        # 고유번호.
        unike_numbro = random.randint(1, 999000)

        unique_num_exist = Player.query.filter_by(player_unique_id=unike_numbro).first()

        counter = 0
        # 중복시 하나하나 확인해 더한다. 현재 상당히 엉성함.
        while unique_num_exist:
            counter += 1
            unike_numbro += 1
            print('caught!')
            # if counter > 10:
            #     unike_numbro += random.randint(1, 10)
            #     counter = 0
            unique_num_exist = Player.query.filter_by(player_unique_id=unike_numbro).first()

        del unique_num_exist

        print('user.id {}, user.user_email {}, user_reg_date {}, last_login {}'
              ', passwd {}, social_id {}'
              .format(current_user.id, current_user.user_email,
                      current_user.user_reg_date, current_user.last_login,
                      current_user.passwd, current_user.social_id))

        # 여기까지 들어오면 계정생성은 성공한거
        # todo 플레이어 뱃지는? 현재는 아무것도 없다!
        player = Player(player_unique_id=unike_numbro, user_id=user_num,
                        affiliated_crew_id=crew_id, player_nick=nick)
        # 재정현황도 추가.
        # todo 추후 기본값 설정해야한다.
        player_cash = PlayerCash(unike_numbro, 100000, 100000, 100000)

        # todo 추후 넣어야 하는 것:
        # 플레이어 도전과제
        # 플레이어

        db.session.add(player)
        db.session.add(player_cash)

        db.session.commit()

        return error(OK)

    except Exception as e:
        import sys

        exc_type, exc_obj, tb = sys.exc_info()
        print('error at', tb.tb_lineno)
        print(e)
        return error(ERROR)


# 로그인 시험.
@app.route('/login/')
def log_in(user_id=None, pwd=None, reg=False):
    """
    :param user_id:
    :param pwd:
    :param reg:
    위 세 변수는 회원가입 됐을 시 한정으로만 작동한다.
    :return:
    총 반환값:
    플레이어 이름, 플레이어 아이디, 소속크루 아이디, 모든 크루정보, 가진 재화현황.
    """

    """
    로그인은 두 종류가 존재함. 
    일반 로그인과 연동 로그인.
    일반 로그인의 경우 이 페이지에서 실질적인 로그인까지 다 담당한다. 
    연동 로그인의 경우 이 시점에서 이미 계정 자체는 로그인이 된 상태이므로
        플레이어 정보만 뽑아오면 된다. 
    """

    try:

        # 유저가 로그인한 상태일 경우(연동로그인 된 상태)
        if not current_user.is_anonymous:

            pass
        else:
            # 암호화된 암호문. 절대 평문으로 여기에 들어와선 안됨!!
            passwd = request.args.get('pwd')
            # 로그인할때 쓰는 이메일주소.
            email = request.args.get('email')
            print(email)
            print(passwd)

            if not passwd or not email:
                return error(ERR_ID_INCORRECT)

            # 이메일 존재하나 확인
            user_to_login = User.query.filter_by(user_email=email).first()

            if not user_to_login:
                del user_to_login
                return error(ERR_ID_INCORRECT)

            # 소셜아이디가 존재할 경우 그에맞는 연동로그인을 해야지 여기로 오면 안됨.
            if user_to_login.social_id:
                del user_to_login
                return error(ERR_INCORRECT_AUTH)

            # todo this MUST NOT be encrypted here. only temporary during mvp shit
            passwd = crypt_pass(passwd)

            # 걸리면 로그인 안된거
            if not passwd == user_to_login.passwd:
                del user_to_login
                return error(ERR_PWD_INCORRECT)

            # 여기까지 왔으면 로그인 준비 된거임.
            login_user(user_to_login, True)
            del user_to_login

        # 플레이어 정보
        player = Player.query.filter_by(user_id=current_user.id).first()

        # 플레이어 정보가 안뜬다는건 캐릭터를 안만들었다는 소리.
        if not player:
            print('no player???')
            # return error(ERR_NO_CHAR)

            # todo MVP상 임의 캐릭터가 생성된다. 실제 에선 위에 오류가 리턴되야함.
            reg_player(is_mvp=True)
            # 역시 MVP 전용으로만 생성되는 것이다.
            player = Player.query.filter_by(user_id=current_user.id).first()

        """
        여기서 이제 내와야 하는 자료:
        1. 플레이어 정보(별명, 아이디, 소속크루, 사진 등)
        2. 존재하는 모든 크루정보...? 
        3. 플레이어 친구목록
        4. 플레이어 재화목록
        
        """

        # 1. 플레이어 정보를 반환. 이때 필요한건 플레이어의 별명, 고유번호, 소속 크루번호,
        # todo 사진?? 현재는 없다
        player_json = {PLAYER_NICK: player.player_nick,
                       PLAYER_LVL: player.player_lvl,
                       PLAYER_EXP: player.player_exp,
                       PLAYER_UNIQUE_ID: player.player_unique_id,
                       CREW_ID: player.affiliated_crew_id}

        crew_inf = Crew.query.filter_by(crew_exist=1).all()
        # 모든 크루 내용물 드가야함.
        crew_json = {CREW_STATS: []}

        for ci in crew_inf:
            print(ci)

            ci_json = {CREW_NAME: ci.crew_name, CREW_DESC: ci.crew_desc,
                       CREW_BOUNDARY: ci.crew_boundary, CREW_LOGO: ci.crew_logo}
            crew_json[CREW_STATS].append(ci_json)
        # 크루내용 추가
        print('crew_json: {}'.format(crew_json))
        player_json.update(crew_json)

        # cash
        player_mono = PlayerCash.query.filter_by(player_unique_id=player.player_unique_id).first()
        player_mono_inf = \
            {CASH: {'player_currency_scrap': player_mono.player_currency_scrap,
                    'player_currency_manpower': player_mono.player_currency_manpower,
                    'player_currency_net': player_mono.player_currency_net,
                    'player_currency_cash': player_mono.player_currency_cash}}

        player_json.update(player_mono_inf)
        player_json.update(add_ok())
        # json.dumps == dic를 JSON.stringify형태로 변환시켜준다.
        stringify = json.dumps(player_json, ensure_ascii=False)

        print('type: {} | {}'.format(type(stringify), stringify))

        return stringify

    except Exception as e:
        import sys

        exc_type, exc_obj, tb = sys.exc_info()
        print('error at', tb.tb_lineno)
        print(e)
        return error(ERROR)


@app.route('/load_items/<item_type>')
@login_required
def load_items(item_type):
    """
    플레이어가 소지한 아이템 목록들을 불러온다.
    가라지 또는 보드현황을 열었을때 사용.

    :param item_type: garage|board
    :return:
    """

    # 아이템타입 명시가 안됬거나 가라지, 보드 외 값일 경우.
    if not item_type or not (item_type == 'garage' or item_type == 'board'):
        return error(ERROR)

    # load player.
    player = Player.query.filter_by(user_id=current_user.id).first()

    # 값 초기화
    la_items = []
    # 타입에 따라 뭘 불러올지 결정된다.
    if item_type == 'garage':
        la_items = PlayerItem.query \
            .filter_by(player_unique_id=player.player_unique_id, is_board=0).all()
    if item_type == 'board':
        la_items = PlayerItem.query \
            .filter_by(player_unique_id=player.player_unique_id, is_board=1).all()

    # 반환해야하는 아이템/보드 목록
    result_list = []

    for i in la_items:
        itemo = Items.query.filter_by(id=i.item_id).first()

        ajxo = {
            'id': itemo.id
        }

        if item_type == 'board':
            ajxo.update({'item_health': i.item_health})
        else:
            ajxo.update({'item_quantity': i.item_quantity})

        result_list.append(ajxo)

    result_dic = {'list': result_list}
    result_dic.update(add_ok())

    return json.dumps(result_dic, ensure_ascii=False)


@app.route('/load_research/')
@login_required
def load_research():
    # 어.... 완료된 연구목록과 현재 연구중인 목록이 뜨게 돼있음.
    """
    게임내 아이템 제작·연구창을 열 시 필요한 목록.
    나와야 하는 종류 : board|equip|consumable
    :return:
    """

    # load player.
    player = Player.query.filter_by(user_id=current_user.id).first()

    """
    반환되야 하는 목록:
    모든 부착물 -- 필요없을듯. 어차피 첫 로딩할때 다 빼오는데.... 
    연구완료한 템 목록:
    연구중인 목록 갱신.
    """

    # 연구다한것들
    researched_items = []
    # 현재 연구하고 있는 것들. 위에 연구현황 확인하는 함수를 그대로 쓴다.
    current_research = check_that_goddamn_research()
    # 위에 들어온건 스트링이기 때문에 별도로 JSON처럼 읽힐 수 있게끔 조치해야 한다.
    current_research = json.loads(current_research)

    # 연구대상 목록을 싹 다 가져온다.
    # items = Items.query.filter(Items.itm_time_to_build != 0).all()

    yeonguwanryo = ResearchedItems.query \
        .filter_by(player_unique_id=player.player_unique_id).order_by(ResearchedItems.item_id).all()

    # 연구완료 목록들 add.
    for i in yeonguwanryo:
        print(i)
        item = {'id': i.item_id}
        researched_items.append(item)

    # 반환될 JSON 목록
    result_json = {}

    # 현 연구중인 목록, 연구완료 목록들 추가.
    # result_json.update({'current_research': current_research})
    result_json.update(current_research)
    result_json.update({'completed_research': researched_items})
    result_json.update(add_ok())

    return json.dumps(result_json, ensure_ascii=True, sort_keys=True)


@app.route('/load_all_items/')
def load_all_items():
    """
    load ALL items for init.
    needs not to have logged in.
    :return:
    """
    # loading all items
    all_items = Items.query.all()

    item_list = []

    for la_ajxo in all_items:
        pluso = {'id': la_ajxo.id, 'itm_name': la_ajxo.itm_name,
                 'itm_desc': la_ajxo.itm_desc,
                 'itm_image': la_ajxo.itm_image,
                 'itm_time_to_build': la_ajxo.itm_time_to_build,
                 'is_board': la_ajxo.is_board,
                 'is_researchable': la_ajxo.is_researchable,
                 'is_consumable': la_ajxo.is_consumable,
                 'board_health': la_ajxo.board_health,
                 'itm_crew': la_ajxo.itm_crew,
                 'itm_season': la_ajxo.itm_season,
                 'itm_currency_scrap': la_ajxo.itm_currency_scrap,
                 'itm_currency_manpower': la_ajxo.itm_currency_manpower,
                 'itm_currency_net': la_ajxo.itm_currency_net,
                 'itm_currency_special': la_ajxo.itm_currency_special,
                 'itm_rank': la_ajxo.itm_rank,
                 'itm_stat': [la_ajxo.itm_stat_0, la_ajxo.itm_stat_1,
                              la_ajxo.itm_stat_2, la_ajxo.itm_stat_3,
                              la_ajxo.itm_stat_4, la_ajxo.itm_stat_5,
                              la_ajxo.itm_stat_6, la_ajxo.itm_stat_7,
                              la_ajxo.itm_stat_8, la_ajxo.itm_stat_9,
                              la_ajxo.itm_stat_10, la_ajxo.itm_stat_11,
                              la_ajxo.itm_stat_12, la_ajxo.itm_stat_13,
                              la_ajxo.itm_stat_14, la_ajxo.itm_stat_15,
                              la_ajxo.itm_stat_16, la_ajxo.itm_stat_17,
                              la_ajxo.itm_stat_18, la_ajxo.itm_stat_19,
                              la_ajxo.itm_stat_20]
                 }

        item_list.append(pluso)

    return_list = {'items': item_list}
    return_list.update(add_ok())

    return json.dumps(return_list, ensure_ascii=False)


@app.route('/load_crew/')
def load_crews():
    """
    크루 목록 반환. 로그인 후 캐릭 등록할때 필요함.
    :return:
    """

    crew_inf = Crew.query.filter_by(crew_exist=1).all()

    result_crew = []

    for i in crew_inf:
        a_crew = {'id': i.id, 'crew_name': i.crew_name, 'crew_desc': i.crew_desc,
                  'crew_boundary': i.crew_boundary, 'crew_exist': i.crew_exist,
                  'crew_logo': i.crew_logo}
        result_crew.append(a_crew)

    result_json = {'list': result_crew}
    result_json.update(add_ok())

    return json.dumps(result_json, ensure_ascii=True, sort_keys=True)


@app.route('/reward/')
@login_required
def result_renoviga():
    """
    게임 완료시 기록 갱신 관련.

    :return:
    """
    try:
        print('uuuuuuuuuugh')
        # todo 정확히 뭐뭐가 들어가는지 전혀 확인이 안되있음.

        player_currency_scrap = request.args.get('cashScrap')
        player_currency_manpower = request.args.get('cashMan')
        player_currency_net = request.args.get('cashNet')

        # numero de itemoj
        itm_json = request.args.get('itmJson')

        player_exp = request.args.get('exp')

        player = Player.query.filter_by(user_id=current_user.id).first()

        """
        - check for any cash increase and add
        - check if itmJSON is there
        - poste, 
        """

        player_cash = PlayerCash.query \
            .filter_by(player_unique_id=player.player_unique_id).first()

        # 재화 추가한다.
        if player_currency_scrap:
            player_cash.player_currency_scrap += int(player_currency_scrap)

        if player_currency_manpower:
            player_cash.player_currency_manpower += int(player_currency_manpower)

        if player_currency_net:
            player_cash.player_currency_net += int(player_currency_net)

        player_items = []

        print('player', player)

        # itm_json = '''{"3":1, "2":1}'''
        if itm_json:
            itm_json = json.loads(itm_json)
            print(itm_json)
            # 여기는 다 템을 먹는거다. tial, vi verigas la itemo, kaj
            for i in itm_json.keys():
                # ĉu la itemo ekzistas?
                item = Items.query.filter_by(id=i).first()
                # ne? pasu.
                if not item:
                    continue

                item_to_add = PlayerItem \
                    .query.filter_by(player_unique_id=player.player_unique_id,
                                     item_id=i).first()
                print(item_to_add)
                # do we have the item on the list? if yes, no need to add.
                if item_to_add:
                    item_to_add.item_quantity += itm_json[i]
                    db.session.commit()
                # if else, add one.
                else:
                    item_to_add = PlayerItem(player_unique_id=player.player_unique_id,
                                             item_id=i, item_quantity=itm_json[i],
                                             item_health=0, is_board=item.is_board)
                    db.session.add(item_to_add)
                    db.session.commit()

        if player_exp:
            player.player_exp += int(player_exp)
            # 경험치 천 넘기면 레벨업.
            # todo 이거 mvp한정임. 현재 랭크와 레벨은 똑같다. 이것도 나중에 바꿔야함.
            if player.player_exp >= 1000:
                player.player_lvl += 1
                player.player_rank += 1
                player.player_exp -= 1000
            db.session.commit()

        # todo 레벨??
        result_json = {'list': itm_json}
        result_json.update(add_ok())
        return json.dumps(itm_json, ensure_ascii=False)
    except Exception as e:
        print("ERROR AT REWARD: ", e)

        return error(ERROR)


@app.route('/see_able_items/')
@login_required
def see_usable_items():
    """
    플레이어가 쓸 수 있는 모든 아이템 목록을 불러온다.
    불러와지는 목록:
    - 기본적으로 쓸 수 있는 부착물
    - 플레이어가 연구 완료한 부착물

    :return:
    """

    # 플레이어 정보를 뺀다. 모든 로그인 관련 기본이지만 여튼...
    player = Player.query.filter_by(user_id=current_user.id).first()

    # 연구 끝났나 확인좀. 굳이 완료목록 뺄 필요는 없을듯?
    check_that_goddamn_research()

    # 뽑아올 아이템 목록:
    item_list = {"item_list": []}

    # 개발시간이 없고 보드가 아니고, 소모성이 아닌것들 == 기본 부착물.
    base_items = Items.query.filter_by(itm_time_to_build=0,
                                       is_board=0, is_consumable=0).all()

    for i in base_items:
        # item_list["item_list"].append({'item_id': i.id})
        item_list["item_list"].append(i.id)

    # 플레이어가 가진 개발완료된 템 목록.
    player_researched_items = ResearchedItems \
        .query.filter_by(player_unique_id=player.player_unique_id).all()

    # 여기에는 연구완료된 보드도 있을 수 있다.... 그거 필터링 해야함.
    for i in player_researched_items:
        an_item = Items.query.filter_by(id=i.item_id).first()

        # 만약 아이템이 보드인 경우 포함하지 않는다.
        if an_item.is_board == 1:
            player_researched_items.remove(i)

    # 필터 끝났으면 마저 넣는다.
    for i in player_researched_items:
        # item_list["item_list"].append({'item_id': i.item_id})
        item_list["item_list"].append(i.item_id)

    item_list.update(add_ok())
    return json.dumps(item_list, sort_keys=True)


@app.route('/see_invest')
@login_required
def see_invest():
    """
    소모재화 투자할 수 있는 방식들 내보내기.
    선택지는 조건에 부합하는 전체를 내보내는 것이 아니라 서너개(미정)만 뽑아서 준다.
    이때 조건:
    랭크제한, 크루에 따른 차이, 날자제한, 등등 - 추후 추가요망.

    :return: 해당 플레이어에 맞는 투자목록.
    """

