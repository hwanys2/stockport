# 🔧 Railway "pip: command not found" 해결 가이드

## 문제
```
/bin/bash: line 1: pip: command not found
Build Failed: build daemon returned an error
```

## 원인
Railway가 Python 환경을 제대로 감지하지 못했습니다.

---

## ✅ 해결 방법

### 방법 1: Railway Settings에서 Python 버전 설정 (권장)

1. **Railway 대시보드** → 서비스 클릭
2. **Settings** 탭
3. **Build & Deploy** 섹션에서:
   - **Python Version**: `3.11` 선택 (또는 입력)
   - **Root Directory**: `backend` 확인
4. **Save** 클릭
5. **Redeploy** 클릭

---

### 방법 2: Root Directory 확인 (가장 중요!)

**Railway Settings에서:**
```
Root Directory: backend
```

⚠️ **이게 설정되지 않으면 Railway가 requirements.txt를 찾지 못합니다!**

---

### 방법 3: Build Command 명시 (선택)

**Settings → Build & Deploy**에서:

**Build Command** (선택사항):
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

또는 비워두기 (Railway가 자동 감지)

---

## 📋 확인 체크리스트

배포 전 확인:

- [ ] **Root Directory**: `backend` 설정됨
- [ ] **Python Version**: `3.11` 설정됨 (또는 자동 감지)
- [ ] `backend/requirements.txt` 파일 존재 확인
- [ ] `backend/runtime.txt` 파일 존재 확인 (선택)
- [ ] `backend/nixpacks.toml` 파일 존재 확인 (선택)

---

## 🔍 배포 로그 확인

**정상 빌드 로그 예시:**
```
✓ Detecting Python project
✓ Installing Python 3.11
✓ Installing dependencies
  Running: pip install -r requirements.txt
✓ Build complete
```

**오류 로그 예시:**
```
✗ pip: command not found
→ Root Directory 확인 필요
```

---

## 🚀 빠른 수정 (1분)

1. Railway 대시보드 → Settings
2. **Root Directory**: `backend` 입력
3. **Python Version**: `3.11` 선택
4. **Save** → **Redeploy**

---

## 💡 추가 팁

### 로컬에서 테스트
```bash
cd backend
python3 --version  # Python 3.11 확인
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Railway CLI로 확인
```bash
railway logs
```

---

## 🆘 여전히 안 되나요?

### 1. 배포 로그 전체 확인
Railway → Deployments → 최신 배포 → View Logs

### 2. 파일 구조 확인
```
backend/
  ├── requirements.txt  ← 이 파일이 있어야 함!
  ├── runtime.txt       ← 선택사항
  ├── nixpacks.toml     ← 선택사항
  └── app/
      └── main.py
```

### 3. Railway 지원팀 문의
- Railway Discord: https://discord.gg/railway
- Railway 문서: https://docs.railway.app

---

**가장 중요한 것: Root Directory를 `backend`로 설정하세요!** 🎯

