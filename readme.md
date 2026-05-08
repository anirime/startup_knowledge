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

### 백엔드

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API 문서: http://localhost:8000/docs

### 프론트엔드

```bash
cd frontend
npm install
npm run dev
```

브라우저: http://localhost:5173

`/api` 요청은 Vite dev 서버가 백엔드(8000)로 프록시합니다.

### 배포 빌드

```bash
cd frontend && npm run build
```

`frontend/dist/` 의 정적 파일을 임의의 정적 호스팅에 올리고, `/api` 를 백엔드로 프록시하면 됩니다.

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
