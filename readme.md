# 스타트업 지식베이스

스타트업 정보를 입력하고 검색할 수 있는 지식 정보 검색 웹페이지.

- **Backend**: FastAPI + SQLite
- **Frontend**: Svelte 5 + Vite

## 데이터 모델

- 기본 정보: 회사명, 업종, 설립연도, 위치, 웹사이트
- 투자 정보: 투자 단계, 누적 투자금, 주요 VC
- 팀 정보: CEO, 직원수, 주요 인력
- 사업 정보: 제품/서비스 설명, 태그

## 검색 기능

- 회사명 키워드 검색
- 업종 / 투자단계 / 지역 / 태그 필터
- 모든 필드 대상 전체 텍스트 검색

## 실행

### 한 줄 실행 (권장)

```bash
./run.sh
```

프론트엔드를 빌드하고 FastAPI가 정적 파일까지 서빙합니다. 브라우저: <http://localhost:8000>

두 번째 실행부터 빌드를 건너뛰려면 `./run.sh --skip-build`.

### 개발 모드 (HMR)

```bash
# 터미널 1: 백엔드
cd backend && pip install -r requirements.txt && uvicorn main:app --reload --port 8000

# 터미널 2: 프론트엔드 (Vite dev 서버, /api 는 8000 으로 프록시)
cd frontend && npm install && npm run dev
```

브라우저: <http://localhost:5173>, API 문서: <http://localhost:8000/docs>

### ngrok 으로 외부에 공개하기

`./run.sh` 가 떠 있는 상태에서 다른 터미널에서:

```bash
ngrok http 8000
```

ngrok 이 발급한 `https://xxxx.ngrok-free.app` 주소로 외부에서 접속 가능합니다.
(ngrok 미설치 시 <https://ngrok.com/download> 후 `ngrok config add-authtoken <token>` 1회 필요.)

## 디렉터리

```
backend/
  main.py        # FastAPI 라우트
  database.py    # SQLite 초기화
  requirements.txt
frontend/
  src/
    App.svelte           # 메인 화면 (목록/검색/필터)
    api.js               # 백엔드 호출
    lib/
      StartupCard.svelte
      StartupForm.svelte
      StartupDetail.svelte
```
