# 🎉 포트폴리오 관리 시스템 - 시작하기

프로젝트가 성공적으로 생성되었습니다! 이 가이드를 따라 바로 시작하세요.

## 📂 프로젝트 구조

```
portfolio/
├── 📘 START_HERE.md          ← 지금 보고 있는 파일
├── 📘 README.md               ← 전체 문서
├── 📘 QUICKSTART.md           ← 5분 빠른 시작
├── 📘 DEPLOYMENT.md           ← Railway 배포 가이드
├── 📘 PROJECT_SUMMARY.md      ← 구현 내역 요약
│
├── 🐍 backend/                ← FastAPI 백엔드
│   ├── app/                   ← 메인 애플리케이션
│   ├── requirements.txt       ← Python 패키지
│   └── env.example            ← 환경변수 예시
│
└── ⚛️  frontend/              ← React 프론트엔드
    ├── src/                   ← 소스 코드
    ├── package.json           ← npm 패키지
    └── env.example            ← 환경변수 예시
```

## 🚀 빠른 시작 (3단계)

### 1️⃣ Backend 실행

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
```

✅ http://localhost:8000/docs 에서 API 확인

### 2️⃣ Frontend 실행 (새 터미널)

```bash
cd frontend
npm install
npm run dev
```

✅ http://localhost:5173 에서 앱 확인

### 3️⃣ 첫 포트폴리오 생성

1. 회원가입 (`http://localhost:5173`)
2. "새 포트폴리오 만들기" 클릭
3. 투자금액 입력 (예: 10,000,000원)
4. 종목 검색 (예: AAPL, MSFT, TSLA)
5. 목표 비중 설정 (합계 100%)
6. 생성 완료! 🎉

## 📚 다음 단계

| 목적 | 문서 |
|------|------|
| 빠른 로컬 실행 | [QUICKSTART.md](QUICKSTART.md) |
| 전체 기능 이해 | [README.md](README.md) |
| Railway 배포 | [DEPLOYMENT.md](DEPLOYMENT.md) |
| 구현 내역 확인 | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |

## 💡 핵심 기능

✅ **자동 계산**: 생성 시점 가격으로 수량 자동 계산  
✅ **비중 관리**: 목표 vs 현재 비중 실시간 비교  
✅ **시각적 경고**: 허용 오차 초과 시 색상 알림  
✅ **유연한 수정**: 보유 수량 수정으로 매매 반영  
✅ **간편한 배포**: Railway로 원클릭 배포  

## 🎯 주요 화면

### 대시보드
- 포트폴리오 목록 카드 형식
- 초기 투자금, 생성일 표시

### 포트폴리오 생성
- 종목 검색 (yfinance API)
- 목표 비중 설정 (합계 100% 검증)
- **자동 수량 계산**

### 포트폴리오 상세
- 요약: 평가금액, 수익금, 수익률
- 종목별 현재 비중 vs 목표 비중
- **색상 경고 시스템**:
  - 🟡 노란색: 허용 오차 초과
  - 🔴 빨간색: 허용 오차 크게 초과

## 🛠 기술 스택

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL/SQLite
- **Frontend**: React + TypeScript + Vite + Zustand
- **인증**: JWT
- **주식 데이터**: yfinance
- **배포**: Railway

## 🐛 문제 해결

### Backend 실행 오류
```bash
# 포트 사용 중
lsof -i :8000
kill -9 <PID>

# 패키지 설치 오류
pip install --upgrade pip
pip install -r requirements.txt
```

### Frontend 실행 오류
```bash
# 포트 사용 중
lsof -i :5173
kill -9 <PID>

# 의존성 재설치
rm -rf node_modules package-lock.json
npm install
```

### API 연결 오류
- Backend가 `http://localhost:8000`에서 실행 중인지 확인
- CORS 설정 확인: `backend/app/config.py`

## 📦 배포하기

### Railway 배포 (권장)

1. Railway 계정 생성 (https://railway.app)
2. GitHub 저장소 연결
3. PostgreSQL 플러그인 추가
4. 환경변수 설정
5. 자동 배포 완료!

**상세 가이드**: [DEPLOYMENT.md](DEPLOYMENT.md)

## 🎓 학습 리소스

### Backend (FastAPI)
- API 문서: `http://localhost:8000/docs`
- 코드 위치: `backend/app/routes/`
- 비즈니스 로직: `backend/app/services/`

### Frontend (React)
- 페이지: `frontend/src/pages/`
- API 클라이언트: `frontend/src/services/api.ts`
- 상태 관리: `frontend/src/store/authStore.ts`

## 🔑 환경변수 설정 (선택)

### Backend (`backend/.env`)
```bash
cp backend/env.example backend/.env
# 파일을 열어 SECRET_KEY 변경
```

### Frontend (`frontend/.env`)
```bash
cp frontend/env.example frontend/.env
# 기본값으로 충분함
```

## ✨ 테스트 시나리오

### 1. 기본 플로우
1. ✅ 회원가입
2. ✅ 로그인
3. ✅ 포트폴리오 생성
4. ✅ 종목 검색 (예: AAPL)
5. ✅ 목표 비중 설정 (예: 100%)
6. ✅ 포트폴리오 확인

### 2. 비중 관리
1. ✅ "상세보기" 클릭
2. ✅ "🔄 새로고침" 클릭
3. ✅ 현재 비중 vs 목표 비중 확인
4. ✅ 색상 경고 확인

### 3. 수량 수정
1. ✅ "수량 수정" 클릭
2. ✅ 새 수량 입력
3. ✅ "저장" 클릭
4. ✅ 비중 재계산 확인

## 🎁 보너스 기능 (향후 추가 가능)

- [ ] 리밸런싱 제안 (매수/매도 수량 계산)
- [ ] 차트 시각화 (파이 차트, 그래프)
- [ ] 알림 기능 (이메일, 푸시)
- [ ] 히스토리 추적
- [ ] CSV 가져오기/내보내기

## 📞 문의 및 지원

- 📖 문서: 이 저장소의 Markdown 파일들
- 🐛 버그 리포트: GitHub Issues
- 💬 질문: GitHub Discussions

---

## 🎯 다음은?

### 로컬 개발
→ [QUICKSTART.md](QUICKSTART.md) 읽기

### 배포
→ [DEPLOYMENT.md](DEPLOYMENT.md) 읽기

### 커스터마이징
→ [README.md](README.md) 전체 문서 읽기

---

**준비 완료! 지금 바로 시작하세요! 🚀**

```bash
# Backend
cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --reload

# Frontend (새 터미널)
cd frontend && npm install && npm run dev
```

