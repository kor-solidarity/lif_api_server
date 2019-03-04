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
개발·투자 관련 일체. 
views에 다 넣으니 천줄이 넘어가는지라 좀 쪼개야할듯.
여기에 들어와야 하는거. 

"""


# 돈벌기 투자 관련.
# 투자버튼 누르면 이거 발동. research와 동일. 돈 버전인거.
@app.route('/make_money/')
@login_required
def make_money():
    """
    돈 투자 관련 코드.

    :return:
    """
    # 플레이어
    player = Player.query.filter_by(user_id=current_user.id).first()
    print('player: ', player.id)

    # 확인1. 플레이어가 존재하는가?
    # 사실 여기서 필터되면 애초에 여기까지 오면 안되는거.
    if not player:
        del player
        print("return error(ERR_NO_CHAR)")
        return error(ERR_NO_CHAR)

    """
    aĵoj por ĉeko

    - ID * 
    - crew*
    - queue*
    - used_items*
    """

    income_id = request.args.get('id')

    # 시키려는 작업의 아이디가 없는 경우.
    if not income_id:
        return error(ERR_NOT_FOUND)

    # 해당 오브젝트
    income_obj = IncomeTab.query.filter_by(id=income_id).first()

    # se ne havas objekton... ERROR!
    if not income_obj:
        return error(ERR_NOT_FOUND)

    print("income_obj.crew", income_obj.crew)
    # 해당 인컴에 전용 크루가 존재하고 플레이어가 그 크루에 소속되있는가?
    if income_obj.crew != 0:
        if income_obj.crew != player.affiliated_crew_id:
            return error(ERR_NOT_A_MEMBER)

    # queue doing this income thingy
    cash_queue = QueueCash.query \
        .filter_by(player_unique_id=player.player_unique_id).all()

    print('cash_queue', cash_queue)

    # 투자는 한번에 최대 5개까지만 허용
    # 기본 1개, 플레이어가 최대 5개까지 살 수 있는거.
    if len(cash_queue) >= player.money_workers:
        return error(ERR_QUEUE_FULL)

    player_mono = PlayerCash.query.filter_by(player_unique_id=player.player_unique_id).first()

    print(player_mono)

    # 써야하는 재화 확인. 이때 돈은 json형태의 string이기에 파싱해줘야 한다.
    # {"player_currency_manpower":3000
    # , "player_currency_scrap":1200, "player_currency_net":5000}
    money_json = income_obj.used_money
    money_json = json.loads(money_json)
    print(money_json)
    # for i in money_json.keys():
    #     cash = money_json[i]

    # 각각 재화 확인. 하드코딩 별로긴 한데 우선 당장 답이...
    if money_json['player_currency_manpower'] > 0:
        if money_json['player_currency_manpower'] > player_mono.player_currency_manpower:
            return error(ERR_NOT_ENOUGH_CASH)

    if money_json['player_currency_scrap'] > 0:
        if money_json['player_currency_scrap'] > player_mono.player_currency_scrap:
            return error(ERR_NOT_ENOUGH_CASH)

    if money_json['player_currency_net'] > 0:
        if money_json['player_currency_net'] > player_mono.player_currency_net:
            return error(ERR_NOT_ENOUGH_CASH)

    # if went to this stage there is the late gate: is the condition met?
    # 조건 - 레벨, 크루.
    condition = income_obj.condition

    # 없으면 0이라서...
    if condition != '0':
        condition = json.loads(condition)

        # 크루가 존재하면?
        if condition[CREW_ID]:
            if condition[CREW_ID] != player.affiliated_crew_id:
                return error(ERR_NOT_A_MEMBER)
        # 랭킹이 존재하면?
        if condition[PLAYER_RANK]:
            if condition[PLAYER_RANK] > player.player_rank:
                error(ERR_LOW_RANK)

    # 여기까지 왔으면 다 통과. 이제 적용한다.
    # 플레이어 재정 템에맞춰 떨군다.
    player_mono.player_currency_scrap \
        = player_mono.player_currency_scrap - money_json['player_currency_scrap']
    player_mono.player_currency_manpower \
        = player_mono.player_currency_manpower - money_json['player_currency_manpower']
    player_mono.player_currency_net \
        = player_mono.player_currency_net - money_json['player_currency_net']

    # 떨궜으면 이제 큐에 넣는다.
    cash_queue_add = QueueCash(player.player_unique_id, income_id, income_obj.time_to_finish)

    db.session.add(cash_queue_add)
    db.session.commit()

    return error(OK)


@app.route('/check_invest/')
@login_required
def check_that_goddamn_money():
    """
    리서치 채워지는것처럼 투자 채워지는거.
    same with check_that_goddamn_research() below.
    difference: money. not research.

    :return:
    """

    player = Player.query.filter_by(user_id=current_user.id).first()
    # 투자돼있는 쿼리 목록
    invest_query = QueueCash.query.filter_by(player_unique_id=player.player_unique_id)

    # 반환될 투자목록
    return_list = {'current_research': []}

    # run all of them in loop.
    for rl in invest_query:
        print('check2')
        nuntempo = datetime.datetime.utcnow()
        # 투자연구시간이 끝났는지?
        if nuntempo > rl.time_to_finish:
            # if so, then it's complete!

            # 완료됬다고 통보한다. 확인하기 위한 템의 정보 로딩.
            income_tab = IncomeTab.query.filter_by(id=rl.income_id).first()
            pluso = {'id': income_tab.id,
                     'name': income_tab.name,
                     'time_to_finish': rl.time_to_finish.isoformat(),
                     'research_done': 1}

            # 재화 추가한다.
            money_json = income_tab.earned_money
            money_json = json.loads(money_json)

            player_cash = PlayerCash.query\
                .filter_by(player_unique_id=player.player_unique_id).first()

            if money_json['player_currency_manpower'] > 0:
                player_cash.player_currency_manpower += money_json['player_currency_manpower']

            if money_json['player_currency_scrap'] > 0:
                player_cash.player_currency_scrap += money_json['player_currency_scrap']

            if money_json['player_currency_net'] > 0:
                player_cash.player_currency_net += money_json['player_currency_net']

            # 추가될 아이템(있으면)
            add_item = None

            # 만일 템이 있으면 추가한다.
            item_json = income_tab.earned_items
            if item_json != '0':
                item_json = json.loads(item_json)

                for i in item_json.keys():
                    # i == item ID
                    print('item_json.keys()', i)
                    an_item = Items.query.filter_by(id=i).first()
                    player_item = PlayerItem.query.filter_by(item_id=i).first()

                    # 이미 갖고있는 템이 아닌 경우 >> 생성한다.
                    if not player_item:
                        # 받는 템이 보드가 아닌 경우. 아닌경우와 따로 놔야한다.
                        if not an_item.is_board:
                            add_item = PlayerItem(player.player_unique_id, i, item_json[i], 0, 0)

                        # 보드인 경우.
                        else:
                            add_item = PlayerItem(player.player_unique_id, i, item_json[i]
                                                  , an_item.board_health, 1)
                    # 이미 갖고있는 템일 시.
                    else:
                        if not an_item.is_board:
                            player_item.item_quantity += item_json[i]
                        else:
                            # 보드를 얻는 경우면 이미 있으면? 기존 보드 체력만 만땅해줌.
                            player_item.item_health = an_item.board_health

            # 넣고 _player_queue_items쪽 없앤다.
            db.session.delete(rl)
            if add_item:
                db.session.add(add_item)
            print('check3')
            db.session.commit()
        else:
            # 시간이 더 필요할 시 남은시간을 한번 더 불러온다.
            income_tab = IncomeTab.query.filter_by(id=rl.income_id).first()
            pluso = {'id': income_tab.id,
                     'name': income_tab.name,
                     'time_to_finish': rl.time_to_finish.isoformat(),
                     'research_done': 0}

        # 결과값 반환
        return_list['current_research'].append(pluso)

    print(return_list)

    return_list.update(add_ok())
    return json.dumps(return_list, ensure_ascii=False)


@app.route('/invest_list')
@login_required
def invest_list():
    """
    플레이어의 크루가 쓸 수 있는 투자목록 반환.

    :return:
    """
    all_list = {'invest_list': []}
    # player = Player.query.filter_by(user_id=current_user.id).first()
    invests = IncomeTab.query.all()
    for i in invests:
        obj = {'id': i.id, 'name': i.name, 'used_money': i.used_money, 'earned_money': i.earned_money,
               'earned_items': i.earned_items, 'condition': i.condition, 'crew': i.crew,
               'time_to_finish': i.time_to_finish}
        all_list['invest_list'].append(obj)

    return json.dumps(all_list, ensure_ascii=False)


@app.route('/check_research/')
@login_required
def check_that_goddamn_research():
    """
    checks the research status of the player - all type.
    :return:
    """

    """
    this area checks if the player's research is done.
    and if it's done, update it gets that all recorded in the DB

    1. id
    2. see the time and look if it's done.
    3. if the time is passed, 
        then it's time to get rid of that on the table and apply it to player


    """
    print('check1, current_user:{}'.format(current_user.id))
    # load player.
    player = Player.query.filter_by(user_id=current_user.id).first()

    # load user's research stats.
    research_list = QueueItem.query \
        .filter_by(player_unique_id=player.player_unique_id).all()

    # researched list to fill.
    # ĉi tiu listo bezonas:
    # 1. item_id, is_board, TTF, item name,
    return_list = {'current_research': []}

    # run all of them in loop.
    for rl in research_list:
        print('check2')
        nuntempo = datetime.datetime.utcnow()
        # did the time passed for t
        if nuntempo > rl.time_to_finish:
            # if so, then it's complete!

            # add result to _player_researched_items
            researched = ResearchedItems(player_unique_id=player.player_unique_id
                                         , item_id=rl.item_id)

            # 완료됬다고 통보한다.
            la_ajxo = Items.query.filter_by(id=rl.item_id).first()
            pluso = {'item_id': la_ajxo.id,
                     'time_to_finish': rl.time_to_finish.isoformat(),
                     'is_board': la_ajxo.is_board, 'research_done': 1}

            # 개발의 대상은 장비(equip, 게임중 등장하는 템)·보드만 해당이 된다.
            # 굳이 템 수량을 반영 할 필요가 없다. 연구하는 템은 수량개념이 없기 때문이다.
            db.session.add(researched)

            # 보드를 개발했을 경우 보드를 등록하고 체력을 넣어줘야 한다.
            if la_ajxo.is_board == 1:
                player_item = PlayerItem(player_unique_id=player.player_unique_id,
                                         item_id=la_ajxo.id, item_quantity=1,
                                         item_health=la_ajxo.board_health,
                                         is_board=la_ajxo.is_board)
                db.session.add(player_item)

            # 넣고 _player_queue_items쪽 없앤다.
            db.session.delete(rl)
            print('check3')
            db.session.commit()
        else:
            # se ankoraŭ bezonas pli tempon, redonas la refreŝigis kontenton.
            la_ajxo = Items.query.filter_by(id=rl.item_id).first()
            pluso = {'item_id': la_ajxo.id,
                     'time_to_finish': rl.time_to_finish.isoformat(),
                     'is_board': la_ajxo.is_board, 'research_done': 0}

        # 결과값 반환
        return_list['current_research'].append(pluso)
    print(return_list)
    return_list.update(add_ok())
    return json.dumps(return_list, ensure_ascii=False)


@app.route('/research/<type>/')
@login_required
def research(type):
    """
    템·재화를 얻기 위해 연구를 할 경우 실시.

    :param type: 타입은 크게 세종류: 재화, 아이템(아이템 안에서 보드인지 아닌지가 갈린다)

    :return:
    """
    # 타입이 없거나 틀린 경우. 에러발생
    if not type:
        print("return error(ERROR)")
        return error(ERROR)

    print("type", type, bool(type == 'item'))

    # 현재는 아이템만 활성화하면 되고 추후 나머지 다 돌려야함. - ...?? 뭔소리였지...
    # 재화돌리는거 다른걸로 돌아가는듯.
    if type == 'item':
        print('check0')
        # 아이템일 경우.
        item_id = request.args.get('item_id')

        """
        확인해야 하는 절차:
        . 플레이어가 존재하는가-
        . 연구하려는 대상 템이 존재하는가-
        . 플레이어의 랭크로 해당 템을 연구시킬 수 있는가-
        . 플레이어가 해당 템 연구를 이미 완료했는가-
        . 플레이어의 재화가 연구하기에 충분한가.-
        · JSON형태의 소모성 재료가 있는 경우 플레이어가 해당 템을 가지고 있는가?-
        . 호버보드인가 일반템인가?-
            ㄴ위에 따라 분류된 큐가 꽉 차있진 않은가?-
            ㄴ플레이어가 해당 템을 이미 연구 중인가-
        · 연구용 템이긴 한가(연구시간이 존재함? + 애초에 연구로 얻을 수 있는거임?)
        """
        # 플레이어
        player = Player.query.filter_by(user_id=current_user.id).first()
        print('player: ', player.id)

        # 확인1. 플레이어가 존재하는가?
        if not player:
            del player
            print("return error(ERR_NO_CHAR)")
            return error(ERR_NO_CHAR)

        # target_item
        target_item = Items.query.filter_by(id=item_id).first()

        # 확인: 연구하려는 대상 템이 존재하는가
        if not target_item:
            del target_item
            print('return error(ERR_NO_SUCH_ITEM)')
            return error(ERR_NO_SUCH_ITEM)

        # 확인: 플레이어의 랭크로 해당 템을 연구시킬 수 있는가?
        if player.player_rank < target_item.itm_rank:
            del player, target_item
            print('return error(ERR_LOW_RANK)')
            return error(ERR_LOW_RANK)

        # 확인: 플레이어가 해당 템 연구를 이미 완료했는가?
        player_research = ResearchedItems.query \
            .filter_by(player_unique_id=player.player_unique_id, item_id=item_id).first()
        if player_research:
            print('return error(ERR_ALREADY_EXIST)')
            return error(ERR_ALREADY_EXIST)

        # 플레이어 재화현황
        player_cash = PlayerCash.query.filter_by(player_unique_id=player.player_unique_id).first()

        print('player_cash', player_cash)

        # 재화는 충분한가?
        if player_cash.player_currency_scrap < target_item.itm_currency_scrap \
                or player_cash.player_currency_manpower < target_item.itm_currency_manpower \
                or player_cash.player_currency_net < target_item.itm_currency_net:
            del player_research, target_item, player, player_cash
            print('return error(ERR_NOT_ENOUGH_CASH)')
            return error(ERR_NOT_ENOUGH_CASH)

        # itm_currency_special이 존재하는가? (0 이 아닌가?)
        if target_item.itm_currency_special != '0':
            # 존재한다면 이 템들이 충분한지 확인한다.
            json_decoded = json.loads(target_item.itm_currency_special)
            print('json_decoded', json_decoded)
            # itm_currency_special에 명시된 아이템 아이디.
            for i in json_decoded.keys():
                try:
                    print('id:{0}, json_decoded[{0}]:{1}'.format(i, json_decoded[i]))
                    special_tem = Items.query.filter_by(id=i).first()
                    print("special_tem: {}".format(special_tem))
                    # 템이 있는지 확인
                    player_item = PlayerItem.query \
                        .filter_by(player_unique_id=player.player_unique_id, item_id=i).first()
                    # print(player_item.item_quantity)
                    # 플레이어의 템이 없나? 에러
                    if not player_item:
                        return error(ERR_NOT_ENOUGH_EQUIP)
                    # 템 자체는 가지고 있다. 근데 충분한 양의 물건이 존재하는가? 없으면 또 에러
                    if player_item.item_quantity < json_decoded[i]:
                        return error(ERR_NOT_ENOUGH_EQUIP)
                except Exception as e:
                    print(e)
                    return error(ERROR)

        # 연구하려는 템이 일반템인가 보드인가?
        # 보드가 아닌경우
        try:
            print('target_item.is_board ', target_item.is_board )
            if target_item.is_board == 0:
                # 구분문
                is_board = 0
                # 개발큐
                queue = QueueItem.query \
                    .filter_by(player_unique_id=player.player_unique_id, is_board=is_board).all()
                print("queue", queue)
                # 분류된 큐가 꽉 차있진 않은가? 그럼 개발안됨.
                if len(queue) >= 2:
                    del player_research, target_item, player, player_cash, queue
                    print('error(ERR_QUEUE_FULL)')
                    return error(ERR_QUEUE_FULL)
                else:
                    # 중복연구중인지 확인.
                    for q in queue:
                        # 중복된 아이디가 있으면 이미 있다고 오류반환.
                        if q.item_id == target_item.id:
                            del player_research, target_item, player, player_cash, queue
                            print('return error(ERR_ALREADY_EXIST)')
                            return error(ERR_ALREADY_EXIST)

            # 보드인 경우
            else:
                # 위와 전반적인 진행은 동일하다. 큐가 하나일뿐.
                is_board = 1
                queue = QueueItem.query \
                    .filter_by(player_unique_id=player.player_unique_id, is_board=is_board).first()
                # 큐가 있으면 여기서 끝.
                if queue:
                    del player_research, target_item, player, player_cash, queue
                    return error(ERR_QUEUE_FULL)
                else:
                    # 없으면 이미 개발했나 확인하고
                    check_dev = ResearchedItems.query\
                        .filter_by(player_unique_id=player.player_unique_id
                                   , item_id=target_item.id).first()
                    # 이미 했으면 이미 있다고 오류반환.
                    if check_dev:
                        del player_research, target_item, player, player_cash, queue
                        return error(ERR_ALREADY_EXIST)

            # final stage. is the item even researchable?
            if target_item.itm_time_to_build == 0:
                del player_research, target_item, player, player_cash, queue, is_board
                return error(ERR_UNRESEARCHABLE)
            # 크루·시즌템 같은건가? 이러면 연구대상 아님
            elif target_item.itm_crew or target_item.itm_season:
                return error(ERR_UNRESEARCHABLE)


            print('ch1')

            # 여기까지 왔으면 연구 실시.
            # todo cash flow records should be later added.
            to_research = QueueItem(player_unique_id=player.player_unique_id, item_id=item_id
                                    , is_board=is_board, ttf=target_item.itm_time_to_build)

            print('to_research', to_research)

            # 플레이어 재정 템에맞춰 떨군다.
            player_cash.player_currency_scrap \
                = player_cash.player_currency_scrap - target_item.itm_currency_scrap
            player_cash.player_currency_manpower \
                = player_cash.player_currency_manpower - target_item.itm_currency_manpower
            player_cash.player_currency_net \
                = player_cash.player_currency_net - target_item.itm_currency_net

            # 개발에 템소모가 있을 경우 템도 떨군다.
            if target_item.itm_currency_special != '0':
                for i in json_decoded.keys():
                    player_item.item_quantity = \
                        player_item.item_quantity - json_decoded[i]

            db.session.add(to_research)

            db.session.commit()

            # 현재 연구중인 목록, 뭘 연구하고 있냐에 따라 보드만 뽑을지 아이템만 뽑을지 확인.
            research_list = QueueItem.query \
                .filter_by(player_unique_id=player.player_unique_id, is_board=is_board)

            # 이 시점까지 들어왔으면 연구반영은 끝. 이제 이에 갱신을 해야함.
            # 반환해야 하는 것: 연구템 목록: 템 id, 연구·제작 완료시간
            print("check2")
            # 반환할 목록
            json_string = []
            # sample = {'name':0, 'desc':1, 'itm_image': 2, 'eff':{'1':0, '2':2}}
            for r in research_list:
                # 대상 아이템
                la_ajxo = Items.query.filter_by(id=r.item_id).first()
                pluso = {'id': la_ajxo.id
                    , 'time_to_finish': r.time_to_finish.isoformat()}
                json_string.append(pluso)
            # cash
            # todo 캐시 반영도 해야하고... 개발용 소모템은?
            player_mono_inf = \
                {CASH: {'player_currency_scrap': player_cash.player_currency_scrap,
                        'player_currency_manpower': player_cash.player_currency_manpower,
                        'player_currency_net': player_cash.player_currency_net,
                        'player_currency_cash': player_cash.player_currency_cash}}

            # 소모템은... 유니티 단에서 건드는 걸로 하는게 나을듯.

            print(json_string)

            result = {'list':json_string}
            result.update(add_ok())
            return json.dumps(json_string, ensure_ascii=False)

        except Exception as e:
            import sys
            exc_type, exc_obj, tb = sys.exc_info()
            print('error at',  tb.tb_lineno)
            print(e)
            return error(ERROR)

    return error(ERROR)


@app.route('/init_stats/')
def init_list():
    """
    게임 첫 시작 시 아이템목록, 투자목록들 정보반환.
    음... 우선은 그렇게만.

    반환해야하는 목록: 아이템, 투자, 업적, 연구

    :return:
    """

    # todo 이거... 버전확인도 해야한다고 했던가? 아니 버전으로 확인한댔던가.
    # todo 모든게 다 로딩되게끔 바꿔야한다.
    item_obj = Items.query.all()

    item_list = []
    # only need to add tri aĵojn.
    # 여기에서
    for i in item_obj:
        item_dic = {'id': i.id, 'name': i.itm_name, 'desc': i.itm_desc,
                    'is_board': i.is_board, 'itm_currency_cash': i.itm_currency_cash}
        item_list.append(item_dic)

    print(item_list)

    investment_list = []

    # same stuff with above.
    invest_obj = IncomeTab.query.all()

    for i in invest_obj:
        invest_dic = {'id': i.id, 'name': i.name, 'condition': i.condition, 'used_money': i.used_money,
                      'earned_money': i.earned_money, 'earned_items': i.earned_items}
        investment_list.append(invest_dic)

    # 연구/개발목록은 필요가 없다. 모두 아이템에서 뽑아오니까.
    the_list = {'items': item_list, 'investments': investment_list}
    the_list.update(add_ok())
    return json.dumps(the_list, ensure_ascii=False)


# 버전 확인
@app.route('/check_version/')
def ch_version():

    version = Version.query.first()

    print(version)
    the_version = {'version': version.version}

    return json.dumps(the_version, ensure_ascii=False)


@app.route('/testing', methods=['GET', "POST"])
def testing_smth():
    if request.method == 'POST':
        post1 = request.form['post1']
        post2 = request.form['post2']
        return 'POST 방식, post1: {}, post2: {}'.format(post1, post2)
    else:
        get1 = request.args.get('get1')
        get2 = request.args.get('get2')
        return 'GET방식, get1: {}, get2: {}'.format(get1, get2)


# todo finish making immediate finish of item research or whatever.
# not needed.
@app.route('/rapidfin/<type>')
@login_required
def quick_item(type):
    """
    템 개발할 머시기들 즉시완료조치

    :return:
    """
    # 타입: 보드, 부착물, 일반템, 현찰
    player = Player.query.filter_by(user_id=current_user.id).first()

    num = request.args.get('item_num')

    # procedures:
    # 1. check if the item exist(duh) -
    # 2. check if the guy is researching this.
    # 3. check if the guy actually has an item

    # 종류별로 하나씩, - e.g. 보드용, 부착물용, 현찰용 등등등등
    # todo 현재 위에 명시된 세가지만 있고 추가 분명 해야할거임...

    # procedure 1 -
    # check if we got the value and actually have it
    if not num:
        return error(ERR_NO_VALUE)

    # 무슨종류인지 확인한 후 타입별로 나눈다.
    if type == 'board':
        item = Items.query.filter_by(id=num, is_board=1).first()
    #
    elif type == 'cash':
        item = IncomeTab.query.filter_by(id=num).first()
    elif type == 'item':
        item = Items.query.filter_by(id=num, is_board=0).first()
    else:
        return error(ERR_NOT_FOUND)

    # is there such item?
    if not item:
        return error(ERR_NOT_FOUND)
    print(item)
    # is the player researching this
    if type == 'cash':
        player_research = QueueCash\
            .query.filter_by(player_unique_id=player.player_unique_id
                             , income_id=num).first()
    else:
        player_research = QueueItem\
            .query.filter_by(player_unique_id=player.player_unique_id
                             , item_id=num).first()
    print(player_research)
    # is the player researching this
    if not player_research:
        return error(ERR_NO_SUCH_INVEST)

    # 여기까지 왔으면 이제 유료템을 갖고있는지 확인한다.
    # todo 추후 템이름 어떻게 정해야 하는지 확인해야 함. 현재는 임의등록.
    if type == 'board':
        finisher_item = PlayerItem\
            .query.filter_by(player_unique_id=player.player_unique_id
                             , item_id=1000).first()
    elif type == 'cash':
        finisher_item = PlayerItem\
            .query.filter_by(player_unique_id=player.player_unique_id
                             , item_id=3000).first()
    else:
        finisher_item = PlayerItem\
            .query.filter_by(player_unique_id=player.player_unique_id
                             , item_id=2000).first()

    # 유료템이 없거나 필요수량이 적으면 오류.
    # todo 현재는 필요수량은 그냥 1로 해둔다. 추후 반영필요
    if not finisher_item or finisher_item.item_quantity == 0:
        return error(ERR_NOT_ENOUGH_CASH)

    # 여기까지 왔으면 이제 준비는 다 됬음. 실제 반영을 하면 됨.
    # 추후 진짜 수정ㅎ야함...
    # 우선 해당 템을 없앤다.
    finisher_item.item_quantity -= 1

    # 종류에 따라 상이조치.
    if type == 'cash':
        # check_that_goddamn_money 참고. 똑같은 절차임.

        # 재화 추가한다.
        money_json = item.earned_money
        money_json = json.loads(money_json)

        player_cash = PlayerCash.query \
            .filter_by(player_unique_id=player.player_unique_id).first()

        if money_json['player_currency_manpower'] > 0:
            player_cash.player_currency_manpower += money_json['player_currency_manpower']

        if money_json['player_currency_scrap'] > 0:
            player_cash.player_currency_scrap += money_json['player_currency_scrap']

        if money_json['player_currency_net'] > 0:
            player_cash.player_currency_net += money_json['player_currency_net']

        # 추가될 아이템(있으면)
        add_item = None

        # 만일 템이 있으면 추가한다.
        item_json = item.earned_items
        if item_json != '0':
            item_json = json.loads(item_json)

            for i in item_json.keys():
                # i == item ID
                print('item_json.keys()', i)
                an_item = Items.query.filter_by(id=i).first()
                player_item = PlayerItem.query.filter_by(item_id=i).first()

                # 이미 갖고있는 템이 아닌 경우 >> 생성한다.
                if not player_item:
                    # 받는 템이 보드가 아닌 경우. 아닌경우와 따로 놔야한다.
                    if not an_item.is_board:
                        add_item = PlayerItem(player.player_unique_id, i, item_json[i], 0, 0)

                    # 보드인 경우.
                    else:
                        add_item = PlayerItem(player.player_unique_id, i, item_json[i]
                                              , an_item.board_health, 1)

                # 이미 갖고있는 템일 시. 근데 보드가 들어올일은 없다캄...
                else:
                    if not an_item.is_board:
                        player_item.item_quantity += item_json[i]
                    else:
                        player_item.item_health = an_item.board_health

        # 여기까지 왔으면 반영 다 된거니 끝.
        db.session.delete(player_research)
        if add_item:
            db.session.add(add_item)
        print('check3')
        db.session.commit()

    else:
        # 템일 경우는 뭐.. 위에 check_that_goddamn_research 와 동일.

        # add result to _player_researched_items
        researched = ResearchedItems(player_unique_id=player.player_unique_id
                                     , item_id=item.id)
        # 굳이 템 수량을 반영 할 필요가 없다. 연구하는 템은 수량개념이 없기 때문이다.
        db.session.add(researched)

        # 보드를 개발했을 경우 보드를 등록하고 체력을 넣어줘야 한다.
        if item.is_board == 1:
            player_item = PlayerItem(player_unique_id=player.player_unique_id
                                     , item_id=item.id, item_quantity=1
                                     , item_health=item.board_health
                                     , is_board=item.is_board)
            db.session.add(player_item)
        db.session.delete(player_research)
        db.session.commit()

    return error(OK)