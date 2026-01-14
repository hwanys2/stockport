# ⚡ Railway 빠른 수정 가이드

## 🚨 "Application failed to respond" 오류 해결

### 1분 안에 해결하기:

#### ✅ Step 1: Railway 대시보드 열기
https://railway.app → 프로젝트 선택

#### ✅ Step 2: Settings 확인
1. 서비스 클릭
2. **Settings** 탭 클릭
3. **Service Settings** 섹션 확인

#### ✅ Step 3: Root Directory 설정
**Root Directory** 필드에 입력:
```
backend
```
(슬래시 없이 `backend`만!)

#### ✅ Step 4: Start Command 확인
**Deploy** 섹션에서 **Start Command** 확인:
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### ✅ Step 5: 환경변수 추가
**Variables** 탭에서 추가:

```bash
SECRET_KEY=<여기에-랜덤-문자열-입력>
```

**SECRET_KEY 생성:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

또는 온라인: https://randomkeygen.com/

#### ✅ Step 6: PostgreSQL 추가 (없는 경우)
프로젝트 뷰에서:
- **"+ New"** 클릭
- **"Database"** 선택
- **"Add PostgreSQL"** 클릭

#### ✅ Step 7: 재배포
**Deployments** 탭 → **Redeploy** 버튼 클릭

---

## ✅ 성공 확인

브라우저에서:
```
https://stockport-production.up.railway.app/health
```

**응답 확인:**
```json
{"status":"healthy"}
```

---

## 🔍 여전히 안 되면?

### 배포 로그 확인:
1. **Deployments** 탭
2. 최신 배포 클릭
3. **View Logs** 클릭
4. 오류 메시지 확인

### 자주 보는 오류:

**"No module named 'app'"**
→ Root Directory를 `backend`로 설정

**"Port already in use"**
→ Start Command에서 `$PORT` 사용 확인

**"Database connection failed"**
→ PostgreSQL 플러그인 추가

---

**상세 가이드**: [RAILWAY_TROUBLESHOOTING.md](RAILWAY_TROUBLESHOOTING.md)

