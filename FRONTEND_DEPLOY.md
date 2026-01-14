# 🎨 Frontend 배포 가이드

## 현재 상황
✅ Backend API 배포 완료
❌ Frontend 웹 페이지 미배포

**결과:** JSON 응답만 보이고 웹 페이지가 안 보임

---

## ✅ Frontend 배포 방법 (5분)

### Step 1: Frontend 서비스 추가

**Railway 프로젝트 뷰에서:**
1. **"+ New"** 버튼 클릭
2. **"GitHub Repo"** 선택
3. 같은 저장소 (`stockport`) 선택
4. **"Add Service"** 클릭

---

### Step 2: Root Directory 설정 (필수!)

**새로 생성된 Frontend 서비스에서:**
1. 서비스 클릭
2. **Settings** 탭
3. **Service Settings** 섹션
4. **Root Directory** 찾기

**입력:**
```
frontend
```

⚠️ **정확히 `frontend`만 입력** (슬래시 없이!)

**Save 클릭**

---

### Step 3: 환경변수 설정 (필수!)

**Settings → Variables** 탭에서:

**Backend URL 확인:**
1. Backend 서비스로 이동
2. **Settings** → **Networking** 탭
3. **Public Networking** 섹션에서 도메인 확인
   - 예: `stockport-production.up.railway.app`

**Frontend 서비스로 돌아가서:**
1. **Settings** → **Variables** 탭
2. **"+ New Variable"** 클릭
3. Name: `VITE_API_URL`
4. Value: `https://stockport-production.up.railway.app`
   - ⚠️ **https://** 포함!
   - ⚠️ **Backend URL** 입력!

**Save 클릭**

---

### Step 4: Build & Deploy 설정 확인

**Settings → Deploy** 섹션에서:

**Build Command:**
```
npm install && npm run build
```

**Start Command:**
```
npm run preview -- --host 0.0.0.0 --port $PORT
```

**Save 클릭**

---

### Step 5: 배포 및 확인

1. **Deployments** 탭으로 이동
2. **Deploy** 버튼 클릭 (또는 자동 배포 대기)
3. **View Logs** 클릭하여 빌드 확인

**확인할 로그:**
```
✓ Installing dependencies
✓ Building for production
✓ Build complete
✓ Starting preview server
```

---

### Step 6: Frontend URL 확인

배포 완료 후:
1. **Settings** → **Networking** 탭
2. **Public Networking** 섹션에서 Frontend 도메인 확인
   - 예: `stockport-frontend-production.up.railway.app`

**브라우저에서 접속:**
```
https://stockport-frontend-production.up.railway.app
```

✅ **이제 웹 페이지가 보입니다!**

---

## 🔧 Backend CORS 설정 업데이트

Frontend URL을 Backend의 CORS에 추가해야 합니다:

**Backend 서비스에서:**
1. **Settings** → **Variables** 탭
2. `CORS_ORIGINS` 환경변수 찾기
3. 값 수정:

**기존:**
```json
["*"]
```

**수정:**
```json
["https://stockport-frontend-production.up.railway.app"]
```

또는 여러 URL:
```json
["https://stockport-frontend-production.up.railway.app", "http://localhost:5173"]
```

**Save 클릭**

**Backend 재배포:**
- Deployments → Redeploy

---

## 📋 Frontend 배포 체크리스트

### Railway Settings:
- [ ] **Root Directory**: `frontend` 설정됨
- [ ] **Build Command**: `npm install && npm run build`
- [ ] **Start Command**: `npm run preview -- --host 0.0.0.0 --port $PORT`

### 환경변수:
- [ ] **VITE_API_URL**: `https://your-backend-url.railway.app` 설정됨
  - ⚠️ **https://** 포함!
  - ⚠️ **Backend URL** 입력!

### Backend CORS:
- [ ] **CORS_ORIGINS**: Frontend URL 포함됨
- [ ] Backend 재배포 완료

### 배포:
- [ ] Frontend 빌드 성공
- [ ] Frontend URL 접속 가능
- [ ] 웹 페이지 표시됨

---

## 🧪 테스트

### 1. Frontend 접속
브라우저에서:
```
https://your-frontend-url.railway.app
```

**예상:** 로그인 페이지가 보임

### 2. API 연결 테스트
1. 회원가입 시도
2. 로그인 시도
3. 오류가 없으면 성공!

---

## 🆘 문제 해결

### "Network Error" 또는 "CORS Error"
→ Backend의 `CORS_ORIGINS`에 Frontend URL 추가 확인

### "Cannot GET /"
→ Start Command 확인: `npm run preview` 사용

### 빌드 실패
→ Root Directory가 `frontend`로 설정되었는지 확인

### API 연결 실패
→ `VITE_API_URL` 환경변수가 올바른 Backend URL인지 확인

---

## 💡 팁

### 두 서비스 URL 확인:
- **Backend**: API 엔드포인트 (예: `/health`, `/docs`)
- **Frontend**: 웹 페이지 (React 앱)

### 환경변수 확인:
```bash
# Railway CLI로 확인
railway variables --service frontend
```

---

## 🎯 요약

1. ✅ Frontend 서비스 추가
2. ✅ Root Directory: `frontend` 설정
3. ✅ `VITE_API_URL` 환경변수 설정 (Backend URL)
4. ✅ 배포
5. ✅ Backend CORS 업데이트
6. ✅ 웹 페이지 접속!

---

**이제 완전한 웹 애플리케이션이 배포됩니다!** 🎉

