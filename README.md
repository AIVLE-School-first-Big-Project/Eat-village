<div align="center">
 <h1>Eat-village</h1>
 </p>
 <p align="center">
  <b>수도권 4반 2조(9조) : 우리는 모두 친9조</b>
 </p>
 <p align="center">
  KT AIVLE-School-first-Big-Project : 2022-04-11 ~ 2022-05-11 </p><br><br>
  
 <pre align="center"> 
 yolov5 모델로 사용자들의 냉장고 속 재료를 분석하여 
 만개의 레시피에서 크롤링한 데이터를 바탕으로 레시피를 추천해주는 모델을 제작하였습니다.
 </pre>
</div>

# : Yolov5를 이용한 냉장고 재료 분석 및 레시피 추천
## 조원 소개
- `수도권 4반 2조 (9조)`
> 안지희(조장), 김연우, 안승훈, 정찬호, 최수진, 한인규

## 1. 개발 배경 및 목적
<pre>
1️⃣. 최근 1인 가구는 증가하고 있고 ‘직접 요리’ 비율은 확 줄었다. 
이는 팬더믹의 영향을 무시할 수 없지만, 설문조사 결과에 ‘조리하기가 번거롭고 귀찮아서’가 랭크되었다. 
우리는 1인 가구가 느끼는 ‘직접 요리’에 대한 허들을 낮추어 신체적, 정서적 건강을 도모할 것을 기대한다.
: <a href='https://www.khan.co.kr/national/national-general/article/202111141025001'>10명 중 4명은 '1인 가구'···‘직접 요리’ 비율 확 줄어든 까닭</a>
: <a href='http://www.research-paper.co.kr/news/articleView.html?idxno=304066'>집에서 하는 요리 귀찮아하면 안 되는 이유</a>

2️⃣. 배달비와 외식비 상승에 부담을 느끼는 시민들이 외식보다는 ‘집밥’을 선택하면서 
‘집에서 요리해 먹기 쉬운 품목’에 대한 수요가 증가하고 있다. 
우리는 이러한 수요에 발 맞춰 ‘집밥’에 대한 접근성을 높일 것이다.
<img src='https://user-images.githubusercontent.com/58163606/167345170-2e6b482a-6114-46c0-95bf-6869f5111651.png' style="height: 200px;"/>
: <a href='https://www.sedaily.com/NewsVIew/264LO712H9'>"차라리 집에서 직접 해먹겠다"…치솟는 외식비에 장보기 는다</a>
: <a href='https://www.chosun.com/economy/market_trend/2021/01/07/MJFHEDVXTFGCNNOW34W7BIOFWA/'>[NOW] 코로나 1년, 밥상은 가난해졌다</a>

</pre>

## 2. 기능 및 UI/UX
- Adobe XD
## 3. 서비스 FLOW
![user_flow_ffff](https://user-images.githubusercontent.com/58163606/167354603-582cccff-bae4-4497-a9c3-6ebf364fdf0a.png)
## 4. Architecture (2-Tier or 3-Tier)
![architecture](https://user-images.githubusercontent.com/92066565/164602627-a2691519-a7b0-4a5e-8281-81bfcd189bbd.png)
## 5. DB 설계
- ERD 모델 (EXERD)
![0509erd](https://user-images.githubusercontent.com/58163606/167395199-1c13b56a-c54e-49e6-9e10-8bfc561bfd6d.png)
## 6. 개발 환경
- FRONT-END : HTML, CSS, JS, Bootstrap
- BACK-END : Django, GoogleCloud, MySQL
## 7. 모바일 연결 설정 : ngrok
- 환경에 맞춰 다운로드 : https://ngrok.com/download
- https://dashboard.ngrok.com/get-started/your-authtoken
  - 회원가입 후 token 발급
  - 회원가입 인증 메일을 수락해야함
- cmd 설정
 ``` bash
  1. ngrok.exe가 다운로드되어 있는 위치로 이동
  2. ngrok config add-authtoken 토큰코드
  3. ngrok http 8000
  ```
- 접속 주소
![ngrok](https://user-images.githubusercontent.com/58163606/167326887-1784dabf-21bc-4731-a622-676cb706ac60.png)
- config/settings.py ALLOWED_HOSTS에 접속 주소에서 https://를 뺸 나머지를 입력
  - 본 프로젝트는 모든 호스트가 접속이 가능하도록 설정됨
![ngrok2](https://user-images.githubusercontent.com/58163606/167327178-dab13f4a-c39a-43f0-923c-a23bbc1c91b0.png)
- 장고 서버 실행
- 모바일에서 접속주소로 접속하면 로그인 페이지로 접속됨
## 8. FFmpeg 설치
- webm를 mp4로 변환하는 과정이 필요
## 9. 실행 방법
``` bash
1. git clone https://github.com/AIVLE-School-first-Big-Project/Eat-village.git
2. cd Eat-village
3. python install -r requirements.txt
4. GCP에서 사용하려는 기기의 IP 등록
5. python manage.py runsever [본인 외부 ip 주소]:8000
  (localhost나 127.0.0.1로 서버 돌리면 타 기기에서 접근 안 됨, DEBUG 가 False이므로 settings- allowed host에 본인 ip 추가)
6. Connect http://[본인외부ip]:8000
```
## 10. 팀원 정보
| Name | Github | Email |
|:---:|:---:|:---:|
|안지희|[@Jinnny-An](https://github.com/Jinnny-An)|syos7462@gmail.com|
|김연우|[@crong22](https://github.com/crong22)|mamen7624@gmail.com|
|안승훈|[@ahnroy](https://github.com/ahnroy)|ahnroy96@gmail.com|
|정찬호|[@joungch](https://github.com/joungch)|joungch2021@gmail.com|
|최수진|[@heeyori](https://github.com/heeyori)|sujin.choi100@gmail.com|
|한인규|[@ikhan94305](https://github.com/ikhan94305)|ikhan94305@gmail.com|
