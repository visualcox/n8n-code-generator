# 빠른 시작 가이드

## 사전 준비

### 필수 소프트웨어
- Python 3.9 이상
- Node.js 18 이상
- npm 또는 yarn

### API 키 준비
다음 중 하나의 LLM API 키가 필요합니다:
- **OpenAI API Key** (추천): https://platform.openai.com/api-keys
- **Anthropic API Key**: https://console.anthropic.com/
- **Ollama** (로컬 실행): https://ollama.ai/

## 5분 설치

### 1단계: Backend 설정

```bash
# Backend 디렉토리로 이동
cd backend

# Python 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env

# .env 파일 수정 (필수!)
nano .env  # 또는 원하는 에디터 사용
```

**`.env` 파일에서 최소한 다음을 설정하세요:**
```bash
# OpenAI 사용시
OPENAI_API_KEY=sk-your-actual-api-key-here

# Anthropic 사용시
ANTHROPIC_API_KEY=sk-ant-your-actual-api-key-here

# Ollama 로컬 사용시 (API 키 불필요)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

### 2단계: Backend 실행

```bash
# backend 디렉토리에서
python main.py
```

✅ 서버가 http://localhost:8000 에서 실행됩니다!

### 3단계: Frontend 설정 (새 터미널)

```bash
# Frontend 디렉토리로 이동
cd frontend

# 의존성 설치
npm install

# 환경변수 설정 (선택사항)
cp ../.env.example .env
```

### 4단계: Frontend 실행

```bash
# frontend 디렉토리에서
npm run dev
```

✅ 앱이 http://localhost:3000 에서 실행됩니다!

## 첫 번째 워크플로우 생성

### 1. LLM 설정하기

1. 브라우저에서 http://localhost:3000 접속
2. 왼쪽 메뉴에서 **"설정"** 클릭
3. **"새 LLM 설정 추가"** 클릭
4. 정보 입력:
   - **설정 이름**: "My OpenAI GPT-4" (원하는 이름)
   - **제공자**: OpenAI 선택
   - **모델 이름**: gpt-4-turbo-preview
   - **API Key**: 준비한 OpenAI API 키 입력
   - **기본 설정으로 사용**: ✅ 체크
5. **"추가"** 버튼 클릭

### 2. 워크플로우 생성하기

1. 왼쪽 메뉴에서 **"홈"** 클릭
2. 요구사항 입력창에 다음과 같이 입력:

```
매일 아침 9시에 Gmail에서 미읽은 중요 메일을 확인하고, 
중요한 메일이 있으면 Slack의 #notifications 채널로 
메일 제목과 발신자를 알림으로 보내주세요.
```

3. **"분석 시작"** 버튼 클릭

4. AI가 추가 질문을 하면 답변:
   - Gmail 계정 정보는?
   - Slack Webhook URL은?
   - "중요한 메일"의 기준은?
   등등...

5. 모든 질문에 답변하면 **개발요구서**가 생성됩니다
   - 검토 후 수정하거나 그대로 진행

6. **"승인 및 JSON 생성"** 클릭

7. 잠시 기다리면 완성된 n8n JSON 코드가 생성됩니다! 🎉

8. **"복사"** 버튼으로 코드 복사

9. n8n에서 **Import from JSON**으로 붙여넣기

## 주요 기능 사용법

### 📚 학습 시스템

1. 왼쪽 메뉴에서 **"학습 관리"** 클릭
2. **"수동 학습 시작"** 클릭
3. AI가 자동으로:
   - n8n 공식 문서에서 예제 수집
   - GitHub에서 인기 워크플로우 수집
   - n8n 템플릿 수집

이 학습 데이터는 앞으로 워크플로우 생성 시 참고 자료로 활용됩니다!

### 📝 히스토리

1. 왼쪽 메뉴에서 **"히스토리"** 클릭
2. 이전에 생성한 모든 워크플로우 확인
3. 클릭하여 상세 내용 보기
4. **"다운로드"** 버튼으로 JSON 파일 저장

### ⚙️ 여러 LLM 사용

1. **"설정"** 메뉴에서 여러 LLM 추가 가능:
   - OpenAI GPT-4 (고품질, 비용 높음)
   - OpenAI GPT-3.5 (빠름, 저렴)
   - Anthropic Claude (균형잡힌 성능)
   - Ollama Llama2 (무료, 로컬 실행)

2. 원하는 LLM의 ✅ 버튼 클릭하여 활성화

3. 활성화된 LLM이 워크플로우 생성에 사용됩니다

## 예시 요구사항

### 간단한 예제
```
Google Sheets의 특정 시트에 새로운 행이 추가되면 
그 내용을 Slack으로 알림을 보내주세요.
```

### 중간 난이도 예제
```
매일 저녁 6시에 Trello의 "진행중" 리스트에 있는 
모든 카드를 확인하고, 마감일이 내일인 카드가 있으면
Discord의 #deadlines 채널로 알림을 보내주세요.
카드 제목, 담당자, 마감일 정보를 포함해주세요.
```

### 복잡한 예제
```
1. RSS 피드를 15분마다 확인
2. 특정 키워드("AI", "머신러닝", "딥러닝")가 포함된 글만 필터링
3. OpenAI API로 각 글의 요약 생성 (100자 이내)
4. Notion 데이터베이스에 저장 (제목, 요약, 링크, 날짜)
5. 중요도가 높은 글(키워드 2개 이상 포함)은 Telegram으로도 알림
```

## 문제 해결

### Backend가 실행되지 않을 때

```bash
# 의존성 재설치
cd backend
pip install --upgrade -r requirements.txt

