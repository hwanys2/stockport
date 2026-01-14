# 🚨 Railway "Application failed to respond" 해결 가이드

## 현재 상황
- 도메인: `stockport-production.up.railway.app`
- 포트: 8080
- 오류: Application failed to respond

---

## ✅ 즉시 확인 사항 (체크리스트)

### 1️⃣ Root Directory 설정 확인

**Railway 대시보드에서:**
1. 서비스 클릭 → **Settings** 탭
2. **Service Settings** 섹션 확인
3. **Root Directory** 필드 확인:
   ```
   ✅ 올바른 설정: backend
   ❌ 잘못된 설정: (비어있음) 또는 /backend 또는 ./backend
   ```

**만약 비어있다면:**
- `backend` 입력
- **Save** 클릭
- **Redeploy** 클릭

---

### 2️⃣ Start Command 확인

**Settings → Deploy** 섹션에서:

**✅ 올바른 Start Command:**
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**❌ 잘못된 예시:**
```
uvicorn app.main:app --host 0.0.0.0 --port 8080  # 고정 포트 사용 안 됨!
python app/main.py  # 잘못된 명령어
```

**수정 방법:**
- Start Command 필드에 위의 올바른 명령어 입력
- **Save** 클릭
- **Redeploy** 클릭

---

### 3️⃣ 배포 로그 확인

**Railway 대시보드에서:**
1. 서비스 클릭
2. **Deployments** 탭
3. 최신 배포 클릭
4. **View Logs** 클릭

**확인할 내용:**

#### ✅ 정상 로그 예시:
```
✓ Building
✓ Installing dependencies
✓ Starting application
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:XXXX (Press CTRL+C to quit)
```

#### ❌ 오류 로그 예시:

**"No module named 'app'"**
```
ModuleNotFoundError: No module named 'app'
```
→ **해결**: Root Directory를 `backend`로 설정

**"Port already in use"**
```
Address already in use
```
→ **해결**: Start Command에서 `$PORT` 사용 확인

**"Database connection failed"**
```
could not connect to server
```
→ **해결**: PostgreSQL 플러그인 추가 및 DATABASE_URL 확인

**"Command not found: uvicorn"**
```
uvicorn: command not found
```
→ **해결**: requirements.txt에 uvicorn이 있는지 확인

---

### 4️⃣ 환경변수 확인

**Settings → Variables** 탭에서 확인:

#### 필수 환경변수:
```bash
DATABASE_URL=postgresql://...  # PostgreSQL 플러그인 추가 시 자동 생성
SECRET_KEY=<랜덤-문자열>      # 수동 생성 필요
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
CORS_ORIGINS=["*"]             # 또는 ["https://your-frontend-url"]
```

**SECRET_KEY 생성 방법:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

### 5️⃣ PostgreSQL 플러그인 확인

**Railway 대시보드에서:**
1. 프로젝트 뷰 확인
2. PostgreSQL 플러그인이 있는지 확인
3. 없으면: **"+ New"** → **"Database"** → **"Add PostgreSQL"**

PostgreSQL 추가 후:
- `DATABASE_URL` 환경변수가 자동 생성됨
- Backend 서비스에서 `${{Postgres.DATABASE_URL}}` 사용 가능

---

## 🔧 단계별 해결 방법

### Step 1: Root Directory 설정

```
Settings → Service Settings → Root Directory → backend 입력 → Save
```

### Step 2: Start Command 확인

```
Settings → Deploy → Start Command 확인/수정:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Step 3: 환경변수 설정

```
Settings → Variables → Add:
- SECRET_KEY: <생성한-랜덤-문자열>
- ALGORITHM: HS256
- ACCESS_TOKEN_EXPIRE_MINUTES: 10080
- CORS_ORIGINS: ["*"]
```

### Step 4: PostgreSQL 추가 (없는 경우)

```
프로젝트 뷰 → + New → Database → Add PostgreSQL
```

### Step 5: 재배포

```
Deployments → 최신 배포 → Redeploy
또는
Settings → Deploy → Redeploy 버튼
```

---

## 🧪 배포 후 테스트

### 1. Health Check
```bash
curl https://stockport-production.up.railway.app/health
```

**예상 응답:**
```json
{"status":"healthy"}
```

### 2. Root Endpoint
```bash
curl https://stockport-production.up.railway.app/
```

**예상 응답:**
```json
{
  "message": "Portfolio Manager API",
  "version": "1.0.0",
  "status": "running"
}
```

### 3. API 문서
브라우저에서:
```
https://stockport-production.up.railway.app/docs
```

---

## 📋 최종 체크리스트

배포 전 확인:

- [ ] Root Directory: `backend` 설정됨
- [ ] Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] PostgreSQL 플러그인 추가됨
- [ ] DATABASE_URL 환경변수 설정됨
- [ ] SECRET_KEY 환경변수 설정됨
- [ ] CORS_ORIGINS 환경변수 설정됨
- [ ] 배포 로그에 오류 없음
- [ ] `/health` 엔드포인트 응답 확인

---

## 🆘 여전히 안 되나요?

### 로그 확인
1. Railway 대시보드 → Deployments → 최신 배포 → View Logs
2. 오류 메시지 복사
3. 아래 섹션에서 해당 오류 찾기

### 흔한 오류와 해결책

#### "ModuleNotFoundError: No module named 'app'"
```bash
# 해결: Root Directory를 backend로 설정
```

#### "Address already in use"
```bash
# 해결: Start Command에서 $PORT 사용 확인 (고정 포트 사용 안 됨)
```

#### "could not connect to server"
```bash
# 해결: PostgreSQL 플러그인 추가 및 DATABASE_URL 확인
```

#### "uvicorn: command not found"
```bash
# 해결: requirements.txt에 uvicorn[standard] 있는지 확인
```

#### "Application startup failed"
```bash
# 해결: 배포 로그에서 상세 오류 확인
```

---

## 💡 프로 팁

### 로컬에서 테스트
배포 전 로컬에서 먼저 테스트:
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
curl http://localhost:8000/health
```

### Railway CLI 사용
```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 로그 확인
railway logs
```

---

## 📞 추가 도움

- Railway 문서: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- 프로젝트 문서: [README.md](README.md)

---

**이 가이드로 해결되었나요? 🎉**

문제가 계속되면 Railway 로그의 정확한 오류 메시지를 공유해주시면 더 구체적으로 도와드릴 수 있습니다!

