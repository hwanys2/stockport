# 포트폴리오 관리 시스템 (Portfolio Manager)

목표 비중(타깃)으로 포트폴리오를 만들고, 현재 비중과 비교하며 리밸런싱 시점을 알려주는 웹 애플리케이션입니다.

## 🎯 주요 기능

### 1. 회원 관리
- 회원가입 / 로그인 (JWT 인증)
- 사용자별 포트폴리오 분리 관리

### 2. 포트폴리오 생성
- 종목 검색 (yfinance API 활용)
- 목표 비중 설정 (합계 100% 검증)
- 생성 시점 가격으로 **초기 수량 자동 계산**
- 종목별 허용 오차폭 설정

### 3. 포트폴리오 관리
- 실시간 가격 새로고침
- **현재 비중 자동 계산**
- 목표 비중 vs 현재 비중 시각적 비교
- 보유 수량 수정 가능
- 허용 오차 범위 초과 시 **시각적 경고** (셀 색상 변경)

### 4. 분석 대시보드
- 총 평가금액, 수익금, 수익률 표시
- 종목별 상세 정보 (현재가, 수량, 평가금액, 수익률)
- 비중 차이에 따른 색상 경고 시스템

## 🏗 기술 스택

### Backend
- **FastAPI** - Python 웹 프레임워크
- **SQLAlchemy** - ORM
- **PostgreSQL** - 데이터베이스 (SQLite 로컬 개발 지원)
- **yfinance** - 주식 가격 데이터
- **JWT** - 인증

### Frontend
- **React 18** - UI 라이브러리
- **TypeScript** - 타입 안전성
- **Vite** - 빌드 도구
- **Zustand** - 상태 관리
- **Axios** - HTTP 클라이언트

### 배포
- **Railway** - 호스팅 플랫폼
- GitHub 연동 자동 배포

## 📦 프로젝트 구조

```
portfolio/
├── backend/                # FastAPI 백엔드
│   ├── app/
│   │   ├── models/        # 데이터베이스 모델
│   │   ├── schemas/       # Pydantic 스키마
│   │   ├── routes/        # API 라우트
│   │   ├── services/      # 비즈니스 로직
│   │   ├── config.py      # 설정
│   │   ├── database.py    # DB 연결
│   │   └── main.py        # FastAPI 앱
│   ├── requirements.txt   # Python 의존성
│   └── Procfile          # Railway 배포 설정
│
├── frontend/              # React 프론트엔드
│   ├── src/
│   │   ├── components/   # 재사용 컴포넌트
│   │   ├── pages/        # 페이지 컴포넌트
│   │   ├── services/     # API 클라이언트
│   │   ├── store/        # 상태 관리
│   │   └── App.tsx       # 메인 앱
│   ├── package.json      # npm 의존성
│   └── vite.config.ts    # Vite 설정
│
└── README.md             # 문서
```

## 🚀 로컬 개발 환경 설정

### 사전 요구사항
- Python 3.9+
- Node.js 18+
- npm or yarn

### 1. Backend 설정

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 환경변수 설정 (선택)
cp .env.example .env
# .env 파일을 열어 필요한 설정 변경

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

Backend는 `http://localhost:8000`에서 실행됩니다.
- API 문서: `http://localhost:8000/docs`

### 2. Frontend 설정

```bash
cd frontend

# 패키지 설치
npm install

# 개발 서버 실행
npm run dev
```

Frontend는 `http://localhost:5173`에서 실행됩니다.

## 📊 데이터 모델

### User (사용자)
- id, email, password (해시), created_at

### Asset (종목)
- id, symbol (티커), name, exchange, currency, asset_type

### Portfolio (포트폴리오)
- id, user_id, name, initial_invest_amount, description, created_at

### PortfolioItem (포트폴리오 구성 종목)
- id, portfolio_id, asset_id
- **target_weight** (목표 비중 %)
- **tolerance** (허용 오차폭 %)
- **entry_price** (생성 시점 가격, 수정 불가)
- **initial_quantity** (초기 수량)
- **current_quantity** (현재 수량, 수정 가능)

