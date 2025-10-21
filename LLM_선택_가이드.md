# 🤖 LLM 선택 가이드

## 어떤 LLM을 사용해야 할까요?

이 앱은 **3가지 LLM**을 지원합니다. 상황에 맞게 선택하세요!

---

## 📊 LLM 비교표

| 특징 | Google Gemini | OpenAI GPT-4 | Ollama (로컬) |
|------|---------------|--------------|---------------|
| **비용** | ⭐⭐⭐⭐⭐ 무료 제공량 넉넉 | ⭐⭐ 사용량 기반 | ⭐⭐⭐⭐⭐ 완전 무료 |
| **성능** | ⭐⭐⭐⭐ 매우 좋음 | ⭐⭐⭐⭐⭐ 최고 | ⭐⭐⭐ 준수 |
| **속도** | ⭐⭐⭐⭐ 빠름 | ⭐⭐⭐⭐ 빠름 | ⭐⭐ 느림 (M4는 빠름) |
| **설정 난이도** | ⭐⭐⭐⭐⭐ 매우 쉬움 | ⭐⭐⭐⭐ 쉬움 | ⭐⭐ 약간 복잡 |
| **인터넷 필요** | ✅ 필요 | ✅ 필요 | ❌ 불필요 |
| **개인정보** | 클라우드 | 클라우드 | ⭐⭐⭐⭐⭐ 로컬만 |

---

## 🎯 상황별 추천

### 🌟 처음 사용하는 경우
**추천: Google Gemini**
- 무료 제공량이 충분함
- 성능 우수
- 설정 간단
- 결제 카드 등록 불필요

**설정 방법:**
1. https://aistudio.google.com/app/apikey
2. "Create API key" 클릭
3. 복사해서 앱에 입력

---

### 💼 업무용으로 사용하는 경우
**추천: OpenAI GPT-4**
- 가장 강력한 성능
- 복잡한 워크플로우도 완벽 생성
- 안정적인 서비스
- 비용: 요청당 약 $0.03-0.05

**설정 방법:**
1. https://platform.openai.com/ 가입
2. $5-10 크레딧 충전
3. API 키 생성
4. 앱에 입력

---

### 🔒 개인정보 보호가 중요한 경우
**추천: Ollama (로컬)**
- 모든 데이터가 Mac에만 저장
- 인터넷 없이 사용 가능
- 완전 무료
- 단점: 성능은 떨어짐

**설정 방법:**
1. https://ollama.ai/download 설치
2. 터미널에서 `ollama pull llama3.2`
3. 앱에서 Ollama 선택 (API 키 불필요)

---

### 💰 비용을 최소화하려는 경우
**추천 순서:**
1. **Google Gemini** (무료 제공량으로 시작)
2. **Ollama** (완전 무료, 로컬)
3. **OpenAI** (유료지만 가장 강력)

---

## 📝 각 LLM 설정 방법

### 1️⃣ Google Gemini 설정

**API 키 받기:**
```bash
1. https://aistudio.google.com/app/apikey 접속
2. Google 계정으로 로그인
3. "Create API key" 클릭
4. "Create API key in new project" 선택
5. 생성된 키 복사 (예: AIzaSy...)
```

**앱에서 설정:**
```
설정 이름: My Gemini
제공자: Google Gemini
모델 이름: gemini-1.5-pro
API Key: AIzaSy... (복사한 키)
기본 설정으로 사용: ✅
```

**무료 제공량:**
- 분당 15개 요청
- 하루 1,500개 요청
- 일반 사용에 충분!

---

### 2️⃣ OpenAI GPT-4 설정

**API 키 받기:**
```bash
1. https://platform.openai.com/ 가입
2. https://platform.openai.com/api-keys 접속
3. "Create new secret key" 클릭
4. 이름 입력 (예: n8n-generator)
5. 생성된 키 복사 (예: sk-proj...)
6. https://platform.openai.com/settings/organization/billing
   에서 $5-10 크레딧 충전
```

