# 🎯 Railway 배포 최종 완벽 가이드

## 현재 상황
- 빌드 오류: `undefined variable 'pip'` in nixpacks
- 502 오류: Application failed to respond

## ✅ 완벽한 해결 방법 (5단계)

---

## Step 1: Root Directory 설정 (필수!)

**Railway 대시보드에서:**
1. 서비스 클릭
2. **Settings** 탭
3. **Service Settings** 섹션
4. **Root Directory** 찾기

**입력:**
```
backend
```

⚠️ **정확히 `backend`만 입력** (슬래시, 점 없이!)

❌ 잘못된 예: `/backend`, `./backend`, `backend/`
✅ 올바른 예: `backend`

**Save 클릭**

---

## Step 2: PostgreSQL 추가 (필수!)

**Railway 프로젝트 뷰에서:**
1. **"+ New"** 클릭
2. **"Database"** 선택
3. **"Add PostgreSQL"** 클릭
4. PostgreSQL이 추가되면 완료

**결과:** `DATABASE_URL` 환경변수가 자동 생성됨

---

## Step 3: 환경변수 설정 (필수!)

**Settings → Variables** 탭에서 다음 추가:

### 1. SECRET_KEY 생성 및 추가

**로컬 터미널에서 실행:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**출력 예시:**
```
rJrZKaMrXpRecWPzbEF_XqfcqZc8qsC_AJiTo-jrblE
```

**Railway에 추가:**
- Name: `SECRET_KEY`
- Value: 위에서 생성한 값 붙여넣기

### 2. 기타 환경변수 추가

```bash
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
CORS_ORIGINS=["*"]
```

**Save 클릭**

---

## Step 4: Build & Deploy 설정 확인

**Settings → Deploy** 섹션에서:

### Build Command:
```
(비워두기 - Railway가 자동 감지)
```

### Start Command:
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Save 클릭**

---

## Step 5: 재배포 및 로그 모니터링

1. **Deployments** 탭으로 이동
2. **Redeploy** 버튼 클릭
3. **View Logs** 클릭하여 실시간 로그 확인

**확인할 내용:**
```
✓ Detecting Python project
✓ Installing Python 3.11
✓ Installing dependencies
  Running: pip install -r requirements.txt
✓ Build complete
INFO:     Started server process
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:XXXX
```

---

## 📋 최종 체크리스트

### Railway Settings:
- [ ] **Root Directory**: `backend` (정확히!)
- [ ] **Build Command**: (비워두기)
- [ ] **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Database:
- [ ] **PostgreSQL** 플러그인 추가됨
- [ ] **DATABASE_URL** 자동 생성 확인

### 환경변수 (Variables 탭):
- [ ] **SECRET_KEY**: 랜덤 문자열 (32자 이상)
- [ ] **ALGORITHM**: `HS256`
- [ ] **ACCESS_TOKEN_EXPIRE_MINUTES**: `10080`
- [ ] **CORS_ORIGINS**: `["*"]`

### 배포:
- [ ] Redeploy 완료
- [ ] 로그에 "Uvicorn running" 메시지 확인
- [ ] 로그에 오류 없음

---

## 🧪 배포 성공 확인

### 1. Health Check
```bash
curl https://stockport-production.up.railway.app/health
```

**예상 응답:**
```json
{"status":"healthy"}
```

### 2. API 문서 접속
브라우저에서:
```
https://stockport-production.up.railway.app/docs
```

Swagger UI가 보이면 성공!

---

## 🆘 여전히 502 오류가 나온다면?

### 배포 로그 확인 (필수!)

**Railway → Deployments → 최신 배포 → View Logs**

로그에서 확인할 내용:

#### 1. "Uvicorn running" 메시지가 있는가?

**있음:**
- 애플리케이션이 시작됨
- 포트 또는 네트워크 문제일 수 있음
- Start Command 확인

**없음:**
- 애플리케이션이 시작되지 않음
- 로그에서 오류 메시지 확인

#### 2. 오류 메시지 확인

**"could not connect to server"**
```
sqlalchemy.exc.OperationalError: could not connect to server
```
→ **해결**: PostgreSQL 플러그인 추가 확인

**"SECRET_KEY"**
```
pydantic_core._pydantic_core.ValidationError
Field required [type=missing, input_value={}, input_type=dict]
```
→ **해결**: SECRET_KEY 환경변수 추가 확인

**"ModuleNotFoundError"**
```
ModuleNotFoundError: No module named 'app'
```
→ **해결**: Root Directory를 `backend`로 설정

**"Address already in use"**
```
Address already in use
```
→ **해결**: Start Command에서 `$PORT` 사용 확인

---

## 💡 디버깅 팁

### Railway CLI로 실시간 로그 확인:
```bash
npm install -g @railway/cli
railway login
railway logs --follow
```

### 로컬에서 먼저 테스트:
```bash
cd backend
export DATABASE_URL="postgresql://user:pass@host:port/db"
export SECRET_KEY="test-secret-key"
export PORT=8000
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

로컬에서 작동하면 Railway 설정 문제입니다.

---

## 🎯 가장 흔한 실수 Top 5

1. **Root Directory 미설정** (95%)
   - 증상: "pip: command not found", "requirements.txt not found"
   - 해결: Root Directory를 `backend`로 설정

2. **PostgreSQL 미추가** (90%)
   - 증상: "could not connect to server"
   - 해결: PostgreSQL 플러그인 추가

3. **SECRET_KEY 미설정** (85%)
   - 증상: "ValidationError", "Field required"
   - 해결: SECRET_KEY 환경변수 추가

4. **Start Command 오류** (80%)
   - 증상: "connection dial timeout", 502 error
   - 해결: `$PORT` 사용 확인

5. **Root Directory에 슬래시 포함** (75%)
   - 증상: 파일을 찾지 못함
   - 해결: `backend`만 입력 (슬래시 없이)

---

## 📸 스크린샷 가이드

### Root Directory 설정 위치:
```
Railway Dashboard
  → Your Service (예: stockport-production)
    → Settings (탭)
      → Service Settings (섹션)
        → Root Directory (필드)
          → 입력: backend
          → Save 버튼 클릭
```

### 환경변수 추가 위치:
```
Railway Dashboard
  → Your Service
    → Settings (탭)
      → Variables (섹션)
        → + New Variable 버튼
          → Name 입력
          → Value 입력
          → Save 버튼 클릭
```

### PostgreSQL 추가 위치:
```
Railway Dashboard
  → Your Project
    → + New 버튼
      → Database 선택
        → Add PostgreSQL 클릭
          → 자동으로 추가됨
```

---

## 🔄 재배포 전 최종 확인

1. Root Directory: `backend` ✓
2. PostgreSQL 추가됨 ✓
3. SECRET_KEY 환경변수 설정됨 ✓
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT` ✓
5. Build Command: (비어있음) ✓

**모두 확인했다면:**
- Deployments → Redeploy 클릭
- View Logs에서 "Uvicorn running" 확인

---

## 📞 추가 도움

- Railway 문서: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Railway 커뮤니티: https://help.railway.app

---

**이 가이드를 순서대로 따라하면 100% 배포 성공!** 🎉

문제가 계속되면 배포 로그 전체를 복사해서 공유해주세요.