# 데이터베이스 초기화
rm n8n_generator.db  # 기존 DB 삭제
python main.py  # 새로 생성됨
```

### Frontend가 실행되지 않을 때

```bash
# 의존성 재설치
cd frontend
rm -rf node_modules package-lock.json
npm install

# 캐시 클리어 후 재실행
npm run dev
```

### LLM 연결 오류

1. API 키가 정확한지 확인
2. .env 파일이 올바른 위치에 있는지 확인
3. Backend 재시작
4. "설정" 메뉴에서 새로 설정 추가

### 학습이 실패할 때

1. 인터넷 연결 확인
2. GitHub Token이 유효한지 확인 (선택사항)
3. "학습 관리" → "학습 로그"에서 오류 확인

## 팁과 요령

### 💡 좋은 요구사항 작성법

**좋은 예시:**
```
매일 오전 10시에 GitHub API로 특정 리포지토리의 
새로운 이슈를 가져와서, 라벨이 "bug"인 이슈만 
Slack #dev-team 채널로 알림을 보내주세요.
이슈 번호, 제목, 작성자를 포함해주세요.
```

**나쁜 예시:**
```
GitHub 이슈 관리
```

### 💡 AI 질문에 명확하게 답변하기

AI가 "중요한 메일의 기준은?"이라고 물으면:

**좋은 답변:**
```
발신자가 boss@company.com이거나 
제목에 [긴급] 또는 [중요]가 포함된 메일입니다.
```

**나쁜 답변:**
```
중요한 거요
```

### 💡 개발요구서 검토하기

- AI가 생성한 개발요구서를 꼭 읽어보세요
- 잘못 이해한 부분이 있으면 수정하세요
- 더 나은 방법이 있으면 제안하세요

## 다음 단계

1. ✅ 첫 워크플로우 생성해보기
2. 📚 여러 예제로 시스템 학습시키기
3. 🔧 실제 업무에 필요한 워크플로우 만들기
4. 📝 히스토리에서 패턴 찾기
5. 🚀 팀과 공유하기

## 지원

문제가 있으시면:
1. CLAUDE.md 문서 참고
2. GitHub Issues 생성
3. API 문서 확인: http://localhost:8000/docs

---

**즐거운 n8n 워크플로우 생성 되세요! 🎉**
