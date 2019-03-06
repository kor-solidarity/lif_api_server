-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        10.2.9-MariaDB - mariadb.org binary distribution
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- lif_table 데이터베이스 구조 내보내기
DROP DATABASE IF EXISTS `lif_table`;
CREATE DATABASE IF NOT EXISTS `lif_table` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
USE `lif_table`;

-- 테이블 lif_table.crew 구조 내보내기
DROP TABLE IF EXISTS `crew`;
CREATE TABLE IF NOT EXISTS `crew` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '기초적인 관리번호',
  `crew_name` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '크루 이름...',
  `crew_desc` text COLLATE utf8_bin NOT NULL COMMENT '해당 클랜의 설명. 그냥 내용 다 드가게 합시다... ',
  `crew_boundary` float NOT NULL DEFAULT 0 COMMENT '시즌별에 필요한건데... 클랜간의 영역 점유율. 무조건 시즌별 클랜들 이 레이트 값이 100에 맞춰져야 한다. ',
  `crew_exist` int(11) NOT NULL DEFAULT 1 COMMENT '(현 운영중인 시즌에)존재하는 크루인가? 0이면 아님.',
  `crew_logo` varchar(100) COLLATE utf8_bin DEFAULT NULL COMMENT '크루로고 파일이름. 필요한가?',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='클랜같은거. NPC 콥.\r\n세부적인 내용이 여기에서 저장되는 일은 없다. 모두 번호로 분류되며 클라이언트 내에서 번호에 맞춰서 불려진다. \r\n*추가사항: 아이템?';

-- 테이블 데이터 lif_table.crew:~3 rows (대략적) 내보내기
DELETE FROM `crew`;
/*!40000 ALTER TABLE `crew` DISABLE KEYS */;
INSERT INTO `crew` (`id`, `crew_name`, `crew_desc`, `crew_boundary`, `crew_exist`, `crew_logo`) VALUES
	(1, 'yolo_crew', '1', 33.3333, 1, NULL),
	(2, 'second_crew', '2', 33.3333, 1, NULL),
	(3, '22223', '32', 33.3334, 1, NULL);
/*!40000 ALTER TABLE `crew` ENABLE KEYS */;

-- 테이블 lif_table.deal_rec 구조 내보내기
DROP TABLE IF EXISTS `deal_rec`;
CREATE TABLE IF NOT EXISTS `deal_rec` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '거래순번',
  `deal_time` timestamp NOT NULL DEFAULT current_timestamp() COMMENT '거래시각',
  `user_num` int(11) NOT NULL COMMENT '플레이어(유저 id)',
  `열 4` int(11) NOT NULL COMMENT '이하 추후 추가.',
  `열 5` int(11) NOT NULL,
  `열 6` int(11) NOT NULL,
  `열 7` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_deal_rec__users` (`user_num`),
  CONSTRAINT `FK_deal_rec__users` FOREIGN KEY (`user_num`) REFERENCES `_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='모든 거래내역';

-- 테이블 데이터 lif_table.deal_rec:~0 rows (대략적) 내보내기
DELETE FROM `deal_rec`;
/*!40000 ALTER TABLE `deal_rec` DISABLE KEYS */;
/*!40000 ALTER TABLE `deal_rec` ENABLE KEYS */;

