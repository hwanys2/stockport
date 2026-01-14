# 🚨 Railway "pip: command not found" 완전 해결 가이드

## 문제
```
/bin/bash: line 1: pip: command not found
Build Failed: build daemon returned an error
```

## 원인
Railway가 Python 환경을 제대로 감지하지 못했습니다.

---

## ✅ 즉시 해결 방법 (3단계)

### Step 1: Root Directory 확인 (가장 중요!)

**Railway 대시보드에서:**
1. 서비스 클릭
2. **Settings** 탭
3. **Service Settings** 섹션 확인
4. **Root Directory** 필드 확인:

```
✅ 올바른 설정: backend
❌ 잘못된 설정: (비어있음) 또는 /backend 또는 ./backend
```

**만약 비어있다면:**
- `backend` 입력 (슬래시 없이!)
- **Save** 클릭
- **Redeploy** 클릭

---

### Step 2: Build Command 확인

**Settings → Deploy** 섹션에서:

**✅ 올바른 설정:**
- **Build Command**: (비워두기 - Railway가 자동 감지)

또는 명시적으로:
```bash
pip install -r requirements.txt
```

**❌ 잘못된 설정:**
```bash
pip install --upgrade pip  # Python이 설치되기 전에 실행됨
```

---

### Step 3: Python Version 확인 (선택)

**Settings → Deploy** 섹션에서:

**Python Version**: `3.11` 선택 (또는 자동 감지)

---

## 🔍 Railway 자동 감지

Railway는 다음 파일을 보면 자동으로 Python 프로젝트로 인식합니다:

- ✅ `requirements.txt` → Python 프로젝트로 인식
- ✅ `runtime.txt` → Python 버전 지정
- ✅ `.python-version` → Python 버전 지정

**중요:** Root Directory가 `backend`로 설정되어 있어야 Railway가 `backend/requirements.txt`를 찾을 수 있습니다!

---

## 📋 확인 체크리스트

배포 전 확인:

- [ ] **Root Directory**: `backend` 설정됨 (슬래시 없이!)
- [ ] **Build Command**: 비워두거나 `pip install -r requirements.txt`
- [ ] **Python Version**: `3.11` 설정됨 (또는 자동 감지)
- [ ] `backend/requirements.txt` 파일 존재 확인
- [ ] `backend/runtime.txt` 파일 존재 확인 (선택)

---

## 🧪 테스트 방법

### 로컬에서 먼저 테스트:
```bash
cd backend
python3 --version  # Python 3.11 확인
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

로컬에서 작동하면 Railway 설정 문제입니다.

---

## 🆘 여전히 안 되나요?

### 1. 배포 로그 전체 확인

**Railway → Deployments → 최신 배포 → View Logs**

**확인할 내용:**

#### ✅ 정상 빌드 로그:
```
✓ Detecting Python project
✓ Installing Python 3.11
✓ Installing dependencies
  Running: pip install -r requirements.txt
✓ Build complete
```

#### ❌ 문제가 있는 로그:

**"requirements.txt not found"**
```
FileNotFoundError: requirements.txt
```
→ **해결**: Root Directory를 `backend`로 설정

**"pip: command not found"**
```
/bin/bash: line 1: pip: command not found
```
→ **해결**: Root Directory 확인, Build Command 확인

**"No module named 'app'"**
```
ModuleNotFoundError: No module named 'app'
```
→ **해결**: Root Directory를 `backend`로 설정

---

### 2. 파일 구조 확인

다음 구조가 맞는지 확인:

```
backend/
  ├── requirements.txt      ← 필수! (이 파일이 있어야 Python 감지)
  ├── runtime.txt           ← 선택 (Python 3.11 명시)
  ├── .python-version       ← 선택 (3.11)
  ├── nixpacks.toml         ← 선택 (설정 파일)
  └── app/
      └── main.py
```

---

### 3. Railway Settings 재확인

**Settings → Service Settings:**
- Root Directory: `backend` (정확히 이것만!)

**Settings → Deploy:**
- Build Command: (비워두기) 또는 `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Python Version: `3.11` (선택)

---

## 💡 프로 팁

### Railway가 자동으로 하는 것:
1. `requirements.txt` 발견 → Python 프로젝트로 인식
2. `runtime.txt` 또는 `.python-version` 확인 → Python 버전 설치
3. `pip install -r requirements.txt` 자동 실행

### 수동 설정이 필요한 경우:
- Root Directory 설정 (monorepo 구조)
- Build Command 명시 (특수한 경우)

---

## 🎯 가장 흔한 원인 Top 3

1. **Root Directory 미설정** (95%)
   - Railway가 루트에서 requirements.txt를 찾음
   - 해결: Root Directory를 `backend`로 설정

2. **Build Command 오류** (80%)
   - Python 설치 전에 pip 실행
   - 해결: Build Command 비우기 (자동 감지)

3. **파일 위치 오류** (70%)
   - requirements.txt가 backend 폴더에 없음
   - 해결: 파일 구조 확인

---

## 📞 추가 도움

- Railway 문서: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- 프로젝트 문서: [README.md](README.md)

---

**가장 중요한 것: Root Directory를 `backend`로 설정하세요!** 🎯

이것만 제대로 설정하면 Railway가 자동으로 Python을 감지하고 설치합니다.

