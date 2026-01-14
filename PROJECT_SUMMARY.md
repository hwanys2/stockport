# 프로젝트 요약

## ✅ 구현 완료 항목

### 🎯 핵심 요구사항

#### 1. 전체 목표 ✅
- ✅ 목표 비중(타깃) 기반 포트폴리오 생성
- ✅ 시간 경과에 따른 현재가 변동 추적
- ✅ 현재 평가금액 / 현재 비중 자동 계산
- ✅ 목표 비중 vs 현재 비중 직관적 비교
- ✅ 허용 오차 범위 벗어날 시 시각적 경고 (셀 색상 변경)

#### 2. 시스템 구조 ✅
- ✅ Frontend + Backend 통합 구조
- ✅ Railway 배포 준비 완료
- ✅ GitHub 자동 배포 설정 가능
- ✅ yfinance를 통한 외부 주식 데이터 연동
- ✅ 종목 검색 + 실시간 가격 조회 기능

#### 3. 회원 기능 ✅
- ✅ 회원가입 / 로그인 (JWT 인증)
- ✅ 개인별 데이터 분리
- ✅ 사용자별 포트폴리오 소유권 관리

#### 4. 데이터 모델 ✅
- ✅ User: id, email, password_hash, created_at
- ✅ Asset: symbol, name, exchange, currency, asset_type
- ✅ Portfolio: name, initial_invest_amount, description
- ✅ PortfolioItem:
  - ✅ target_weight (목표 비중)
  - ✅ tolerance (허용 오차폭)
  - ✅ entry_price (생성 시점 가격, 수정 불가)
  - ✅ initial_quantity (초기 수량)
  - ✅ current_quantity (현재 수량, 수정 가능)

#### 5. 포트폴리오 생성 흐름 ✅
- ✅ Step A: 포트폴리오 이름 + 총 투자금액 입력
- ✅ Step B: 종목 검색 및 선택 (다중 종목 지원)
- ✅ Step C: 목표 비중 설정 (합계 100% 검증)
- ✅ Step D: 생성 시점 현재가로 초기 수량 자동 계산
  - ✅ 종목별 투자액 = 총투자금 × 목표비중
  - ✅ 초기 수량 = 종목별 투자액 ÷ entry_price
  - ✅ entry_price 고정 (수정 불가)
  - ✅ current_quantity 수정 가능

#### 6. 가격 업데이트 ✅
- ✅ "새로고침" 버튼으로 최신 가격 조회
- ✅ 실시간 재계산 로직:
  - ✅ 종목별 평가금액 = current_quantity × latest_price
  - ✅ 총 평가금액 = Σ(종목별 평가금액)
  - ✅ 현재 비중 = 종목별 평가금액 ÷ 총 평가금액 × 100

#### 7. 비교 UI ✅
- ✅ 종목명 / 티커
- ✅ 목표 비중 (target %)
- ✅ 현재 비중 (current %)
- ✅ 차이 (diff = current - target)
- ✅ 현재가 (latest price)
- ✅ 수량 (current_quantity, 수정 가능)
- ✅ 평가금액 (value)
- ✅ 허용오차 (tolerance %)
- ✅ 경고 (조건부 색상 변경)

#### 8. MVP 기능 ✅
- ✅ 회원가입 / 로그인
- ✅ 포트폴리오 생성 (투자금 + 종목 + 목표비중)
- ✅ 생성 시점 가격 조회 + 초기 수량 자동 계산 + 저장
- ✅ 보유 수량 수정
- ✅ 새로고침으로 최신가 업데이트 + 현재 비중 계산
- ✅ 허용오차 설정 + 범위 벗어나면 색상 변경

## 📁 프로젝트 구조

```
portfolio/
├── backend/                          # Python FastAPI Backend
│   ├── app/
│   │   ├── models/
│   │   │   ├── user.py              # User 모델
│   │   │   └── portfolio.py         # Asset, Portfolio, PortfolioItem 모델
│   │   ├── schemas/
│   │   │   ├── user.py              # User 스키마
│   │   │   └── portfolio.py         # Portfolio 스키마
│   │   ├── routes/
│   │   │   ├── auth.py              # 인증 API
│   │   │   ├── assets.py            # 종목 API
│   │   │   └── portfolios.py        # 포트폴리오 API
│   │   ├── services/
│   │   │   ├── auth.py              # 인증 로직 (JWT)
│   │   │   └── market.py            # 주식 가격 조회 (yfinance)
│   │   ├── config.py                # 설정
│   │   ├── database.py              # DB 연결
│   │   └── main.py                  # FastAPI 앱
│   ├── requirements.txt             # Python 의존성
│   ├── Procfile                     # Railway 배포
│   └── railway.json                 # Railway 설정
│
├── frontend/                         # React TypeScript Frontend
│   ├── public/
│   │   └── vite.svg                 # 아이콘
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.tsx           # 네비게이션
│   │   │   └── Navbar.css
│   │   ├── pages/
│   │   │   ├── Login.tsx            # 로그인 페이지
│   │   │   ├── Signup.tsx           # 회원가입 페이지
│   │   │   ├── Dashboard.tsx        # 대시보드
│   │   │   ├── CreatePortfolio.tsx  # 포트폴리오 생성
│   │   │   ├── PortfolioDetail.tsx  # 포트폴리오 상세
│   │   │   └── (각 CSS 파일)
│   │   ├── services/
│   │   │   └── api.ts               # API 클라이언트
│   │   ├── store/
│   │   │   └── authStore.ts         # 상태 관리 (Zustand)
│   │   ├── App.tsx                  # 메인 앱
│   │   ├── main.tsx                 # 엔트리 포인트
│   │   └── index.css                # 글로벌 스타일
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── railway.json
│
├── .github/
│   └── workflows/
│       └── deploy.yml               # GitHub Actions (선택)
│
├── README.md                         # 전체 문서
├── DEPLOYMENT.md                     # 배포 가이드
├── QUICKSTART.md                     # 빠른 시작
├── PROJECT_SUMMARY.md               # 이 파일
└── .gitignore                       # Git 제외 파일
```

