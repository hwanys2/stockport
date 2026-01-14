# 🚨 Railway 빌드 실패 해결 방법

## 문제: "railpack process exited with an error"

이 오류는 Railway가 프로젝트 루트에서 `package.json` 또는 `requirements.txt`를 찾지 못해서 발생합니다.

**원인**: 이 프로젝트는 monorepo 구조 (backend + frontend 분리)입니다.

---

## ✅ 해결 방법 (2분 소요)

### Backend 서비스 설정

1. **Railway 대시보드**로 이동
2. 현재 서비스 클릭
3. **Settings** 탭 클릭
4. **Service Settings** 섹션에서:
   
   **Root Directory** 찾기 → 다음 입력:
   ```
   backend
   ```
   ⚠️ 중요: 슬래시 없이 `backend`만 입력하세요!

5. **Variables** 탭에서 환경변수 설정:
   ```bash
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   SECRET_KEY=<랜덤-문자열-생성>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=10080
   CORS_ORIGINS=["*"]
   ```

6. **Deployments** 탭 → **Redeploy** 버튼 클릭

7. ✅ 빌드 성공! Backend URL 복사

---

### Frontend 서비스 추가

1. 같은 프로젝트에서 **"+ New"** 클릭
2. **"GitHub Repo"** 선택
3. 같은 저장소 (`stockport`) 선택
4. **Settings** 탭에서:
   
   **Root Directory** 설정:
   ```
   frontend
   ```

5. **Variables** 탭에서:
   ```bash
   VITE_API_URL=<위에서-복사한-Backend-URL>
   ```

6. **Deploy** 버튼 클릭

7. ✅ Frontend 배포 완료!

8. Backend Settings로 돌아가서 `CORS_ORIGINS` 업데이트:
   ```bash
   CORS_ORIGINS=["<Frontend-URL>"]
   ```

---

## 📸 스크린샷 가이드

### Root Directory 설정 위치:
```
Railway Dashboard
  → Your Service
    → Settings (탭)
      → Service Settings (섹션)
        → Root Directory (필드)
          → 입력: backend 또는 frontend
```

---

## 🔍 확인 사항

### Backend 확인:
```bash
curl https://your-backend.railway.app/health

# 응답 예상:
{"status":"healthy"}
```

### Frontend 확인:
브라우저에서 Frontend URL 접속 → 로그인 페이지 표시

---

## 💡 자주 하는 실수

❌ **잘못된 Root Directory 설정:**
- `/backend` ← 슬래시 있으면 안 됨
- `./backend` ← 상대경로 불필요
- `backend/` ← 끝에 슬래시 불필요

✅ **올바른 Root Directory 설정:**
- `backend` ← 정확히 이것만
- `frontend` ← 정확히 이것만

---

## 🎯 빠른 체크리스트

Backend 서비스:
- [ ] Root Directory: `backend` 설정
- [ ] PostgreSQL 추가
- [ ] 환경변수 설정
- [ ] Redeploy 클릭
- [ ] `/health` 엔드포인트 테스트

Frontend 서비스:
- [ ] Root Directory: `frontend` 설정
- [ ] `VITE_API_URL` 환경변수 설정
- [ ] Deploy 클릭
- [ ] 웹사이트 접속 테스트

Backend CORS 업데이트:
- [ ] `CORS_ORIGINS`에 Frontend URL 추가
- [ ] Redeploy

---

## 🆘 여전히 안 되나요?

### Backend 로그 확인:
```
Railway Dashboard → Backend Service → Deployments → 최신 배포 클릭 → View Logs
```

### 흔한 오류:

**"No module named 'app'"**
→ Root Directory가 `backend`로 설정되었는지 확인

**"Cannot find module"** (Frontend)
→ Root Directory가 `frontend`로 설정되었는지 확인

**"Database connection failed"**
→ PostgreSQL 플러그인 추가했는지 확인
→ `DATABASE_URL` 환경변수 확인

**"CORS error"**
→ Backend의 `CORS_ORIGINS`에 Frontend URL 추가

---

## 📚 관련 문서

- 전체 배포 가이드: [DEPLOYMENT.md](DEPLOYMENT.md)
- 프로젝트 문서: [README.md](README.md)
- 빠른 시작: [QUICKSTART.md](QUICKSTART.md)

---

**이 가이드로 해결되었나요? 🎉**

문제가 계속되면 Railway 로그를 확인하거나 GitHub Issues에 문의하세요.