**앱에서 설정:**
```
설정 이름: My GPT-4
제공자: OpenAI (GPT-4, GPT-3.5)
모델 이름: gpt-4-turbo-preview
API Key: sk-proj... (복사한 키)
기본 설정으로 사용: ✅
```

**비용 예상:**
- 워크플로우 1개 생성: $0.05-0.10
- $10으로 약 100-200개 생성 가능

---

### 3️⃣ Ollama (로컬) 설정

**Ollama 설치:**
```bash
# 1. Ollama 다운로드 및 설치
open https://ollama.ai/download
# Mac용 .dmg 파일 다운로드 → 설치

# 2. 모델 다운로드 (한 번만)
ollama pull llama3.2
# 또는 더 큰 모델: ollama pull llama3.2:70b

# 3. 실행 확인
ollama list
```

**앱에서 설정:**
```
설정 이름: Local Llama
제공자: Ollama (로컬 무료)
모델 이름: llama3.2
API URL: http://localhost:11434
기본 설정으로 사용: ✅
```

**장점:**
- 완전 무료
- 인터넷 불필요
- 개인정보 완벽 보호
- M4 Mac에서 빠른 속도

**단점:**
- 초기 다운로드 필요 (약 2-4GB)
- 성능은 GPT-4보다 낮음

---

## 🔄 여러 LLM 함께 사용하기

**추천 방법:**
1. **Gemini**: 기본으로 사용 (무료)
2. **GPT-4**: 복잡한 워크플로우용 (유료)
3. **Ollama**: 테스트용 (무료)

**설정에서 전환:**
- 각 LLM을 모두 추가
- 원하는 LLM 옆의 ✅ 버튼 클릭
- 즉시 전환됨!

---

## 💡 모델 선택 가이드

### Google Gemini 모델
- **gemini-1.5-pro**: 균형잡힌 성능 (추천)
- **gemini-1.5-flash**: 더 빠르고 저렴
- **gemini-1.0-pro**: 구버전 (비추천)

### OpenAI 모델
- **gpt-4-turbo-preview**: 최신 GPT-4 (추천)
- **gpt-4**: 안정적인 GPT-4
- **gpt-3.5-turbo**: 저렴하지만 성능 낮음

### Ollama 모델
- **llama3.2**: 빠르고 가벼움 (3GB, 추천)
- **llama3.2:70b**: 강력하지만 느림 (39GB)
- **codellama**: 코드 특화 모델

---

## ❓ FAQ

### Q: 어떤 LLM이 가장 좋나요?
**A:** 성능은 **GPT-4 > Gemini > Ollama** 순이지만, 
무료로 시작하려면 **Gemini**를 추천합니다!

### Q: Gemini 무료 제공량이 부족하면?
**A:** Ollama로 전환하거나, OpenAI 유료 사용을 고려하세요.

### Q: 여러 LLM을 동시에 사용할 수 있나요?
**A:** 네! 설정에서 여러 개 추가하고 상황에 따라 전환하세요.

### Q: Ollama가 너무 느려요!
**A:** 더 작은 모델(`llama3.2:3b`)을 사용하거나 Gemini로 전환하세요.

### Q: OpenAI 비용이 얼마나 나올까요?
**A:** 워크플로우 1개당 약 $0.05-0.10입니다. 
$10으로 100-200개 생성 가능합니다.

### Q: API 키를 여러 개 등록할 수 있나요?
**A:** 네! 각 제공자별로 여러 설정을 만들 수 있습니다.

---

## 🎯 결론

### 처음 사용자
→ **Google Gemini** (무료, 쉬움, 성능 좋음)

### 업무 사용자
→ **OpenAI GPT-4** (유료, 최고 성능)

### 개인정보 중시
→ **Ollama** (무료, 로컬, 안전)

---

**모든 LLM을 추가해두고 상황에 맞게 전환하며 사용하세요! 🚀**