## 🔑 핵심 로직

### 1. 포트폴리오 생성 시

```python
# 각 종목별
종목별 투자액 = 총 투자금 × (목표 비중 / 100)
초기 수량 = 종목별 투자액 / entry_price (생성 시점 현재가)
```

### 2. 현재 비중 계산

```python
# 새로고침 시
종목별 평가금액 = current_quantity × latest_price
총 평가금액 = Σ(종목별 평가금액)
현재 비중 = (종목별 평가금액 / 총 평가금액) × 100
```

### 3. 경고 시스템

```python
비중 차이 = 현재 비중 - 목표 비중

if |비중 차이| > 허용오차:
    경고 표시 (색상 변경)
```

## 🎨 UI 기능

### 색상 경고 시스템
- **정상**: 흰색 배경
- **경고** (허용오차 초과): 노란색 배경
- **위험** (허용오차 1.5배 초과): 빨간색 배경

### 주요 페이지
1. **로그인/회원가입** - 인증
2. **대시보드** - 포트폴리오 목록
3. **포트폴리오 생성** - 종목 검색 및 비중 설정
4. **포트폴리오 상세** - 분석 및 관리

## 🚢 Railway 배포

### Backend 배포

1. Railway 프로젝트 생성
2. GitHub 저장소 연결
3. Root Directory: `/backend` 설정
4. PostgreSQL 플러그인 추가
5. 환경변수 설정:
   ```
   DATABASE_URL=<PostgreSQL URL>
   SECRET_KEY=<랜덤 문자열>
   CORS_ORIGINS=["https://your-frontend-url.railway.app"]
   ```

### Frontend 배포

1. 새 Railway 서비스 생성
2. Root Directory: `/frontend` 설정
3. 환경변수 설정:
   ```
   VITE_API_URL=https://your-backend-url.railway.app
   ```
4. 빌드 커맨드는 `railway.json`에 자동 설정됨

### GitHub 자동 배포

1. Railway에 GitHub 앱 설치
2. 저장소 연결
3. `main` 브랜치에 push하면 자동 배포

```bash
git add .
git commit -m "Deploy to Railway"
git push origin main
```

## 📝 API 엔드포인트

### 인증
- `POST /auth/signup` - 회원가입
- `POST /auth/login` - 로그인

### 종목
- `GET /assets/search?q={query}` - 종목 검색
- `POST /assets` - 종목 추가
- `GET /assets/{id}/price` - 현재가 조회

### 포트폴리오
- `GET /portfolios` - 포트폴리오 목록
- `POST /portfolios` - 포트폴리오 생성
- `GET /portfolios/{id}` - 포트폴리오 상세
- `GET /portfolios/{id}/analysis` - 포트폴리오 분석 (핵심!)
- `PATCH /portfolios/{id}/items/{item_id}` - 수량 업데이트
- `DELETE /portfolios/{id}` - 포트폴리오 삭제

## 🛠 개발 팁

### Backend 테스트
```bash
# API 문서로 테스트
http://localhost:8000/docs

# 또는 curl
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

### Frontend 빌드
```bash
cd frontend
npm run build
npm run preview  # 빌드 결과 미리보기
```

## 🔮 향후 개선 사항

- [ ] 리밸런싱 제안 (매수/매도 수량 계산)
- [ ] 알림 기능 (이메일, 푸시)
- [ ] 차트 시각화 (비중 파이 차트, 수익률 그래프)
- [ ] 히스토리 추적 (비중 변화 기록)
- [ ] 다중 포트폴리오 비교
- [ ] 한국 주식 지원 강화
- [ ] 배당금 추적
- [ ] CSV 가져오기/내보내기

## 📄 라이선스

MIT License

## 👨‍💻 개발자

포트폴리오 관리 프로젝트

---

**문의사항이나 버그 리포트는 GitHub Issues를 이용해주세요!**

