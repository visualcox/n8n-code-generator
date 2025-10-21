# 🍎 M4 Mac 사용자 빠른 시작 가이드

## ⚡ 3분 안에 시작하기

### 준비물
- ✅ M4 Mac (Python 기본 내장!)
- 📦 Node.js (설치 필요)
- 🔑 OpenAI API 키

---

## 🚀 설치 및 실행 (초간단)

### 1단계: Node.js 설치 (3분)

```bash
# 1. Node.js 다운로드
open https://nodejs.org/

# 2. LTS 버전 다운로드 → .pkg 파일 실행 → 계속 클릭

# 3. 설치 확인
node --version
npm --version
```

✅ 버전 정보가 나오면 성공!

---

### 2단계: OpenAI API 키 받기 (5분)

1. https://platform.openai.com/ 가입
2. https://platform.openai.com/api-keys 접속
3. "Create new secret key" 클릭
4. 키 복사 → 메모장에 저장

---

### 3단계: 자동 설치 (10분)

터미널 열기: `⌘ + 스페이스바` → `terminal` 입력

```bash
# 1. 앱 폴더로 이동
cd ~/webapp
# (또는 실제 경로: cd /Users/사용자이름/webapp)

# 2. 자동 설치 실행
chmod +x install.sh
./install.sh
```

**설치가 끝나면:**
```bash
# 3. API 키 설정
cd backend
nano .env

# OPENAI_API_KEY=여기에_실제_API_키_입력
# Ctrl+X → Y → Enter로 저장
```

---

### 4단계: 앱 실행! 🎉

**터미널 탭 1:**
```bash
cd ~/webapp
./start_backend.sh
```

**새 터미널 탭 (`⌘ + T`):**
```bash
cd ~/webapp
./start_frontend.sh
```

**브라우저에서:**
```
http://localhost:3000
```

---

## 💡 처음 사용하기

### 1. LLM 설정 (한 번만)
- "설정" 메뉴 클릭
- "새 LLM 설정 추가"
- OpenAI / gpt-4-turbo-preview 선택
- API 키 입력
- "기본 설정으로 사용" ✅

### 2. 워크플로우 생성
- "홈" 메뉴 클릭
- 원하는 자동화 입력:

```
매일 아침 9시에 Gmail에서 미읽은 메일을 확인하고,
중요한 메일이 있으면 Slack으로 알림을 보내주세요.
```

- "분석 시작" 클릭
- AI 질문에 답변
- 완성! 🎊

---

## 🔧 유용한 Mac 단축키

| 단축키 | 기능 |
|--------|------|
| `⌘ + 스페이스바` | Spotlight 검색 (터미널 열기) |
| `⌘ + T` | 새 터미널 탭 |
| `⌘ + W` | 탭 닫기 |
| `⌃ + C` | 프로그램 종료 |
| `⌘ + C` / `⌘ + V` | 복사/붙여넣기 |

---

## ❓ 문제 해결

### Python이 없다고 나옴?
```bash
# Homebrew 설치
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 설치
brew install python@3.11
```

### Permission denied?
```bash
chmod +x install.sh start_backend.sh start_frontend.sh
```

### M4 호환성 문제?
```bash
softwareupdate --install-rosetta
```

---

## 🎯 예제 프롬프트

### 간단한 예제
```
Google Sheets에 새로운 행이 추가되면 
Slack으로 알림을 보내주세요.
```

### 실용적인 예제
```
매일 저녁 6시에 Trello "진행중" 리스트의 
마감일이 내일인 카드를 찾아서 
Discord로 알림을 보내주세요.
```

### 복잡한 예제
```
RSS 피드를 15분마다 확인하고
"AI" 키워드가 포함된 글의 요약을 
OpenAI로 생성해서 Notion에 저장하고
중요한 글은 Telegram으로도 알림해주세요.
```

---

## 📚 더 자세한 가이드

- **비개발자를_위한_실행_가이드.md**: 상세 설명
- **시작하기.md**: 초간단 가이드
- **QUICKSTART.md**: 빠른 시작

---

## 🎉 다음에 다시 실행하기

```bash
# 탭 1
cd ~/webapp && ./start_backend.sh

# 탭 2 (⌘ + T로 새 탭)
cd ~/webapp && ./start_frontend.sh

# 브라우저
http://localhost:3000
```

---

**완료! M4 Mac에서 AI 자동화 코드 생성기를 사용하세요! 🚀**
