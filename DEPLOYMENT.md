# 🚀 Vercel + Railway 배포 가이드

## 📋 준비물

1. **GitHub 계정** (이미 있음 ✅)
2. **Vercel 계정** (무료) - https://vercel.com
3. **Railway 계정** (무료) - https://railway.app

---

## 🎯 Part 1: Backend를 Railway에 배포

### 1️⃣ Railway 가입 및 프로젝트 생성

1. https://railway.app 접속
2. **"Start a New Project"** 클릭
3. **"Deploy from GitHub repo"** 선택
4. GitHub 계정 연동
5. `visualcox/n8n-code-generator` 저장소 선택
6. **Root Directory**: `backend` 입력
7. **Deploy** 클릭!

### 2️⃣ 환경 변수 설정

Railway 대시보드에서:

1. 프로젝트 클릭 → **"Variables"** 탭
2. 다음 환경 변수들 추가:

```bash
# LLM 설정 (사용할 것만 추가)
DEFAULT_LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here

# 또는 OpenAI 사용시
# DEFAULT_LLM_PROVIDER=openai
# OPENAI_API_KEY=sk-proj-...

# 또는 Anthropic 사용시
# DEFAULT_LLM_PROVIDER=anthropic
# ANTHROPIC_API_KEY=sk-ant-...

# Database (Railway가 자동으로 SQLite 지원)
DATABASE_URL=sqlite:///./data/n8n_workflows.db

# CORS (나중에 Frontend URL로 변경)
FRONTEND_URL=*

# Port (Railway가 자동 설정)
PORT=8000
```

3. **"Deploy"** 버튼 클릭

### 3️⃣ Backend URL 확인

1. 배포 완료 후 **"Settings"** → **"Domains"**
2. Railway가 제공하는 URL 복사 (예: `https://n8n-backend-production.up.railway.app`)
3. 이 URL을 메모장에 저장! 📝

---

## 🎨 Part 2: Frontend를 Vercel에 배포

### 1️⃣ Vercel 가입 및 프로젝트 생성

1. https://vercel.com 접속
2. **"Add New Project"** 클릭
3. GitHub 계정 연동
4. `visualcox/n8n-code-generator` 저장소 선택
5. **Root Directory**: `frontend` 입력

### 2️⃣ 빌드 설정

**Framework Preset**: Vite
**Build Command**: `npm run build`
**Output Directory**: `dist`
**Install Command**: `npm install`

### 3️⃣ 환경 변수 설정

**Environment Variables** 섹션에 추가:

```bash
VITE_API_URL=https://your-railway-backend-url.up.railway.app
```

(위에서 복사한 Railway Backend URL을 입력!)

### 4️⃣ 배포

**"Deploy"** 클릭!

### 5️⃣ Frontend URL 확인

배포 완료 후:
- Vercel이 제공하는 URL 확인 (예: `https://n8n-code-generator.vercel.app`)
- 이 주소로 접속하면 앱이 작동! 🎉

---

## 🔧 Part 3: Backend CORS 업데이트

Frontend URL을 받았으면 Railway로 돌아가서:

1. Railway 프로젝트 → **"Variables"** 탭
2. `FRONTEND_URL` 변수를 Vercel URL로 변경:
   ```
   FRONTEND_URL=https://n8n-code-generator.vercel.app
   ```
3. 자동으로 재배포됨!

---

## ✅ 배포 완료 확인

1. **Frontend URL**로 접속
2. 설정 페이지에서 LLM 설정
3. 워크플로우 생성 테스트!

---

## 🔄 업데이트 방법

### 자동 배포 (추천!)

로컬에서 코드 수정 후:

```bash
git add .
git commit -m "업데이트 내용"
git push origin main
```

→ Vercel과 Railway가 자동으로 배포! 🚀

---

## 💰 비용

- **Vercel**: 무료 (취미 프로젝트)
- **Railway**: 무료 $5 크레딧/월 (충분함)

---

## 🐛 문제 해결

### Backend 연결 안 됨
1. Railway 로그 확인: `railway logs`
2. 환경 변수 확인
3. Database 경로 확인

### Frontend 빌드 실패
1. Vercel 빌드 로그 확인
2. `VITE_API_URL` 환경 변수 확인
3. package.json의 dependencies 확인

### CORS 오류
1. Railway의 `FRONTEND_URL` 환경 변수 확인
2. Backend의 `main.py` CORS 설정 확인

---

## 📞 도움이 필요하면

각 단계를 진행하면서 문제가 생기면 스크린샷과 함께 알려주세요!

---

**다음 단계**: Railway 계정부터 만들어보세요! 🚀
