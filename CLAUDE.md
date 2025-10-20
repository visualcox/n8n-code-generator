# n8n JSON 코드 생성기 - 개발 가이드

## 프로젝트 개요

완벽한 n8n 워크플로우 JSON 코드를 자동으로 생성하는 AI 기반 웹 애플리케이션입니다.

## 핵심 기능

### 1. 지능형 요구사항 분석
- 사용자의 대략적인 요구사항을 LLM으로 심층 분석
- 부족한 정보는 자동으로 질문하여 수집 (추론 금지)
- 명확한 정보 기반으로만 개발 진행

### 2. 체계적인 워크플로우
1. 요구사항 입력
2. AI 기반 요구사항 분석
3. 필요시 추가 질문 생성 및 답변 수집
4. 개발요구서 자동 생성
5. 사용자 검토 및 수정
6. n8n JSON 코드 생성
7. 자동 테스트 및 최적화
8. 최종 코드 제공

### 3. 사전 학습 시스템
- **자동 학습 소스**:
  - n8n 공식 사이트 구축 사례
  - n8n 공식 매뉴얼
  - GitHub 인기 n8n 워크플로우 (10+ stars)
- **학습 주기**: 주 1회 자동 실행 (일요일 00:00)
- **학습 데이터 활용**: 코드 생성 시 참고 자료로 활용

### 4. 히스토리 관리
- 모든 생성 요청 기록 저장
- 생성된 코드 재확인 및 다운로드
- 과거 요청 데이터 학습 자료로 활용

### 5. LLM 설정
- 다중 LLM 지원:
  - OpenAI (GPT-4, GPT-3.5 등)
  - Anthropic (Claude)
  - Ollama (로컬 LLM)
  - 커스텀 API
- 각 LLM별 세부 설정 (temperature, max_tokens 등)
- 활성 LLM 전환 가능

## 기술 스택

### Backend
- **FastAPI**: Python 비동기 웹 프레임워크
- **SQLAlchemy**: ORM 및 데이터베이스 관리
- **LangChain**: LLM 통합 및 관리
- **APScheduler**: 주기적 학습 스케줄링
- **BeautifulSoup4 & Selenium**: 웹 크롤링

### Frontend
- **React 18 + TypeScript**: UI 프레임워크
- **Vite**: 빌드 도구
- **Zustand**: 상태 관리
- **Monaco Editor**: 코드 에디터
- **Tailwind CSS**: 스타일링
- **Axios**: HTTP 클라이언트

### Database
- **SQLite** (개발): 간편한 로컬 DB
- **PostgreSQL** (프로덕션): 확장 가능한 RDBMS

## 디렉토리 구조

```
webapp/
├── backend/
│   ├── app/
│   │   ├── api/              # REST API 엔드포인트
│   │   │   ├── workflow.py   # 워크플로우 생성 API
│   │   │   ├── llm_config.py # LLM 설정 API
│   │   │   └── learning.py   # 학습 시스템 API
│   │   ├── core/             # 핵심 설정
│   │   │   └── config.py     # 애플리케이션 설정
│   │   ├── models/           # 데이터베이스 모델
│   │   │   └── database.py   # SQLAlchemy 모델
│   │   ├── services/         # 비즈니스 로직
│   │   │   ├── llm_service.py      # LLM 통합 서비스
│   │   │   ├── learning_service.py # 학습 시스템 서비스
│   │   │   └── workflow_service.py # 워크플로우 서비스
│   │   ├── schemas/          # Pydantic 스키마
│   │   │   └── workflow.py   # 요청/응답 스키마
│   │   └── utils/            # 유틸리티
│   ├── main.py               # FastAPI 애플리케이션 엔트리
│   ├── requirements.txt      # Python 의존성
│   └── .env.example          # 환경변수 예시
├── frontend/
│   ├── src/
│   │   ├── components/       # React 컴포넌트
│   │   ├── pages/            # 페이지 컴포넌트
│   │   │   ├── HomePage.tsx      # 메인 생성 페이지
│   │   │   ├── HistoryPage.tsx   # 히스토리 페이지
│   │   │   ├── SettingsPage.tsx  # LLM 설정 페이지
│   │   │   └── LearningPage.tsx  # 학습 관리 페이지
│   │   ├── services/         # API 서비스
│   │   │   └── api.ts        # API 클라이언트
│   │   ├── store/            # 상태 관리
│   │   │   └── workflowStore.ts # Zustand 스토어
│   │   ├── utils/            # 유틸리티
│   │   ├── App.tsx           # 메인 App 컴포넌트
│   │   ├── main.tsx          # 엔트리 포인트
│   │   └── index.css         # 글로벌 스타일
│   ├── package.json          # NPM 의존성
│   ├── vite.config.ts        # Vite 설정
│   ├── tailwind.config.js    # Tailwind 설정
│   └── tsconfig.json         # TypeScript 설정
└── data/
    ├── templates/            # n8n 템플릿
    ├── learned_examples/     # 학습된 예제
    └── training_data/        # 학습 데이터
```

