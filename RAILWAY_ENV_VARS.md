# 🔐 Railway 환경변수 설정 가이드

## ✅ 필수 환경변수 (반드시 설정 필요)

### 1. DATABASE_URL (자동 생성)

**설정 방법:**
1. Railway 프로젝트에서 **"+ New"** 클릭
2. **"Database"** 선택
3. **"Add PostgreSQL"** 클릭
4. 자동으로 `DATABASE_URL` 환경변수가 생성됨

**Backend 서비스에서 사용:**
- **Variables** 탭에서:
  ```
  DATABASE_URL=${{Postgres.DATABASE_URL}}
  ```
  또는 PostgreSQL 플러그인을 추가하면 자동으로 연결됨

**❌ 수동으로 추가할 필요 없음!** (PostgreSQL 플러그인 추가 시 자동 생성)

---

### 2. SECRET_KEY (수동 생성 필요!)

**⚠️ 중요: 아무거나 넣으면 안 됩니다!**

**보안 요구사항:**
- 최소 32자 이상의 랜덤 문자열
- 예측 불가능한 값
- 프로덕션에서는 반드시 강력한 값 사용

**생성 방법:**

#### 방법 1: Python으로 생성 (권장)
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**예시 출력:**
```
rJrZKaMrXpRecWPzbEF_XqfcqZc8qsC_AJiTo-jrblE
```

#### 방법 2: 온라인 생성기
https://randomkeygen.com/ → "CodeIgniter Encryption Keys" 사용

#### 방법 3: OpenSSL
```bash
openssl rand -hex 32
```

**Railway에 추가:**
1. **Settings** → **Variables** 탭
2. **"+ New Variable"** 클릭
3. **Name**: `SECRET_KEY`
4. **Value**: 위에서 생성한 랜덤 문자열
5. **Save** 클릭

**예시:**
```
SECRET_KEY=rJrZKaMrXpRecWPzbEF_XqfcqZc8qsC_AJiTo-jrblE
```

---

### 3. ALGORITHM (선택, 기본값 있음)

**설정:**
```
ALGORITHM=HS256
```

**❌ 필수 아님** (코드에 기본값 있음, 하지만 명시하는 것이 좋음)

---

### 4. ACCESS_TOKEN_EXPIRE_MINUTES (선택, 기본값 있음)

**설정:**
```
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

**설명:** JWT 토큰 만료 시간 (분 단위)
- 10080 = 7일
- 원하는 값으로 변경 가능

**❌ 필수 아님** (코드에 기본값 있음)

---

### 5. CORS_ORIGINS (선택, 기본값 있음)

**개발 환경:**
```
CORS_ORIGINS=["*"]
```

**프로덕션 (Frontend URL 지정):**
```
CORS_ORIGINS=["https://your-frontend.railway.app"]
```

**❌ 필수 아님** (코드에 기본값 있음, 하지만 설정 권장)

---

## ❌ 추가하지 말아야 할 환경변수

### PORT (자동 제공됨)

**❌ PORT 환경변수를 수동으로 추가하지 마세요!**

**이유:**
- Railway가 자동으로 `$PORT` 환경변수를 제공합니다
- 각 배포마다 다른 포트를 할당합니다
- Start Command에서 `$PORT`를 사용하면 자동으로 연결됩니다

**올바른 Start Command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**잘못된 예시:**
```bash
# ❌ 고정 포트 사용 (절대 안 됨!)
uvicorn app.main:app --port 8080

# ❌ PORT 환경변수 수동 추가 (불필요)
PORT=8080  # 이렇게 하지 마세요!
```

---

## 📋 Railway 환경변수 설정 체크리스트

### 필수 (반드시 설정):
- [ ] **DATABASE_URL**: PostgreSQL 플러그인 추가 (자동 생성)
- [ ] **SECRET_KEY**: 랜덤 문자열 생성 후 추가

### 선택 (권장):
- [ ] **ALGORITHM**: `HS256`
- [ ] **ACCESS_TOKEN_EXPIRE_MINUTES**: `10080`
- [ ] **CORS_ORIGINS**: `["*"]` 또는 Frontend URL

### 추가하지 말 것:
- [ ] **PORT**: ❌ 추가하지 마세요 (Railway가 자동 제공)

---

## 🎯 빠른 설정 가이드

### Step 1: PostgreSQL 추가
1. 프로젝트 뷰 → "+ New" → "Database" → "Add PostgreSQL"
2. `DATABASE_URL` 자동 생성 확인

### Step 2: SECRET_KEY 생성 및 추가
```bash
# 로컬에서 실행
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

생성된 값을 복사하여:
1. Railway → Settings → Variables
2. "+ New Variable"
3. Name: `SECRET_KEY`
4. Value: 생성한 값 붙여넣기
5. Save

### Step 3: 선택적 환경변수 추가
- ALGORITHM: `HS256`
- ACCESS_TOKEN_EXPIRE_MINUTES: `10080`
- CORS_ORIGINS: `["*"]`

### Step 4: 재배포
- Deployments → Redeploy

---

## 🔒 보안 주의사항

### SECRET_KEY 보안:
- ✅ **프로덕션에서는 반드시 강력한 랜덤 값 사용**
- ✅ **절대 코드에 하드코딩하지 마세요**
- ✅ **GitHub에 커밋하지 마세요** (`.env`는 `.gitignore`에 있음)
- ❌ **"test", "secret", "123456" 같은 값 사용 금지**
- ❌ **다른 프로젝트와 동일한 SECRET_KEY 사용 금지**

### 환경변수 확인:
```bash
# Railway CLI로 확인 (로컬에서)
railway variables
```

---

## 💡 팁

### 환경변수 확인 방법:
1. Railway 대시보드 → Settings → Variables
2. 또는 Railway CLI: `railway variables`

### 환경변수 테스트:
로컬에서 테스트:
```bash
export DATABASE_URL="postgresql://..."
export SECRET_KEY="test-secret-key"
export PORT=8000
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## 📞 문제 해결

### "SECRET_KEY validation error"
→ SECRET_KEY 환경변수가 설정되지 않았거나 비어있음
→ 해결: SECRET_KEY 환경변수 추가

### "Database connection failed"
→ DATABASE_URL이 없거나 잘못됨
→ 해결: PostgreSQL 플러그인 추가 확인

### "Port already in use"
→ PORT 환경변수를 수동으로 추가했을 가능성
→ 해결: PORT 환경변수 삭제 (Railway가 자동 제공)

---

**요약:**
- ✅ **DATABASE_URL**: PostgreSQL 플러그인 추가 (자동)
- ✅ **SECRET_KEY**: 랜덤 문자열 생성 후 추가 (필수!)
- ❌ **PORT**: 추가하지 마세요 (Railway가 자동 제공)

