# Railway 배포 가이드

이 문서는 포트폴리오 관리 애플리케이션을 Railway에 배포하는 상세 가이드입니다.

## 📋 사전 준비

1. **Railway 계정 생성**
   - https://railway.app 에서 회원가입
   - GitHub 계정으로 가입 권장

2. **GitHub 저장소 준비**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

## 🗄 데이터베이스 설정 (Backend)

### Step 1: Railway 프로젝트 생성

1. Railway 대시보드에서 "New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. 저장소 선택 및 연결

### Step 2: PostgreSQL 추가

1. 프로젝트에서 "+ New" → "Database" → "Add PostgreSQL" 클릭
2. 자동으로 `DATABASE_URL` 환경변수가 생성됨

### Step 3: Backend 서비스 설정

1. 프로젝트에서 GitHub 저장소 서비스 선택
2. Settings → 다음 설정 변경:

#### Build & Deploy Settings
```
Root Directory: /backend
Build Command: (비워둠, nixpacks가 자동 처리)
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### Environment Variables
```bash
# 자동 설정됨 (PostgreSQL 플러그인에서)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# 수동 추가 필요
SECRET_KEY=<랜덤-긴-문자열-여기에-입력>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# CORS 설정 (프론트엔드 URL로 변경 예정)
CORS_ORIGINS=["*"]
```

**SECRET_KEY 생성 방법:**
```bash
# Python으로 생성
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: 배포

1. Settings → Deploy 탭
2. "Deploy" 버튼 클릭
3. 빌드 로그 확인
4. 배포 완료 후 URL 복사 (예: `https://your-backend.railway.app`)

### Step 5: API 테스트

```bash
# Health check
curl https://your-backend.railway.app/health

# API 문서 접속
https://your-backend.railway.app/docs
```

## 🎨 Frontend 배포

### Step 1: 새 서비스 추가

1. 같은 프로젝트에서 "+ New" → "GitHub Repo" 클릭
2. 같은 저장소 선택 (monorepo 구조)

### Step 2: Frontend 서비스 설정

#### Settings → Build & Deploy
```
Root Directory: /frontend
Build Command: npm install && npm run build
Start Command: npm run preview -- --host 0.0.0.0 --port $PORT
```

#### Environment Variables
```bash
# Backend URL 설정
VITE_API_URL=https://your-backend.railway.app
```

**중요:** Backend URL은 첫 번째 단계에서 복사한 URL을 사용하세요!

### Step 3: 배포

1. "Deploy" 버튼 클릭
2. 빌드 완료 후 Frontend URL 복사 (예: `https://your-frontend.railway.app`)

### Step 4: CORS 업데이트

Backend 서비스로 돌아가서 환경변수 수정:

```bash
CORS_ORIGINS=["https://your-frontend.railway.app"]
```

변경 후 Backend 재배포 (자동으로 재시작됨)

## 🔄 자동 배포 설정

### GitHub 푸시로 자동 배포

Railway는 기본적으로 GitHub 푸시 시 자동 배포됩니다.

```bash
git add .
git commit -m "Update feature"
git push origin main
```

### 배포 브랜치 변경 (선택)

Settings → Deploy → Branch: `main` (또는 원하는 브랜치)

## 🐛 트러블슈팅

### Backend 배포 실패

#### 문제 1: 포트 바인딩 실패
```
❌ Error: Address already in use
```

**해결:**
- Start Command가 `--port $PORT` 를 사용하는지 확인
- Procfile 또는 railway.json 확인

#### 문제 2: 데이터베이스 연결 실패
```
❌ Error: could not connect to database
```

**해결:**
```bash
# DATABASE_URL이 올바른지 확인
echo ${{Postgres.DATABASE_URL}}

# requirements.txt에 psycopg2-binary 있는지 확인
grep psycopg2 backend/requirements.txt
```

#### 문제 3: Import 에러
```
❌ ModuleNotFoundError: No module named 'app'
```

**해결:**
- Root Directory가 `/backend`로 설정되어 있는지 확인
- Start Command: `uvicorn app.main:app` (not `backend.app.main:app`)

### Frontend 배포 실패

#### 문제 1: API 연결 실패
```
❌ Network Error / CORS Error
```

**해결:**
1. VITE_API_URL이 올바른 Backend URL인지 확인
2. Backend의 CORS_ORIGINS에 Frontend URL 추가했는지 확인
3. Backend URL이 `https://`로 시작하는지 확인 (not `http://`)

#### 문제 2: 빌드 실패
```
❌ Error: Cannot find module
```

**해결:**
```bash
# package.json 확인
cat frontend/package.json

# 로컬에서 빌드 테스트
cd frontend
npm install
npm run build
```

#### 문제 3: 페이지 새로고침 시 404
```
❌ 404 Not Found (SPA routing issue)
```

**해결:**
- Vite preview는 기본적으로 SPA routing을 지원합니다
- 문제가 지속되면 `vite-plugin-static-copy` 사용 고려

## 📊 환경변수 요약

### Backend 환경변수
| 변수명 | 예시 | 필수 |
|--------|------|------|
| DATABASE_URL | postgresql://... | ✅ |
| SECRET_KEY | random-secret-key | ✅ |
| ALGORITHM | HS256 | ✅ |
| ACCESS_TOKEN_EXPIRE_MINUTES | 10080 | ⚠️ |
| CORS_ORIGINS | ["https://..."] | ✅ |

### Frontend 환경변수
| 변수명 | 예시 | 필수 |
|--------|------|------|
| VITE_API_URL | https://backend.railway.app | ✅ |

## 🔐 보안 체크리스트

- [ ] SECRET_KEY는 랜덤하고 긴 문자열 사용
- [ ] CORS_ORIGINS에 실제 Frontend URL만 허용
- [ ] DATABASE_URL은 절대 공개하지 않기
- [ ] GitHub에 `.env` 파일 커밋하지 않기 (`.gitignore` 확인)
- [ ] API 문서 (`/docs`)를 프로덕션에서 비활성화 고려

## 📈 모니터링

### Railway 대시보드에서 확인
- CPU/Memory 사용량
- 요청 로그
- 에러 로그
- 배포 히스토리

### 로그 확인
```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 로그 보기
railway logs --service backend
railway logs --service frontend
```

## 💰 비용 관리

### Railway 무료 플랜
- $5 무료 크레딧 (매월)
- 충분한 경우: 소규모 프로젝트

### 비용 절감 팁
- 사용하지 않는 서비스 중지
- 데이터베이스 크기 모니터링
- 불필요한 빌드 트리거 방지

## 🚀 배포 체크리스트

### Backend
- [ ] PostgreSQL 추가
- [ ] Root Directory: `/backend`
- [ ] 환경변수 모두 설정
- [ ] Start Command 확인
- [ ] 배포 성공
- [ ] `/health` 엔드포인트 테스트
- [ ] `/docs` 접속 확인

### Frontend
- [ ] Root Directory: `/frontend`
- [ ] VITE_API_URL 설정
- [ ] Build Command 확인
- [ ] 배포 성공
- [ ] 웹사이트 접속 테스트
- [ ] 로그인 기능 테스트

### 통합 테스트
- [ ] Backend CORS 업데이트
- [ ] 회원가입 테스트
- [ ] 로그인 테스트
- [ ] 포트폴리오 생성 테스트
- [ ] 가격 새로고침 테스트

---

**배포 완료! 🎉**

문제가 있다면:
1. Railway 로그 확인
2. 브라우저 개발자 도구 (F12) 확인
3. GitHub Issues에 문의