## 설치 및 실행

### Backend 설정

```bash
cd backend

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일을 편집하여 API 키 등 설정

# 서버 실행
python main.py
```

서버는 http://localhost:8000 에서 실행됩니다.

### Frontend 설정

```bash
cd frontend

# 의존성 설치
npm install

# 환경변수 설정
cp ../.env.example .env
# 필요시 .env 파일 수정

# 개발 서버 실행
npm run dev
```

프론트엔드는 http://localhost:3000 에서 실행됩니다.

## API 문서

서버 실행 후 http://localhost:8000/docs 에서 자동 생성된 API 문서를 확인할 수 있습니다.

### 주요 엔드포인트

#### 워크플로우 생성
- `POST /api/workflow/create` - 새 워크플로우 요청 생성
- `POST /api/workflow/{id}/analyze` - 요구사항 분석
- `POST /api/workflow/{id}/answers` - 질문 답변 제출
- `POST /api/workflow/{id}/generate-spec` - 개발요구서 생성
- `PUT /api/workflow/{id}/update-spec` - 개발요구서 수정
- `POST /api/workflow/{id}/generate-json` - JSON 코드 생성
- `POST /api/workflow/{id}/test-optimize` - 테스트 및 최적화
- `GET /api/workflow/{id}` - 워크플로우 조회
- `GET /api/workflow/` - 워크플로우 목록 조회

#### LLM 설정
- `POST /api/llm/config` - LLM 설정 추가
- `GET /api/llm/config` - LLM 설정 목록
- `GET /api/llm/config/{id}` - LLM 설정 조회
- `PUT /api/llm/config/{id}/activate` - LLM 활성화
- `DELETE /api/llm/config/{id}` - LLM 설정 삭제

#### 학습 시스템
- `POST /api/learning/run` - 수동 학습 시작
- `GET /api/learning/examples` - 학습된 예제 목록
- `GET /api/learning/examples/{id}` - 예제 상세 조회
- `GET /api/learning/logs` - 학습 로그 조회
- `GET /api/learning/stats` - 학습 통계 조회

## 개발 원칙

### 1. 정확성 우선
- 추론이 아닌 질문을 통한 정보 수집
- 명확한 정보만으로 코드 생성
- 불확실한 부분은 반드시 사용자에게 질문

### 2. 효율성 추구
- 비용 대비 최적의 솔루션
- 불필요한 노드나 복잡성 제거
- API 호출 최소화

### 3. 지속가능성
- 최소 비용으로 최대 효과
- 확장 가능한 아키텍처
- 유지보수 용이성

### 4. 학습 기반 개선
- 지속적인 예제 학습
- 사용자 피드백 반영
- 품질 지속 향상

## 환경변수 설명

### Backend (.env)

```bash
# 애플리케이션 설정
APP_NAME="n8n JSON Code Generator"
DEBUG=True
HOST=0.0.0.0
PORT=8000

# 데이터베이스
DATABASE_URL=sqlite+aiosqlite:///./n8n_generator.db

# LLM 설정
DEFAULT_LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
OLLAMA_BASE_URL=http://localhost:11434

# 학습 시스템
LEARNING_ENABLED=True
LEARNING_SCHEDULE_CRON=0 0 * * 0
N8N_DOCS_URL=https://docs.n8n.io
N8N_TEMPLATES_URL=https://n8n.io/workflows
GITHUB_TOKEN=your_token_here
GITHUB_MIN_STARS=10

# CORS
CORS_ORIGINS=["http://localhost:3000"]
```

### Frontend (.env)

```bash
VITE_API_URL=http://localhost:8000
```

## 프로덕션 배포

### Docker 사용 (권장)

```bash
# Dockerfile 생성 필요
docker-compose up -d
```

### 수동 배포

1. Backend:
   - PostgreSQL 설정
   - Gunicorn 또는 Uvicorn으로 실행
   - Nginx 리버스 프록시

2. Frontend:
   - `npm run build`
   - 빌드된 파일을 정적 호스팅

## 트러블슈팅

### LLM 연결 오류
- API 키 확인
- 네트워크 연결 확인
- Rate limit 확인

### 학습 실패
- GitHub 토큰 유효성 확인
- 네트워크 접근성 확인
- 로그 확인 (`/api/learning/logs`)

### 데이터베이스 오류
- DATABASE_URL 확인
- 권한 확인
- 마이그레이션 실행

## 라이선스

MIT License

## 기여 방법

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 지원

문제가 있으시면 Issue를 생성해주세요.
