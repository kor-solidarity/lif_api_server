# lif-api-server

해당 코드는 Lifgames 라고 하는 인디게임 스타트업에서 만들던 게임에서 구동시킬 예정이었던 REST API 서버코드입니다.

This code is a REST API server code intended to run for the Indie game made by Lifgames.

Ĉi tiu kodo estas REST-API servkodo intencis kondukti por la sendependa ludo faris de Lifgames. 

--- 
해당 게임의 이름은 <레일로드:크루배틀>로 예술동호인들이 철로 위에서 호버보드를 타고 경기를 하며 사람들의 관심을 끌게 한다는 컨셉으로 진행되는 모바일 게임입니다.<br>

The name of the Game is <RailRoad:Crew Battle>, a mobile game with a concept of the art-club members on hoverboards competing each other on the railroads, trying to gain the people's attention.<br>

La nomo de la ludo estas <RailRoad:Crew Battle>, la movebla ludo kiu havas la koncepto de la art-klubanoj kun flugtabulon konkuras kun sin mem por gajni la popolan intereson.

[![mvp 소개영상](https://img.youtube.com/vi/hUqvv9Y1_TQ/sddefault.jpg)](https://youtu.be/hUqvv9Y1_TQ)<br>
<MVP 소개 유튜브영상>

---
저는 게임 내 UI(유니티, C#), 그리고 게임에 구동될 API 서버 구축을 담당했습니다. 서버구축 언어로는 파이썬 Flask 프레임워크를 사용했고 서버단은 AWS를, DB는 Mysql로 아마존 RDS를 활용했습니다. AWS에서 EC2에 전체 코드를 넣고 이를 nginx로 구동시켰으며, https 적용에는 aws 인증관리자 서비스를 사용했습니다.<br>

I participated in in-game UI(Unity, C#) and API server for the game to run on. For the server I used Python Flask Framework, and AWS for the server, mysql for the DB(AWS RDS). I ran the server by using AWS EC2 utilizing it with nginx, and AWS certificate service was used for applying https.<br>

Mi partoprenis en fari la en-luda UI-on(Unity, C#) kaj la API servon por funkcii la ludo. Por la servon mi uzis Python Flask Framework-on, kaj AWS-on por servo, mysql-on por DB(AWS RDS). Mi funkciis la servon per AWS EC2 utiligii kun nginx, kaj AWS certificate service estis uzita por apliki https.

---
서버 코드는 전부 혼자 만들었고 사용된 DB 테이블 구조는 다음과 같습니다.<br>

The full code for the server is made by me, and the DB Structure is as follows.<br>

La tutkodo estas farita de mi, kaj la DB strukturo estas kiel jene.

![DB 테이블](https://raw.githubusercontent.com/kor-solidarity/lif_api_server/master/table_structure.png)

-DB 테이블 구조-

---
아쉽게도 최종적으로 프로젝트가 중단됨에 따라 완성은 되지 않았습니다.

The code is regrettably left unfinished as the project itself got terminated.

La kodo bedaŭre ne perfektigis ĉar la projeckto fine ĉesigis.