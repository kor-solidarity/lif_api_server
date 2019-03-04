import json
# 각종 반환값 모음.

# 정상실행됨
OK = 0

ERR_SAME_NICK = -1  # 중복별명
ERR_SAME_ID = -2  # 중복아이디
ERR_EMAIL_EXIST = -3  # 이메일 이미 존재
ERR_PWD_INCORRECT = -4  # 암호틀림
ERR_ID_INCORRECT = -4  # 아이디가 틀림. 굳이 위와 따로 분류할 필요는 없을듯.
ERR_NO_CREW = -5  # 선택한 크루는 존재하지 않음.
TOO_LONG = -6  # 뭔진 모르겠지만 입력한게 너무 길다.
ERR_NOT_LOGGED_IN = -7  # 로그인 안됨.
ERR_NO_CHAR = -8  # 캐릭터(Player 테이블) 생성 안함.
ERR_ALREADY_EXIST = -9  # 대상이 이미 존재함.
ERR_NOT_FOUND = -10  # 검색결과가 없음. 넣으려는 ID가 없다던지 등등

# 계정 연동로그인해야 하는데 일반로그인 시도하거나 정반대. 굳이 넣어야하나?
ERR_INCORRECT_AUTH = -11
ERR_NO_SUCH_ITEM = -12  # 찾으려는 아이템이 없음.
ERR_NO_SUCH_INVEST = -12  # 찾으려는 투자대상이 없음.
ERR_LOW_RANK = -13  # 랭크가 너무 낮아서 해당 작업을 못함.
ERR_NOT_ENOUGH_CASH = -14  # 재화부족, 어떤종류던간에.
ERR_NOT_ENOUGH_EQUIP = -15  # 부착물·부품 부족
ERR_QUEUE_FULL = -16  # 큐 꽉참.
ERR_UNRESEARCHABLE = -17  # 연구대상이 아님.
ERR_NOT_A_MEMBER = -18  # 해당 크루 소속이 아님

ERR_NO_VALUE = -20  # 값이 들어와야 하는데 안들어왔음
ERR_JSON_INCORRECT = -21  # JSON 형태의 파일 받아서 파싱시도하는데 JSON 형태가 아님.
ERR_NOT_HIGHSCORE = -22  # 최고점수 갱신하려는데 최고기록이 아니어서 반영이 안됨.

# 연동로그인 대상임.(네이버 또는 구글아이디) 인증메일 전송 최소화를 위한 조치.
ERR_NOT_USING_OAUTH = -50

ERROR = -100  # 그 외 모든 에러. 우선 임시로 둔거고 뭔 에런지 좀 찾아봐야함...

###############################
# 자료반환에 쓰일 각종 플레이어 칼럼명.
CASH = 'cash'
CREW_BOUNDARY = 'crew_boundary'
CREW_DESC = 'crew_desc'
CREW_ID = 'crew_id'
CREW_NAME = 'crew_name'
CREW_STATS = 'crew_stats'
CREW_LOGO = 'crew_logo'
FRIENDS = 'friends'
HIGHSCORE = 'highscore'
PLAYER_UNIQUE_ID = 'player_unique_id'
PLAYER_NICK = 'player_nick'
PLAYER_LVL = 'player_lvl'
PLAYER_EXP = 'player_exp'
PLAYER_RANK = 'player_rank'
PIC = 'pic'
RELATIONS = 'relations'  # 친구관계 확인용

get_and_post = ['GET', 'POST']

# 위에 오류 반환.
def error(code):
    """
    :param code:
    :return: {'error': <errnum>}
    """
    return json.dumps({'error': code})


def add_ok():
    """
    :return: {'error': OK}
    """
    return {'error': OK}