-- 테이블 lif_table.exp_table 구조 내보내기
DROP TABLE IF EXISTS `exp_table`;
CREATE TABLE IF NOT EXISTS `exp_table` (
  `lvl` int(11) NOT NULL COMMENT '레벨',
  `exp` int(11) NOT NULL COMMENT '해당 레벨때 다음으로 넘길 시 필요한 경험치(1일 경우 2로 올라가는데까지 드는비용)',
  PRIMARY KEY (`lvl`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='레벨별 다음으로 가는데 얻어야 하는 경험치';

-- 테이블 데이터 lif_table.exp_table:~0 rows (대략적) 내보내기
DELETE FROM `exp_table`;
/*!40000 ALTER TABLE `exp_table` DISABLE KEYS */;
INSERT INTO `exp_table` (`lvl`, `exp`) VALUES
	(1, 1000);
/*!40000 ALTER TABLE `exp_table` ENABLE KEYS */;

-- 테이블 lif_table.gameinfo 구조 내보내기
DROP TABLE IF EXISTS `gameinfo`;
CREATE TABLE IF NOT EXISTS `gameinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '기본 id ',
  `version` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '버전명',
  `date` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '마지막 수정일자. 필요한가...?',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='게임정보, 근데 칼럼하나만 쓸듯.';

-- 테이블 데이터 lif_table.gameinfo:~0 rows (대략적) 내보내기
DELETE FROM `gameinfo`;
/*!40000 ALTER TABLE `gameinfo` DISABLE KEYS */;
INSERT INTO `gameinfo` (`id`, `version`, `date`) VALUES
	(1, '1.0', '2018-06-25 07:39:09');
/*!40000 ALTER TABLE `gameinfo` ENABLE KEYS */;

-- 테이블 lif_table.game_map 구조 내보내기
DROP TABLE IF EXISTS `game_map`;
CREATE TABLE IF NOT EXISTS `game_map` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `area_id` int(11) DEFAULT NULL COMMENT '지역 아이디. 위에 아이디랑 통합해야할까?',
  `area_name` varchar(50) COLLATE utf8_bin DEFAULT NULL COMMENT '구역명',
  `area_pts` int(11) DEFAULT NULL COMMENT '크루가 이 구역을 점령했을 시 얻는 점수',
  `reward` varchar(200) COLLATE utf8_bin DEFAULT NULL COMMENT '구역을 먹었을 시 얻는 템·재화 등',
  `crew_ticket` varchar(100) COLLATE utf8_bin DEFAULT NULL COMMENT '크루별 지역전 누적점수. 최종적으로 가장 점수많은애가 구역차지.',
  `is_playable` int(11) DEFAULT NULL COMMENT '이 지역에서 플레이가 가능한가?',
  `hq_of` int(11) DEFAULT NULL COMMENT '어느 크루의 본진?',
  `열 8` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='게임 내 영역에 대한 테이블.';

-- 테이블 데이터 lif_table.game_map:~0 rows (대략적) 내보내기
DELETE FROM `game_map`;
/*!40000 ALTER TABLE `game_map` DISABLE KEYS */;
/*!40000 ALTER TABLE `game_map` ENABLE KEYS */;

-- 테이블 lif_table.income_tab 구조 내보내기
DROP TABLE IF EXISTS `income_tab`;
CREATE TABLE IF NOT EXISTS `income_tab` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '기본 관리번호',
  `name` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '해당 투자의 명칭.',
  `used_money` varchar(200) COLLATE utf8_bin NOT NULL COMMENT '쓰일 돈. JSON으로 파싱하면 될듯??',
  `earned_money` varchar(200) COLLATE utf8_bin NOT NULL COMMENT '받을 돈. JSON으로 파싱하면 될듯? ',
  `earned_items` varchar(100) COLLATE utf8_bin NOT NULL COMMENT '받을 템. 해당사항 없을 시 0처리',
  `condition` varchar(100) COLLATE utf8_bin NOT NULL DEFAULT '0' COMMENT '발동조건. 조건없이 도는것도 있겠지만 있을경우 대비. 레벨과 크루 두종류.',
  `crew` int(11) NOT NULL DEFAULT 0 COMMENT '특정 크루만 할 수 있는가? 0이면 공통',
  `time_to_finish` int(11) NOT NULL COMMENT '완료하는데 드는 시간. 초단위.',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=502 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='게임 내 재화 투자 관련. ';

-- 테이블 데이터 lif_table.income_tab:~2 rows (대략적) 내보내기
DELETE FROM `income_tab`;
/*!40000 ALTER TABLE `income_tab` DISABLE KEYS */;
INSERT INTO `income_tab` (`id`, `name`, `used_money`, `earned_money`, `earned_items`, `condition`, `crew`, `time_to_finish`) VALUES
	(500, 'ㅎㅎㅎㅎ', '{"player_currency_manpower":100, "player_currency_scrap":120, "player_currency_net":500}', '{"player_currency_manpower":3500, "player_currency_scrap":1250, "player_currency_net":5500}', '0', '0', 0, 1000),
	(501, '1', '{"player_currency_manpower":10, "player_currency_scrap":10, "player_currency_net":10}', '{"player_currency_manpower":3500, "player_currency_scrap":1250, "player_currency_net":5500}', '{"10":5}', '0', 0, 3000);
/*!40000 ALTER TABLE `income_tab` ENABLE KEYS */;

-- 테이블 lif_table.items_equip 구조 내보내기
DROP TABLE IF EXISTS `items_equip`;
CREATE TABLE IF NOT EXISTS `items_equip` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'numbro de item-o. Ĉu mi devas klarigi ĉi tio?',
  `itm_name` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '등록할 아이템 이름',
  `itm_desc` varchar(500) COLLATE utf8_bin NOT NULL COMMENT '설명. 이게 게임상에서 무슨템인지 설명대사 띄우는거.',
  `itm_image` varchar(50) COLLATE utf8_bin NOT NULL COMMENT 'image name',
  `itm_time_to_build` int(11) NOT NULL DEFAULT 0 COMMENT '템 연구시 드는 시간(초단위). 0이면 연구없이 뜨는거',
  `is_board` int(11) NOT NULL DEFAULT 0 COMMENT '보드인가? 아니면 0. 이거랑 아래 is_consumable 둘다 0이면 부착물이라는 소리',
  `is_researchable` int(11) NOT NULL DEFAULT 0 COMMENT '연구용인 것인가?',
  `is_consumable` int(11) NOT NULL DEFAULT 0 COMMENT '소모성인가? 아니면 0. 이게 1인 경우 아래 모든 능력치가 무시되도 될듯',
  `board_health` int(11) NOT NULL DEFAULT 0 COMMENT '보드의 체력. 보드가 아니면 무시',
  `itm_crew` int(11) NOT NULL DEFAULT 0 COMMENT '어느 크루 소속인가? 0이면 크루템 아님',
  `itm_season` int(11) NOT NULL DEFAULT 0 COMMENT '무슨 시즌때 배포된 템? 0이면 시즌템이 아닌거.',
  `itm_currency_scrap` int(11) NOT NULL DEFAULT 0 COMMENT '각 템에는 제작하는데 드는 비용이 있다. 그 중 하나.',
  `itm_currency_manpower` int(11) NOT NULL DEFAULT 0 COMMENT '각 템에는 제작하는데 드는 비용이 있다. 그 중 하나.',
  `itm_currency_net` int(11) NOT NULL DEFAULT 0 COMMENT '각 템에는 제작하는데 드는 비용이 있다. 그 중 하나.',
  `itm_currency_cash` int(11) NOT NULL DEFAULT 0 COMMENT '캐시템일 경우 얼마짜린지 확인용도. 당연 원화겠지?',
  `itm_currency_special` varchar(100) COLLATE utf8_bin NOT NULL DEFAULT '0' COMMENT 'JSON 형태로 들어갈 소모품 재료 목록. 템 아이디로 확인. 예: {"1":2, "2":1}',
  `itm_rank` int(11) NOT NULL DEFAULT 0 COMMENT '랭크제한. 이 수치 이하면 사용 못하는거. 현재 MVP상에선 레벨도 이걸로 적용된다',
  `itm_stat_0` float NOT NULL DEFAULT 0 COMMENT '공격력',
  `itm_stat_1` float NOT NULL DEFAULT 0 COMMENT '가속도',
  `itm_stat_2` float NOT NULL DEFAULT 0 COMMENT '순간 가속도 - 판정시 가속?',
  `itm_stat_3` float NOT NULL DEFAULT 0 COMMENT '순간 가속 감속값 - 순간가속도가 초당 이 값만큼 감소',
  `itm_stat_4` float NOT NULL DEFAULT 0 COMMENT '최고 속도',
  `itm_stat_5` float NOT NULL DEFAULT 0 COMMENT '점프 상승 속도',
  `itm_stat_6` float NOT NULL DEFAULT 0 COMMENT '점프각도 변화값',
  `itm_stat_7` float NOT NULL DEFAULT 0,
  `itm_stat_8` float NOT NULL DEFAULT 0,
  `itm_stat_9` float NOT NULL DEFAULT 0,
  `itm_stat_10` float NOT NULL DEFAULT 0,
  `itm_stat_11` float NOT NULL DEFAULT 0,
  `itm_stat_12` float NOT NULL DEFAULT 0,
  `itm_stat_13` float NOT NULL DEFAULT 0,
  `itm_stat_14` float NOT NULL DEFAULT 0,
  `itm_stat_15` float NOT NULL DEFAULT 0,
  `itm_stat_16` float NOT NULL DEFAULT 0,
  `itm_stat_17` float NOT NULL DEFAULT 0,
  `itm_stat_18` float NOT NULL DEFAULT 0,
  `itm_stat_19` float NOT NULL DEFAULT 0,
  `itm_stat_20` float NOT NULL DEFAULT 0,
  `itm_stat_21` float NOT NULL DEFAULT 0,
  `itm_stat_22` float NOT NULL DEFAULT 0,
  `itm_stat_23` float NOT NULL DEFAULT 0,
  `itm_stat_24` float NOT NULL DEFAULT 0,
  `itm_stat_25` float NOT NULL DEFAULT 0,
  `itm_stat_26` float NOT NULL DEFAULT 0,
  `itm_stat_27` float NOT NULL DEFAULT 0,
  `itm_stat_28` float NOT NULL DEFAULT 0,
  `itm_stat_29` float NOT NULL DEFAULT 0,
  `itm_stat_30` float NOT NULL DEFAULT 0,
  `itm_chance` float NOT NULL DEFAULT 0 COMMENT '스테이지 클리어 시 아이템 뜰 확률',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3002 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='listo de ĉiuj itemoj en la ludo.\r\n모든 아이템은 id를 같은대로 공유한다. 관리 편의성 용도.\r\n템은 보드·부착물·소모품이 존재한다. \r\n부착물은 게임 중간중간에 얻는 템. 해당 판에서만 쓰이고 끝인 방식. \r\n소모품은 재료·티켓·등등......갯수가 있는것들. 연구대상이 아니다. ';

-- 테이블 데이터 lif_table.items_equip:~16 rows (대략적) 내보내기
DELETE FROM `items_equip`;
/*!40000 ALTER TABLE `items_equip` DISABLE KEYS */;
INSERT INTO `items_equip` (`id`, `itm_name`, `itm_desc`, `itm_image`, `itm_time_to_build`, `is_board`, `is_researchable`, `is_consumable`, `board_health`, `itm_crew`, `itm_season`, `itm_currency_scrap`, `itm_currency_manpower`, `itm_currency_net`, `itm_currency_cash`, `itm_currency_special`, `itm_rank`, `itm_stat_0`, `itm_stat_1`, `itm_stat_2`, `itm_stat_3`, `itm_stat_4`, `itm_stat_5`, `itm_stat_6`, `itm_stat_7`, `itm_stat_8`, `itm_stat_9`, `itm_stat_10`, `itm_stat_11`, `itm_stat_12`, `itm_stat_13`, `itm_stat_14`, `itm_stat_15`, `itm_stat_16`, `itm_stat_17`, `itm_stat_18`, `itm_stat_19`, `itm_stat_20`, `itm_stat_21`, `itm_stat_22`, `itm_stat_23`, `itm_stat_24`, `itm_stat_25`, `itm_stat_26`, `itm_stat_27`, `itm_stat_28`, `itm_stat_29`, `itm_stat_30`, `itm_chance`) VALUES
	(0, '없음', '아무것도 없음. (지우지 말것)', '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '0', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(1, 'K3OC', 'KAWA철강에서 제작한 염가형 코일', '코일1', 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, '0', 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(2, '반응형 노즐', '고물상에서 쉽게 찾을 수 있는 오래된 노즐. 오래된 기술이다.', '노즐1', 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, '0', 1, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(3, '시장표 콘덴서', '부품시장에서 쉽게 찾을 수 있는 콘덴서.', '콘덴서1', 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, '0', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(4, '30년된 배터리', '폐차장에서 입수한 이름모를 배터리. 다들 그냥 30년묵은 배터리라 부른다.', '배터리1', 10, 0, 1, 0, 0, 0, 0, 100, 100, 100, 0, '0', 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(5, 'WA5V', 'WABI에서 만든 인도산 전자석', '전자석1', 10, 0, 1, 0, 0, 0, 0, 100, 100, 100, 0, '0', 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(6, 'CREW01', '크루배틀에 참가하는 전원을 위해 주최측에서 제작한 방전장치.', '아크방전1', 10, 0, 1, 0, 0, 0, 0, 100, 100, 100, 0, '0', 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(7, 'CREW02', '크루배틀에 참가하는 전원을 위해 주최측에서 제작한 방전장치.', '아크방전2', 10, 0, 1, 0, 0, 0, 0, 100, 100, 100, 0, '0', 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(8, 'Bull Power', '도로공사용 불도저에 들어가는 저항.', '저항1', 10, 0, 1, 0, 0, 0, 0, 100, 100, 100, 0, '0', 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(9, 'ECU. by PinkR', '넷상에서 유포된 의문의 데이터로 맵핑한 ECU. PinkR이 누구지?  (매핑 안된 ECU 필요)', 'ecu1', 10, 0, 1, 0, 0, 0, 0, 200, 200, 200, 0, '{"10":1}', 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(10, '매핑 안된 ECU', '방금 사온 ECU  보드.  재료 아이템.', 'ecu1', 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, '0', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(50, '보드ui 테스트용', '보드 ui 테스트용 아이템', 'non', 100, 1, 0, 0, 100, 0, 0, 10, 20, 5, 0, '0', 1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(51, '보드ui 테스트 2', '보드 ui 테스트용 아이템 2', 'non', 100, 1, 0, 0, 100, 0, 0, 10, 20, 5, 0, '0', 1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(1000, '보드캐시템', '보드 개발 즉시완료를 위한 캐시템. 임시로 우선 이리 놓음.', 'non', 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 100, '0', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(2000, '템개발캐시템', '일반템 개발 즉시완료 아이템. 위와동일', 'non', 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 100, '0', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(3000, '투자캐시템', '설명할필요 없겠지?', 'non', 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 100, '0', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
/*!40000 ALTER TABLE `items_equip` ENABLE KEYS */;

-- 테이블 lif_table.item_tree 구조 내보내기
DROP TABLE IF EXISTS `item_tree`;
CREATE TABLE IF NOT EXISTS `item_tree` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_id` int(11) NOT NULL COMMENT '소속된 아이템 아이디',
  `item_parent_id` int(11) NOT NULL COMMENT '연결된 하위 아이템 아이디. 이게 먼져 연구가 안됬으면 템 못씀',
  PRIMARY KEY (`id`),
  KEY `FK_item_tree_items` (`item_id`),
  KEY `FK_item_tree_items_2` (`item_parent_id`),
  CONSTRAINT `FK_item_tree_items` FOREIGN KEY (`item_id`) REFERENCES `items_equip` (`id`),
  CONSTRAINT `FK_item_tree_items_2` FOREIGN KEY (`item_parent_id`) REFERENCES `items_equip` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='템 강화시 필요.';

-- 테이블 데이터 lif_table.item_tree:~0 rows (대략적) 내보내기
DELETE FROM `item_tree`;
/*!40000 ALTER TABLE `item_tree` DISABLE KEYS */;
/*!40000 ALTER TABLE `item_tree` ENABLE KEYS */;

-- 테이블 lif_table.login_records 구조 내보내기
DROP TABLE IF EXISTS `login_records`;
CREATE TABLE IF NOT EXISTS `login_records` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL COMMENT '사용자 계정',
  `ip_addr` varchar(50) COLLATE utf8_bin NOT NULL COMMENT 'IP주소',
  `time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '접속시간.',
  PRIMARY KEY (`id`),
  KEY `FK_login_records__users` (`user_id`),
  CONSTRAINT `FK_login_records__users` FOREIGN KEY (`user_id`) REFERENCES `_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='각 플레이어들의 로그인 기록 등등';

-- 테이블 데이터 lif_table.login_records:~0 rows (대략적) 내보내기
DELETE FROM `login_records`;
/*!40000 ALTER TABLE `login_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `login_records` ENABLE KEYS */;

-- 테이블 lif_table.records 구조 내보내기
DROP TABLE IF EXISTS `records`;
CREATE TABLE IF NOT EXISTS `records` (
  `record_num` int(11) NOT NULL AUTO_INCREMENT,
  `player_num` int(11) NOT NULL,
  `map_info` longblob NOT NULL COMMENT '맵정보. 자료를 통째로 넣는걸 가정하고 넣음.',
  `victory` int(11) NOT NULL COMMENT 'if 1, win, elif 0, lose',
  `elapsed_time` float NOT NULL COMMENT 'elapsed time in seconds',
  `recorded_time` timestamp NOT NULL DEFAULT current_timestamp() COMMENT '등록된 시간.',
  `item_used` text COLLATE utf8_bin NOT NULL COMMENT '해당 판에 쓰인 아이템 목록. JSON 형태로 저장해야 할듯?',
  `score` int(11) NOT NULL COMMENT '점수',
  PRIMARY KEY (`record_num`),
  KEY `player_num` (`player_num`),
  CONSTRAINT `FK__players` FOREIGN KEY (`player_num`) REFERENCES `_players` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='게임기록들. ';

-- 테이블 데이터 lif_table.records:~0 rows (대략적) 내보내기
DELETE FROM `records`;
/*!40000 ALTER TABLE `records` DISABLE KEYS */;
/*!40000 ALTER TABLE `records` ENABLE KEYS */;

-- 테이블 lif_table.records_best 구조 내보내기
DROP TABLE IF EXISTS `records_best`;
CREATE TABLE IF NOT EXISTS `records_best` (
  `player_unique_id` int(11) NOT NULL COMMENT '플레이어 번호. ',
  `time_stamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '시간. 기록된 시간.',
  `record_score` int(100) NOT NULL COMMENT '점수.',
  `record_time` float NOT NULL COMMENT '게임 클리어 타임.  elapsed time in seconds',
  `record_item` varchar(100) COLLATE utf8_bin DEFAULT NULL COMMENT '해당 스테이지에서 사용한 아이템 아이디 목록.',
  `record_board` int(11) NOT NULL COMMENT '사용한 보드 아이디.',
  `record_stage` int(11) NOT NULL COMMENT '스테이지 순서. ( ex : 3142    = 스테이지 3번 1번 4번 2번 순서로 등장. )',
  `record_barricade_1` text COLLATE utf8_bin NOT NULL COMMENT '첫번째 스테이지에 등장한 장애물',
  `record_barricade_2` text COLLATE utf8_bin NOT NULL COMMENT '두번째 스테이지에 등장한 장애물',
  `record_barricade_3` text COLLATE utf8_bin NOT NULL COMMENT '세번째 스테이지에 등장한 장애물',
  `record_barricade_4` text COLLATE utf8_bin NOT NULL COMMENT '네번째 스테이지에 등장한 장애물',
  `record_barricade_5` text COLLATE utf8_bin NOT NULL COMMENT '다섯번째 스테이지에 등장한 장애물',
  PRIMARY KEY (`player_unique_id`),
  KEY `FK__records_best__players` (`player_unique_id`),
  CONSTRAINT `FK__records_best__players` FOREIGN KEY (`player_unique_id`) REFERENCES `_players` (`player_unique_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='각 플레이어별 최고기록 저장되는거. 최고기록 보기, 크루배틀 등에서 사용.';

-- 테이블 데이터 lif_table.records_best:~0 rows (대략적) 내보내기
DELETE FROM `records_best`;
/*!40000 ALTER TABLE `records_best` DISABLE KEYS */;
INSERT INTO `records_best` (`player_unique_id`, `time_stamp`, `record_score`, `record_time`, `record_item`, `record_board`, `record_stage`, `record_barricade_1`, `record_barricade_2`, `record_barricade_3`, `record_barricade_4`, `record_barricade_5`) VALUES
	(727329, '2019-01-07 08:45:12', 9515414, 732.541, '[5, 10, 8, 7, 2, 1, 3]', 15, 3241, '[{\'num\': 1, \'stage_num\': 3, \'x_pos\': 5.321, \'barricade_num\': 3}, {\'num\': 2, \'stage_num\': 3, \'x_pos\': 9.732, \'barricade_num\': 5}, {\'num\': 3, \'stage_num\': 3, \'x_pos\': 15.121, \'barricade_num\': 2}]', '[{\'num\': 1, \'stage_num\': 3, \'x_pos\': 5.321, \'barricade_num\': 3}, {\'num\': 2, \'stage_num\': 3, \'x_pos\': 10.1, \'barricade_num\': 5}, {\'num\': 3, \'stage_num\': 3, \'x_pos\': 15.21, \'barricade_num\': 2}]', '[{\'num\': 1, \'stage_num\': 3, \'x_pos\': 5.321, \'barricade_num\': 3}, {\'num\': 2, \'stage_num\': 3, \'x_pos\': 8.31, \'barricade_num\': 5}, {\'num\': 3, \'stage_num\': 3, \'x_pos\': 15.321, \'barricade_num\': 2}]', '[{\'num\': 1, \'stage_num\': 3, \'x_pos\': 5.321, \'barricade_num\': 3}, {\'num\': 2, \'stage_num\': 3, \'x_pos\': 11, \'barricade_num\': 5}, {\'num\': 3, \'stage_num\': 3, \'x_pos\': 15, \'barricade_num\': 2}]', '[{\'num\': 1, \'stage_num\': 3, \'x_pos\': 5.321, \'barricade_num\': 3}, {\'num\': 2, \'stage_num\': 3, \'x_pos\': 10.921, \'barricade_num\': 5}, {\'num\': 3, \'stage_num\': 3, \'x_pos\': 15.521, \'barricade_num\': 2}]');
/*!40000 ALTER TABLE `records_best` ENABLE KEYS */;

-- 테이블 lif_table.season 구조 내보내기
DROP TABLE IF EXISTS `season`;
CREATE TABLE IF NOT EXISTS `season` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '관리번호',
  `season_descr` varchar(500) COLLATE utf8_bin NOT NULL COMMENT '시즌 이야기',
  `season_name` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '시즌 명칭',
  `start_date` datetime NOT NULL COMMENT '시작일자.',
  `end_date` datetime NOT NULL COMMENT '시즌 종료일자. ',
  `crew_num` int(11) NOT NULL DEFAULT 0 COMMENT '쓸 수 있는 크루? 승리한 크루?',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='각 시즌별 기록기재 용도? 우선은 이래 놓기만.\r\n이 항목은 UI상에서 띄울 자료만 넣는다. ';

-- 테이블 데이터 lif_table.season:~0 rows (대략적) 내보내기
DELETE FROM `season`;
/*!40000 ALTER TABLE `season` DISABLE KEYS */;
/*!40000 ALTER TABLE `season` ENABLE KEYS */;

-- 테이블 lif_table._friends 구조 내보내기
DROP TABLE IF EXISTS `_friends`;
CREATE TABLE IF NOT EXISTS `_friends` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `player_unique_id` int(11) NOT NULL COMMENT '친구추가 당사자',
  `friend_unique_id` int(11) NOT NULL COMMENT '추가할 친구',
  `relation` int(11) NOT NULL COMMENT '세부내용 테이블코멘트',
  PRIMARY KEY (`id`),
  KEY `FK__friends__players` (`player_unique_id`),
  KEY `FK__friends__players_2` (`friend_unique_id`),
  CONSTRAINT `FK__friends__players` FOREIGN KEY (`player_unique_id`) REFERENCES `_players` (`player_unique_id`),
  CONSTRAINT `FK__friends__players_2` FOREIGN KEY (`friend_unique_id`) REFERENCES `_players` (`player_unique_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='친구추가. \r\nrelation 테이블 구분:\r\n0 - 친구추가 승인대기(friend_unique_id가 승인해야함)\r\n1 - 친구\r\n2 - 차단상태. player_unique_id가 friend_unique_id를 차단한거.\r\n';

-- 테이블 데이터 lif_table._friends:~0 rows (대략적) 내보내기
DELETE FROM `_friends`;
/*!40000 ALTER TABLE `_friends` DISABLE KEYS */;
/*!40000 ALTER TABLE `_friends` ENABLE KEYS */;

-- 테이블 lif_table._friends_copy 구조 내보내기
DROP TABLE IF EXISTS `_friends_copy`;
CREATE TABLE IF NOT EXISTS `_friends_copy` (
  `player_unique_id` int(11) NOT NULL COMMENT '친구추가 당사자',
  `friend_unique_id` int(11) NOT NULL COMMENT '추가할 친구',
  `friend_accepted` int(11) NOT NULL DEFAULT 0 COMMENT '0이면 추가 확인 띄워야함.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT COMMENT='친구추가. \r\nrelation 테이블 구분:\r\n0 - 친구추가 승인대기(friend_unique_id가 승인해야함)\r\n1 - 친구\r\n2 - 차단상태. player\r\n';

-- 테이블 데이터 lif_table._friends_copy:~4 rows (대략적) 내보내기
DELETE FROM `_friends_copy`;
/*!40000 ALTER TABLE `_friends_copy` DISABLE KEYS */;
INSERT INTO `_friends_copy` (`player_unique_id`, `friend_unique_id`, `friend_accepted`) VALUES
	(1, 3, 1),
	(1, 2, 1),
	(2, 3, 0),
	(1, 4, 0);
/*!40000 ALTER TABLE `_friends_copy` ENABLE KEYS */;

-- 테이블 lif_table._players 구조 내보내기
DROP TABLE IF EXISTS `_players`;
CREATE TABLE IF NOT EXISTS `_players` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '플레이어 관리용 고유번호. ',
  `player_unique_id` int(11) NOT NULL COMMENT '플레이어 식별번호? 개인적으로 왜필요한진 잘 모르겠음.',
  `user_id` int(11) NOT NULL COMMENT 'user_num과 동일. 고유 관리번호.',
  `affiliated_crew_id` int(11) NOT NULL COMMENT '소속된 크루 번호. crew 테이블의 crew_id',
  `player_nick` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '케릭명',
  `player_highscore` int(200) NOT NULL DEFAULT 0 COMMENT '플레이어의 최고점수(지도 통틀어서)',
  `player_badge` varchar(100) COLLATE utf8_bin NOT NULL COMMENT '플레이어 프로필사진',
  `player_rank` int(11) NOT NULL DEFAULT 1,
  `player_lvl` int(11) NOT NULL DEFAULT 1,
  `player_exp` int(11) NOT NULL DEFAULT 0,
  `money_workers` int(11) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `player_nick` (`player_nick`),
  UNIQUE KEY `player_unique_id` (`player_unique_id`),
  KEY `FK_players_crew` (`affiliated_crew_id`),
  KEY `player_num` (`user_id`),
  CONSTRAINT `FK_players_crew` FOREIGN KEY (`affiliated_crew_id`) REFERENCES `crew` (`id`),
  CONSTRAINT `player_num` FOREIGN KEY (`user_id`) REFERENCES `_users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='플레이어들과 관련된 기본 사항. ';

-- 테이블 데이터 lif_table._players:~35 rows (대략적) 내보내기
DELETE FROM `_players`;
/*!40000 ALTER TABLE `_players` DISABLE KEYS */;
INSERT INTO `_players` (`id`, `player_unique_id`, `user_id`, `affiliated_crew_id`, `player_nick`, `player_highscore`, `player_badge`, `player_rank`, `player_lvl`, `player_exp`, `money_workers`) VALUES
	(4, 84658, 11, 1, '으아아아', 0, 'testing', 20, 20, 0, 1),
	(5, 84659, 12, 2, 'ray', 0, 'testing', 20, 20, 0, 1),
	(6, 361489, 13, 2, 'uuugh', 0, 'testing', 20, 20, 0, 1),
	(7, 73089, 14, 1, '스크루디스', 0, 'testing', 50, 20, 0, 1),
	(8, 381069, 16, 1, '15275329456', 0, 'testing', 59, 59, 550, 1),
	(9, 570949, 17, 1, '15275302076', 0, 'testing', 24, 24, 350, 1),
	(11, 727329, 20, 1, '15277595947', 0, 'testing', 24, 24, 50, 1),
	(12, 916926, 18, 1, '15277663738', 0, 'testing', 22, 22, 450, 1),
	(13, 485490, 21, 1, '15277663882', 0, 'testing', 23, 23, 500, 1),
	(14, 318476, 19, 1, '15277663922', 0, 'testing', 20, 20, 700, 1),
	(15, 383618, 22, 1, '15277664158', 0, 'testing', 20, 20, 550, 1),
	(16, 902285, 23, 1, '15277664320', 0, 'testing', 21, 21, 750, 1),
	(17, 22, 24, 1, '15277664402', 0, 'testing', 20, 20, 450, 1),
	(18, 518679, 25, 1, '15277664742', 0, 'testing', 20, 20, 700, 1),
	(19, 369426, 27, 1, '15277664910', 0, 'testing', 20, 20, 500, 1),
	(20, 194575, 26, 1, '15277664919', 0, 'testing', 21, 21, 450, 1),
	(21, 162384, 28, 1, '15277664951', 0, 'testing', 22, 22, 850, 1),
	(22, 788427, 29, 1, '15277665044', 0, 'testing', 20, 20, 350, 1),
	(23, 515254, 31, 1, '15277665487', 0, 'testing', 20, 20, 150, 1),
	(24, 299227, 34, 1, '15277665630', 0, 'testing', 20, 20, 0, 1),
	(25, 802192, 33, 1, '15277665635', 0, 'testing', 20, 20, 0, 1),
	(26, 226862, 32, 1, '15277670684', 0, 'testing', 20, 20, 0, 1),
	(27, 919345, 30, 1, '15277671145', 0, 'testing', 20, 20, 450, 1),
	(28, 670239, 36, 1, '15277671578', 0, 'testing', 20, 20, 50, 1),
	(29, 610384, 35, 1, '15277671596', 0, 'testing', 20, 20, 0, 1),
	(30, 631240, 39, 1, '15277671915', 0, 'testing', 20, 20, 800, 1),
	(31, 25850, 38, 1, '15277672045', 0, 'testing', 20, 20, 400, 1),
	(32, 417711, 37, 1, '15277672056', 0, 'testing', 20, 20, 650, 1),
	(33, 589312, 41, 1, '15277672947', 0, 'testing', 20, 20, 750, 1),
	(34, 533981, 42, 1, '15277673356', 0, 'testing', 20, 20, 0, 1),
	(35, 187640, 44, 1, '15277673788', 0, 'testing', 20, 20, 0, 1),
	(36, 627200, 43, 1, '15277673855', 0, 'testing', 20, 20, 0, 1),
	(37, 212508, 40, 1, '15277673986', 0, 'testing', 20, 20, 700, 1),
	(38, 402897, 45, 1, '15277676498', 0, 'testing', 20, 20, 700, 1),
	(39, 7777777, 46, 1, 'sm', 0, 'testing', 10, 10, 0, 5);
/*!40000 ALTER TABLE `_players` ENABLE KEYS */;

-- 테이블 lif_table._players_cash 구조 내보내기
DROP TABLE IF EXISTS `_players_cash`;
CREATE TABLE IF NOT EXISTS `_players_cash` (
  `player_unique_id` int(11) NOT NULL,
  `player_currency_scrap` int(11) NOT NULL DEFAULT 0 COMMENT '일반재화 1',
  `player_currency_manpower` int(11) NOT NULL DEFAULT 0 COMMENT '일반재화 2',
  `player_currency_net` int(11) NOT NULL DEFAULT 0 COMMENT '일반재화 3',
  `player_currency_cash` int(11) NOT NULL DEFAULT 0 COMMENT '캐시',
  PRIMARY KEY (`player_unique_id`),
  CONSTRAINT `FK__players_cash__players` FOREIGN KEY (`player_unique_id`) REFERENCES `_players` (`player_unique_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='게임 내 재화';

-- 테이블 데이터 lif_table._players_cash:~35 rows (대략적) 내보내기
DELETE FROM `_players_cash`;
/*!40000 ALTER TABLE `_players_cash` DISABLE KEYS */;
INSERT INTO `_players_cash` (`player_unique_id`, `player_currency_scrap`, `player_currency_manpower`, `player_currency_net`, `player_currency_cash`) VALUES
	(22, 500, 500, 500, 0),
	(25850, 500, 500, 500, 0),
	(73089, 1630, 3900, 5500, 0),
	(84658, 500, 500, 500, 0),
	(84659, 500, 500, 500, 0),
	(162384, 263, 266, 247, 0),
	(187640, 500, 500, 500, 0),
	(194575, 528, 540, 530, 0),
	(212508, 500, 500, 500, 0),
	(226862, 500, 500, 500, 0),
	(299227, 500, 500, 500, 0),
	(318476, 500, 500, 500, 0),
	(361489, 500, 500, 500, 0),
	(369426, 500, 500, 500, 0),
	(381069, 722, 814, 825, 0),
	(383618, 500, 500, 500, 0),
	(402897, 500, 500, 500, 0),
	(417711, 500, 500, 500, 0),
	(485490, 607, 713, 613, 0),
	(515254, 500, 500, 500, 0),
	(518679, 500, 500, 500, 0),
	(533981, 500, 500, 500, 0),
	(570949, 2740, 7280, 10530, 0),
	(589312, 500, 500, 500, 0),
	(610384, 500, 500, 500, 0),
	(627200, 500, 500, 500, 0),
	(631240, 500, 500, 500, 0),
	(670239, 500, 500, 500, 0),
	(727329, 517, 519, 501, 0),
	(788427, 500, 500, 500, 0),
	(802192, 500, 500, 500, 0),
	(902285, 591, 556, 588, 0),
	(916926, 500, 500, 500, 0),
	(919345, 500, 500, 500, 0),
	(7777777, 600, 720, 220, 0);
/*!40000 ALTER TABLE `_players_cash` ENABLE KEYS */;

-- 테이블 lif_table._players_cash_flow 구조 내보내기
DROP TABLE IF EXISTS `_players_cash_flow`;
CREATE TABLE IF NOT EXISTS `_players_cash_flow` (
  `id` int(20) NOT NULL COMMENT '기본 관리번호',
  `time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '언제 삼?',
  `player_unique_id` int(11) NOT NULL COMMENT '플레이어 번호?',
  `cash_type` int(11) NOT NULL COMMENT '어떤 돈임?',
  `cash_cost` int(11) NOT NULL COMMENT '도합 얼마?',
  `item_id` int(11) NOT NULL COMMENT '무슨 템? id',
  `item_quantity` int(11) NOT NULL COMMENT '몇개?',
  PRIMARY KEY (`id`),
  KEY `FK___players_` (`player_unique_id`),
  KEY `FK__items` (`item_id`),
  CONSTRAINT `FK___players_` FOREIGN KEY (`player_unique_id`) REFERENCES `_players` (`player_unique_id`),
  CONSTRAINT `FK__items` FOREIGN KEY (`item_id`) REFERENCES `items_equip` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='플레이어들 캐시 사용내역. ';

-- 테이블 데이터 lif_table._players_cash_flow:~0 rows (대략적) 내보내기
DELETE FROM `_players_cash_flow`;
/*!40000 ALTER TABLE `_players_cash_flow` DISABLE KEYS */;
/*!40000 ALTER TABLE `_players_cash_flow` ENABLE KEYS */;

-- 테이블 lif_table._player_challenge_list 구조 내보내기
DROP TABLE IF EXISTS `_player_challenge_list`;
CREATE TABLE IF NOT EXISTS `_player_challenge_list` (
  `player_num` int(11) NOT NULL COMMENT '플레이어 번호. players 테이블의 프라이머리키',
  `열 2` int(11) NOT NULL DEFAULT 0 COMMENT '각 목록 달성여부: 1이 달성',
  `열 3` int(11) NOT NULL DEFAULT 0,
  KEY `FK_challenge_list_players` (`player_num`),
  CONSTRAINT `FK_challenge_list_players` FOREIGN KEY (`player_num`) REFERENCES `_players` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='도전과제 목록.\r\n내용물은 아직 들어가있지 않음.';

-- 테이블 데이터 lif_table._player_challenge_list:~0 rows (대략적) 내보내기
DELETE FROM `_player_challenge_list`;
/*!40000 ALTER TABLE `_player_challenge_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `_player_challenge_list` ENABLE KEYS */;

-- 테이블 lif_table._player_items 구조 내보내기
DROP TABLE IF EXISTS `_player_items`;
CREATE TABLE IF NOT EXISTS `_player_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '단순 관리번호',
  `player_unique_id` int(11) NOT NULL COMMENT '플레이어 고유번호',
  `item_id` int(11) NOT NULL COMMENT '아이템 아이디',
  `item_quantity` int(11) NOT NULL COMMENT '가진 수량. 보드인 경우 1 고정.',
  `item_health` int(11) NOT NULL DEFAULT 0 COMMENT '보드의 체력. is_board 일 경우에만 적용. 아니면 0 -- 추후 current_health로 개명해야함.',
  `is_board` int(11) NOT NULL DEFAULT 0 COMMENT '보드인가? 아니면 0',
  PRIMARY KEY (`id`),
  KEY `FK__player_items__players` (`player_unique_id`),
  KEY `FK__player_items_items` (`item_id`),
  CONSTRAINT `FK__player_items__players` FOREIGN KEY (`player_unique_id`) REFERENCES `_players` (`player_unique_id`),
  CONSTRAINT `FK__player_items_items` FOREIGN KEY (`item_id`) REFERENCES `items_equip` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='플레이어가 가지고 있는 아이템 목록.';

-- 테이블 데이터 lif_table._player_items:~7 rows (대략적) 내보내기
DELETE FROM `_player_items`;
/*!40000 ALTER TABLE `_player_items` DISABLE KEYS */;
INSERT INTO `_player_items` (`id`, `player_unique_id`, `item_id`, `item_quantity`, `item_health`, `is_board`) VALUES
	(70, 570949, 3000, 4, 0, 0),
	(71, 570949, 10, 5, 0, 0),
	(72, 7777777, 3000, 30, 0, 0),
	(73, 7777777, 50, 1, 100, 1),
	(74, 7777777, 2000, 20, 0, 0),
	(76, 7777777, 10, 10, 0, 0),
	(77, 7777777, 1, 1, 0, 0);
/*!40000 ALTER TABLE `_player_items` ENABLE KEYS */;

-- 테이블 lif_table._player_queue_cash 구조 내보내기
DROP TABLE IF EXISTS `_player_queue_cash`;
CREATE TABLE IF NOT EXISTS `_player_queue_cash` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `player_unique_id` int(11) NOT NULL COMMENT '플레이어 번호',
  `income_id` int(11) NOT NULL COMMENT '투자하고있는 대상 아이디',
  `time_to_finish` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '걸리는 시간.',
  PRIMARY KEY (`id`),
  KEY `FK__player_queue_cash__players` (`player_unique_id`),
  KEY `FK__player_queue_cash_income_tab` (`income_id`),
  CONSTRAINT `FK__player_queue_cash__players` FOREIGN KEY (`player_unique_id`) REFERENCES `_players` (`player_unique_id`) ON UPDATE NO ACTION,
  CONSTRAINT `FK__player_queue_cash_income_tab` FOREIGN KEY (`income_id`) REFERENCES `income_tab` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='캐시 캐기위해 큐 등을 올려놓은거. income_tab 테이블에서 가져온다. ';

-- 테이블 데이터 lif_table._player_queue_cash:~2 rows (대략적) 내보내기
DELETE FROM `_player_queue_cash`;
/*!40000 ALTER TABLE `_player_queue_cash` DISABLE KEYS */;
INSERT INTO `_player_queue_cash` (`id`, `player_unique_id`, `income_id`, `time_to_finish`) VALUES
	(5, 570949, 500, '2018-07-17 18:38:49'),
	(6, 7777777, 500, '2018-10-24 06:48:55');
/*!40000 ALTER TABLE `_player_queue_cash` ENABLE KEYS */;

-- 테이블 lif_table._player_queue_items 구조 내보내기
DROP TABLE IF EXISTS `_player_queue_items`;
CREATE TABLE IF NOT EXISTS `_player_queue_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'PK',
  `player_unique_id` int(11) NOT NULL COMMENT '연동될 플레이어 번호',
  `item_id` int(11) NOT NULL COMMENT '연구·개발하는 아이템.',
  `is_board` int(11) NOT NULL COMMENT '보드인가?',
  `time_to_finish` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '끝날 시간.',
  PRIMARY KEY (`id`),
  KEY `FK__player_queue_items__players` (`player_unique_id`),
  KEY `FK__player_queue_items_items_equip` (`item_id`),
  CONSTRAINT `FK__player_queue_items__players` FOREIGN KEY (`player_unique_id`) REFERENCES `_players` (`player_unique_id`) ON UPDATE CASCADE,
  CONSTRAINT `FK__player_queue_items_items_equip` FOREIGN KEY (`item_id`) REFERENCES `items_equip` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=139 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='아이템 개발큐';

-- 테이블 데이터 lif_table._player_queue_items:~2 rows (대략적) 내보내기
DELETE FROM `_player_queue_items`;
/*!40000 ALTER TABLE `_player_queue_items` DISABLE KEYS */;
INSERT INTO `_player_queue_items` (`id`, `player_unique_id`, `item_id`, `is_board`, `time_to_finish`) VALUES
	(1, 73089, 4, 0, '2018-07-03 02:34:45'),
	(138, 162384, 6, 0, '2018-06-22 06:42:49');
/*!40000 ALTER TABLE `_player_queue_items` ENABLE KEYS */;

-- 테이블 lif_table._player_researched_items 구조 내보내기
DROP TABLE IF EXISTS `_player_researched_items`;
CREATE TABLE IF NOT EXISTS `_player_researched_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '기본관리번호',
  `player_unique_id` int(11) NOT NULL COMMENT '플레이어 고유번호',
  `item_id` int(11) NOT NULL COMMENT '연구완료한 아이템 아이디',
  PRIMARY KEY (`id`),
  KEY `FK__player_researched_items__players` (`player_unique_id`),
  KEY `FK__player_researched_items_items` (`item_id`),
  CONSTRAINT `FK__player_researched_items__players` FOREIGN KEY (`player_unique_id`) REFERENCES `_players` (`player_unique_id`) ON UPDATE NO ACTION,
  CONSTRAINT `FK__player_researched_items_items` FOREIGN KEY (`item_id`) REFERENCES `items_equip` (`id`) ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='연구완료한 아이템 목록';

-- 테이블 데이터 lif_table._player_researched_items:~19 rows (대략적) 내보내기
DELETE FROM `_player_researched_items`;
/*!40000 ALTER TABLE `_player_researched_items` DISABLE KEYS */;
INSERT INTO `_player_researched_items` (`id`, `player_unique_id`, `item_id`) VALUES
	(99, 570949, 4),
	(100, 570949, 5),
	(101, 570949, 6),
	(102, 570949, 7),
	(103, 7777777, 5),
	(104, 7777777, 4),
	(105, 7777777, 6),
	(106, 381069, 4),
	(107, 570949, 8),
	(108, 381069, 5),
	(109, 381069, 6),
	(110, 381069, 8),
	(111, 381069, 7),
	(112, 381069, 9),
	(113, 485490, 4),
	(114, 162384, 4),
	(115, 162384, 5),
	(116, 7777777, 7),
	(117, 7777777, 8);
/*!40000 ALTER TABLE `_player_researched_items` ENABLE KEYS */;

-- 테이블 lif_table._users 구조 내보내기
DROP TABLE IF EXISTS `_users`;
CREATE TABLE IF NOT EXISTS `_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '고유 관리번호',
  `user_email` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '이메일주소',
  `user_reg_date` timestamp NOT NULL DEFAULT current_timestamp() COMMENT '회원가입시간.',
  `last_login` timestamp NULL DEFAULT NULL COMMENT '최종 로그인 일자',
  `passwd` varchar(80) COLLATE utf8_bin DEFAULT NULL COMMENT '암호. 암호화되야함.',
  `social_id` varchar(80) COLLATE utf8_bin DEFAULT NULL COMMENT '연동로그인 계정',
  `verified` int(11) NOT NULL DEFAULT 0 COMMENT '승인되었는가? 연동로그인이면 자동승인이지만 일반 이메일가입이면 메일로 승인받는다.',
  `verified_date` timestamp NULL DEFAULT NULL COMMENT '승인된 시간. 연동이면 연동당시 시간 그대로.',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_email` (`user_email`),
  UNIQUE KEY `social_id` (`social_id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='기본정보. 계정아이디, 이메일, 별명, 등등. ';

-- 테이블 데이터 lif_table._users:~40 rows (대략적) 내보내기
DELETE FROM `_users`;
/*!40000 ALTER TABLE `_users` DISABLE KEYS */;
INSERT INTO `_users` (`id`, `user_email`, `user_reg_date`, `last_login`, `passwd`, `social_id`, `verified`, `verified_date`) VALUES
	(1, 'aa@aa.com', '2017-11-07 17:07:34', NULL, 'liveonce', NULL, 1, NULL),
	(2, 'aa@aaa.com', '2017-11-16 13:18:13', NULL, '', NULL, 1, NULL),
	(10, 'yy@aaaa.com', '2017-11-16 14:22:50', NULL, 'carry', NULL, 1, NULL),
	(11, '00e@gmail.com', '2018-05-07 22:55:08', NULL, NULL, '0', 1, NULL),
	(12, '00031@gmail.com', '2018-05-16 13:57:34', NULL, NULL, 'google$', 1, NULL),
	(13, '00ooo@naver.com', '2018-05-22 15:35:47', NULL, '8a2da05455775e8987cbfac5a0ca54f3f728e274', NULL, 1, NULL),
	(14, '00this@naver.com', '2018-05-28 16:12:11', NULL, '8a2da05455775e8987cbfac5a0ca54f3f728e274', NULL, 1, NULL),
	(16, '1', '2018-05-28 16:12:11', NULL, '356a192b7913b04c54574d18c28d46e6395428ab', NULL, 1, NULL),
	(17, '2', '2018-05-28 17:50:29', NULL, 'da4b9237bacccdf19c0760cab7aec4a8359010b0', NULL, 1, NULL),
	(18, '3', '2018-05-30 21:28:02', NULL, '77de68daecd823babbb58edb1c8e14d7106e83bb', NULL, 1, NULL),
	(19, '4', '2018-05-30 21:28:27', NULL, '1b6453892473a467d07372d45eb05abc2031647a', NULL, 1, NULL),
	(20, '5', '2018-05-30 21:28:35', NULL, 'ac3478d69a3c81fa62e60f5c3696165a4e5e6ac4', NULL, 1, NULL),
	(21, '6', '2018-05-30 21:28:45', NULL, 'c1dfd96eea8cc2b62785275bca38ac261256e278', NULL, 1, NULL),
	(22, '7', '2018-05-30 21:28:50', NULL, '902ba3cda1883801594b6e1b452790cc53948fda', NULL, 1, NULL),
	(23, '8', '2018-05-30 21:28:55', NULL, 'fe5dbbcea5ce7e2988b8c69bcfdfde8904aabc1f', NULL, 1, NULL),
	(24, '9', '2018-05-30 21:28:59', NULL, '0ade7c2cf97f75d009975f4d720d1fa6c19f4897', NULL, 1, NULL),
	(25, '10', '2018-05-30 21:29:07', NULL, 'b1d5781111d84f7b3fe45a0852e59758cd7a87e5', NULL, 1, NULL),
	(26, '11', '2018-05-31 09:44:35', NULL, '17ba0791499db908433b80f37c5fbc89b870084b', NULL, 1, NULL),
	(27, '12', '2018-05-31 09:46:26', NULL, '7b52009b64fd0a2a49e6d8a939753077792b0554', NULL, 1, NULL),
	(28, '13', '2018-05-31 09:46:46', NULL, 'bd307a3ec329e10a2cff8fb87480823da114f8f4', NULL, 1, NULL),
	(29, '14', '2018-05-31 09:46:48', NULL, 'fa35e192121eabf3dabf9f5ea6abdbcbc107ac3b', NULL, 1, NULL),
	(30, '15', '2018-05-31 09:46:50', NULL, 'f1abd670358e036c31296e66b3b66c382ac00812', NULL, 1, NULL),
	(31, '16', '2018-05-31 09:46:54', NULL, '1574bddb75c78a6fd2251d61e2993b5146201319', NULL, 1, NULL),
	(32, '17', '2018-05-31 09:46:57', NULL, '0716d9708d321ffb6a00818614779e779925365c', NULL, 1, NULL),
	(33, '18', '2018-05-31 09:47:00', NULL, '9e6a55b6b4563e652a23be9d623ca5055c356940', NULL, 1, NULL),
	(34, '19', '2018-05-31 09:47:03', NULL, 'b3f0c7f6bb763af1be91d9e74eabfeb199dc1f1f', NULL, 1, NULL),
	(35, '20', '2018-05-31 09:47:07', NULL, '91032ad7bbcb6cf72875e8e8207dcfba80173f7c', NULL, 1, NULL),
	(36, '21', '2018-05-31 09:47:13', NULL, '472b07b9fcf2c2451e8781e944bf5f77cd8457c8', NULL, 1, NULL),
	(37, '22', '2018-05-31 09:47:24', NULL, '12c6fc06c99a462375eeb3f43dfd832b08ca9e17', NULL, 1, NULL),
	(38, '23', '2018-05-31 09:47:27', NULL, 'd435a6cdd786300dff204ee7c2ef942d3e9034e2', NULL, 1, NULL),
	(39, '24', '2018-05-31 09:47:33', NULL, '4d134bc072212ace2df385dae143139da74ec0ef', NULL, 1, NULL),
	(40, '25', '2018-05-31 09:47:38', NULL, 'f6e1126cedebf23e1463aee73f9df08783640400', NULL, 1, NULL),
	(41, '26', '2018-05-31 09:47:41', NULL, '887309d048beef83ad3eabf2a79a64a389ab1c9f', NULL, 1, NULL),
	(42, '27', '2018-05-31 09:47:44', NULL, 'bc33ea4e26e5e1af1408321416956113a4658763', NULL, 1, NULL),
	(43, '28', '2018-05-31 09:47:48', NULL, '0a57cb53ba59c46fc4b692527a38a87c78d84028', NULL, 1, NULL),
	(44, '29', '2018-05-31 09:47:52', NULL, '7719a1c782a1ba91c031a682a0a2f8658209adbf', NULL, 1, NULL),
	(45, '30', '2018-05-31 09:47:57', NULL, '22d200f8670dbdb3e253a90eee5098477c95c23d', NULL, 1, NULL),
	(46, '100', '2018-06-04 17:26:08', NULL, '310b86e0b62b828562fc91c7be5380a992b2786a', NULL, 1, NULL),
	(47, '00e@hanmail.net', '2018-08-07 06:28:39', NULL, '8a2da05455775e8987cbfac5a0ca54f3f728e274', NULL, 1, NULL),
	(48, '000@naver.com', '2018-10-01 04:44:27', NULL, NULL, '', 0, NULL);
/*!40000 ALTER TABLE `_users` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