## 🎨 주요 화면

### 1. 로그인 / 회원가입
- 이메일 + 비밀번호 입력
- JWT 토큰 발급 및 로컬 저장

### 2. 대시보드
- 포트폴리오 카드 그리드
- 생성/삭제 버튼
- 초기 투자금, 생성일 표시

### 3. 포트폴리오 생성
- **기본 정보**: 이름, 설명, 투자금액
- **종목 선택**: 검색 → 추가
- **목표 비중 설정**: 각 종목의 target_weight, tolerance
- **자동 계산**: 생성 시점 가격으로 수량 계산

### 4. 포트폴리오 상세
- **요약**: 초기 투자금, 현재 평가금액, 수익금, 수익률
- **종목 테이블**:
  - 종목명, 목표 비중, 현재 비중, 차이
  - 현재가, 수량, 평가금액, 수익률
  - 수량 수정 버튼
- **색상 경고**:
  - 노란색: 허용 오차 초과
  - 빨간색: 허용 오차 크게 초과

## 🔧 기술 스택

| 구분 | 기술 |
|------|------|
| Backend | FastAPI, SQLAlchemy, PostgreSQL/SQLite |
| Frontend | React 18, TypeScript, Vite |
| 인증 | JWT (python-jose) |
| 주식 데이터 | yfinance |
| 상태 관리 | Zustand |
| HTTP | Axios |
| 배포 | Railway |
| CI/CD | GitHub Actions |

## 📊 API 엔드포인트

### 인증
- `POST /auth/signup` - 회원가입
- `POST /auth/login` - 로그인 (JWT 발급)

### 종목
- `GET /assets/search?q={query}` - 종목 검색
- `POST /assets` - 종목 추가
- `GET /assets/{id}` - 종목 조회
- `GET /assets/{id}/price` - 현재가 조회

### 포트폴리오
- `GET /portfolios` - 목록
- `POST /portfolios` - 생성 (자동 수량 계산)
- `GET /portfolios/{id}` - 상세
- `GET /portfolios/{id}/analysis` - **분석 (핵심 API)**
- `PATCH /portfolios/{id}/items/{item_id}` - 수량 수정
- `DELETE /portfolios/{id}` - 삭제

## 💡 핵심 알고리즘

### 포트폴리오 생성 시

```python
for each item in items:
    # 1. 현재가 조회
    entry_price = get_current_price(item.asset.symbol)
    
    # 2. 종목별 투자액 계산
    item_invest_amount = total_invest × (target_weight / 100)
    
    # 3. 초기 수량 계산
    initial_quantity = item_invest_amount / entry_price
    
    # 4. 저장
    save(entry_price, initial_quantity, current_quantity=initial_quantity)
```

### 포트폴리오 분석 시 (새로고침)

```python
# Pass 1: 총 평가금액 계산
total_value = 0
for item in items:
    latest_price = get_current_price(item.asset.symbol)
    item_value = item.current_quantity × latest_price
    total_value += item_value

# Pass 2: 현재 비중 및 경고 계산
for item in items:
    latest_price = get_current_price(item.asset.symbol)
    item_value = item.current_quantity × latest_price
    
    # 현재 비중
    current_weight = (item_value / total_value) × 100
    
    # 비중 차이
    weight_diff = current_weight - item.target_weight
    
    # 경고 여부
    is_out_of_range = |weight_diff| > item.tolerance
    
    # 셀 색상
    if is_out_of_range:
        if |weight_diff| > item.tolerance × 1.5:
            color = "danger"  # 빨간색
        else:
            color = "warning"  # 노란색
```

## 🚀 배포 상태

### 로컬 개발 환경
- ✅ Backend: `http://localhost:8000`
- ✅ Frontend: `http://localhost:5173`

### Railway 배포 (예정)
1. Backend 서비스 + PostgreSQL
2. Frontend 서비스
3. 자동 HTTPS, 환경변수 설정

## 📝 다음 단계

### 즉시 실행 가능
1. `QUICKSTART.md` 참고하여 로컬 실행
2. 회원가입 → 포트폴리오 생성 → 관리 테스트
3. Railway 배포 (`DEPLOYMENT.md` 참고)

### 향후 개선 가능
- [ ] 리밸런싱 제안 (매수/매도 수량 계산)
- [ ] 차트 시각화 (파이 차트, 수익률 그래프)
- [ ] 알림 기능
- [ ] 히스토리 추적
- [ ] CSV 가져오기/내보내기
- [ ] 한국 주식 지원 강화

## ✨ 특징

1. **자동 계산**: 생성 시점 가격으로 수량 자동 계산
2. **비중 관리**: 목표 vs 현재 비중 실시간 비교
3. **시각적 경고**: 허용 오차 벗어나면 색상으로 알림
4. **유연한 수정**: 수량 수정으로 매매 반영 가능
5. **간편한 배포**: Railway로 쉬운 배포

---

**프로젝트 완성! 🎉**

모든 요구사항이 구현되었으며, 즉시 사용 가능한 상태입니다.

