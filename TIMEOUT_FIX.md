# 🚨 Railway "connection dial timeout" 해결 가이드

## 문제 분석

로그에서 확인된 오류:
```
upstreamErrors: "connection dial timeout"
upstreamAddress: "" (비어있음)
upstreamRqDuration: 15002ms
responseDetails: "Retried single replica"
```

## 원인
애플리케이션이 **포트에 바인딩되지 않았거나 시작되지 않았습니다**.

---

## ✅ 즉시 해결 방법

### 1단계: 배포 로그 확인 (가장 중요!)

**Railway 대시보드에서:**
1. 서비스 클릭
2. **Deployments** 탭
3. 최신 배포 클릭
4. **View Logs** 클릭

**확인할 내용:**

#### ✅ 정상 시작 로그:
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:XXXX (Press CTRL+C to quit)
```

#### ❌ 문제가 있는 로그:

**애플리케이션이 시작되지 않음:**
```
(로그가 비어있거나 빌드만 있고 시작 로그 없음)
```
→ **해결**: Start Command 확인

**데이터베이스 연결 실패:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```
→ **해결**: PostgreSQL 플러그인 추가 및 DATABASE_URL 확인

**환경변수 오류:**
```
pydantic_core._pydantic_core.ValidationError
```
→ **해결**: SECRET_KEY 등 필수 환경변수 설정

**포트 바인딩 실패:**
```
Address already in use
```
→ **해결**: Start Command에서 `$PORT` 사용 확인

---

### 2단계: Start Command 확인 (필수!)

**Settings → Deploy** 섹션에서:

**✅ 올바른 Start Command:**
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**❌ 잘못된 예시:**
```
uvicorn app.main:app --port 8080  # 고정 포트 사용 안 됨!
uvicorn app.main:app  # 포트 지정 없음
python app/main.py  # 잘못된 명령어
```

**확인 방법:**
- Settings → Deploy → Start Command 필드 확인
- `$PORT` 환경변수를 사용하는지 확인
- `--host 0.0.0.0`이 있는지 확인

---

### 3단계: 환경변수 확인

**Settings → Variables** 탭에서 확인:

#### 필수 환경변수:

```bash
# 1. DATABASE_URL (PostgreSQL 플러그인 추가 시 자동 생성)
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

**PostgreSQL 플러그인 추가:**
- 프로젝트 뷰 → "+ New" → "Database" → "Add PostgreSQL"
- 추가 후 `DATABASE_URL`이 자동 생성됨

```bash
# 2. SECRET_KEY (수동 생성 필요!)
SECRET_KEY=<랜덤-문자열-32자-이상>
```

**SECRET_KEY 생성:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

또는 온라인: https://randomkeygen.com/

```bash
# 3. 기타 환경변수
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
CORS_ORIGINS=["*"]
```

---

### 4단계: Root Directory 확인

**Settings → Service Settings** 섹션에서:

```
Root Directory: backend
```

⚠️ **이게 설정되지 않으면 모든 것이 실패합니다!**

---

### 5단계: 재배포 및 로그 모니터링

1. **Deployments** 탭
2. **Redeploy** 버튼 클릭
3. **View Logs** 클릭하여 실시간 모니터링
4. 다음 메시지가 나타나는지 확인:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:XXXX
   ```

---

## 🔍 상세 진단

### 애플리케이션이 시작되는지 확인

배포 로그에서 다음을 찾으세요:

#### 1. 빌드 단계
```
✓ Building
✓ Installing dependencies
✓ Build complete
```

#### 2. 시작 단계 (중요!)
```
INFO:     Started server process
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:XXXX
```

**이 메시지가 없다면:**
- 애플리케이션이 시작되지 않음
- Start Command 확인 필요
- 환경변수 확인 필요

#### 3. 런타임 오류
```
ERROR:    Application startup failed
```
→ 로그에서 상세 오류 확인

---

## 📋 완전한 체크리스트

### Railway Settings:
- [ ] **Root Directory**: `backend` 설정됨
- [ ] **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] **Python Version**: `3.11` (또는 자동 감지)

### 환경변수:
- [ ] **DATABASE_URL**: PostgreSQL 플러그인 추가됨
- [ ] **SECRET_KEY**: 랜덤 문자열 설정됨
- [ ] **ALGORITHM**: `HS256`
- [ ] **ACCESS_TOKEN_EXPIRE_MINUTES**: `10080`
- [ ] **CORS_ORIGINS**: `["*"]`

### 배포 로그:
- [ ] 빌드 성공
- [ ] **"Uvicorn running"** 메시지 확인됨
- [ ] 오류 메시지 없음

---

## 🧪 테스트 방법

### 배포 후 즉시 테스트:

```bash
curl https://stockport-production.up.railway.app/health
```

**예상 응답:**
```json
{"status":"healthy"}
```

**502 오류가 계속되면:**
- 애플리케이션이 시작되지 않음
- 배포 로그 확인 필요

---

## 💡 디버깅 팁

### 1. 간단한 Start Command로 테스트

임시로 Start Command 변경:
```bash
python -c "import sys; print('Python:', sys.version); import uvicorn; print('Uvicorn OK')"
```

이렇게 하면 Python과 Uvicorn이 설치되었는지 확인 가능

### 2. 로컬에서 먼저 테스트

```bash
cd backend
export DATABASE_URL="postgresql://..."
export SECRET_KEY="test-secret-key"
export PORT=8000
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

로컬에서 작동하면 Railway 설정 문제일 가능성이 높습니다.

### 3. Railway CLI로 로그 확인

```bash
npm install -g @railway/cli
railway login
railway logs --follow
```

---

## 🆘 여전히 안 되나요?

### 배포 로그 전체 확인:

1. Railway → Deployments → 최신 배포
2. View Logs 클릭
3. **전체 로그 복사**
4. 다음을 확인:

**애플리케이션 시작 로그가 있는가?**
- 있음 → 다른 문제 (포트, 환경변수)
- 없음 → Start Command 문제

**오류 메시지가 있는가?**
- 있음 → 오류 메시지에 따라 해결
- 없음 → Start Command 확인

---

## 🎯 가장 흔한 원인 Top 3

1. **Start Command 오류** (95%)
   - `$PORT` 사용 안 함
   - `--host 0.0.0.0` 없음
   → **해결**: Start Command 확인

2. **환경변수 없음** (90%)
   - DATABASE_URL 없음
   - SECRET_KEY 없음
   → **해결**: 환경변수 설정

3. **Root Directory 미설정** (85%)
   - `backend`로 설정 안 됨
   → **해결**: Root Directory 설정

---

## 📞 추가 도움

- Railway 문서: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- 프로젝트 문서: [README.md](README.md)

---

**가장 중요한 것: 배포 로그에서 "Uvicorn running" 메시지를 확인하세요!** 🎯

이 메시지가 없다면 애플리케이션이 시작되지 않은 것입니다.

