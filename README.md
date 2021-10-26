# law-farm-api
<pre><code>docker-compose up -d 
</code></pre>
[API Docs: HTTP](http://api.fotone.moe:8000/docs)
[API Docs: HTTPS](https://api.fotone.moe/docs)   

# TODO

- README.md 상세 작성
- ~~docker-compose 손보고 태스트하기~~
- ~~Oracle Cloud 에 최신 레포 배포하기~~
- ~~CRUD 클래스화~~
- ~~user 엔드포인트의 상세한 CRUD (사용자 정보, 비밀번호 재설정, 등)~~
- 일부 validation 안 되는 사항들 체크
- ~~오래된 패키지 최신으로 교체하기~~
- pipenv와 같은 의존성 관리도구 도입하기

# 업데이트 리스트

- 20.10.26: nginx proxy 추가 (SSL 인증, 하위호환을 위해 당분간 http 8000포트는 열려 있을 예정), 게시판 CRUD 추가와 일부 엔드포인트 CRUD 추가
