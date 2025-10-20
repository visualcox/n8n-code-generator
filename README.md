# n8n JSON 코드 생성기

완벽한 n8n 워크플로우 JSON 코드를 자동으로 생성하는 AI 기반 웹 애플리케이션

## 주요 기능

### 1. 지능형 요구사항 분석
- 사용자의 대략적인 요구사항을 심층 분석
- 부족한 정보는 자동으로 질문하여 수집
- 추론이 아닌 명확한 정보 기반 개발

### 2. 체계적인 개발 프로세스
1. 요구사항 입력
2. AI 기반 요구사항 분석 및 추가 질문
3. 개발요구서 자동 생성
4. 사용자 검토 및 수정
5. n8n JSON 코드 생성
6. 자동 테스트 및 최적화
7. 최종 코드 제공

### 3. 사전 학습 시스템
- n8n 공식 사이트의 구축 사례 학습
- n8n 공식 매뉴얼 지속 학습
- GitHub 인기 n8n 코드 학습
- 주 1회 자동 업데이트

### 4. 히스토리 관리
- 이전 요청 내역 조회
- 생성된 코드 재사용
- 학습 데이터로 활용

### 5. LLM 설정
- 로컬 LLM 연동 (Ollama 등)
- API 기반 LLM 연동 (OpenAI, Anthropic 등)
- 커스텀 설정 지원

## 기술 스택

### Backend
- **Framework**: FastAPI
- **Database**: SQLite / PostgreSQL
- **LLM Integration**: LangChain
- **Crawler**: BeautifulSoup4, Selenium
- **Scheduler**: APScheduler

### Frontend
- **Framework**: React 18 + TypeScript
- **State Management**: Zustand
- **UI Components**: Tailwind CSS + shadcn/ui
- **Code Editor**: Monaco Editor
- **HTTP Client**: Axios

## 프로젝트 구조

```
webapp/
├── backend/
│   ├── app/
│   │   ├── api/          # API 엔드포인트
│   │   ├── core/         # 핵심 로직
│   │   ├── models/       # 데이터 모델
│   │   ├── services/     # 비즈니스 로직
│   │   └── utils/        # 유틸리티
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/   # React 컴포넌트
│   │   ├── pages/        # 페이지
│   │   ├── services/     # API 서비스
│   │   ├── store/        # 상태 관리
│   │   └── utils/        # 유틸리티
│   ├── package.json
│   └── vite.config.ts
└── data/
    ├── templates/        # n8n 템플릿
    ├── learned_examples/ # 학습된 예제
    └── training_data/    # 학습 데이터

```

## 설치 및 실행

### Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 개발 원칙

1. **정확성**: 추론보다 질문, 명확한 정보 기반 개발
2. **효율성**: 비용 대비 최적의 솔루션
3. **지속가능성**: 최소 비용으로 최대 효과
4. **학습성**: 지속적인 학습으로 품질 향상

## 라이선스

MIT License
