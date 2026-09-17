# meww-api

FastAPI 기반 API 서버. Google Gemini API를 호출하는 `/ask` 엔드포인트를 포함합니다.

## 기술 스택

- Python 3.9
- FastAPI
- httpx (비동기 HTTP 클라이언트)
- pydantic
- pytest / pytest-asyncio

## 시작하기

### 1. 가상환경 설정 및 의존성 설치

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 환경변수 설정

`/ask` 엔드포인트는 Google Gemini API 키가 필요합니다.

```bash
export GOOGLE_GEMINI_API_KEY="your-api-key"
```

### 3. 서버 실행

```bash
uvicorn main:app --reload
```

기본적으로 `http://localhost:8000`에서 실행됩니다. 대화형 API 문서는 `http://localhost:8000/docs`에서 확인할 수 있습니다.

## API 엔드포인트

| Method | Path | 설명 |
| --- | --- | --- |
| GET | `/health` | 서버 상태 확인 (헬스체크) |
| POST | `/echo` | 요청 바디(`title`, `creator`, `rating`)를 그대로 반환 |
| POST | `/ask` | `prompt`를 Gemini API로 전달하고 생성된 답변을 반환 |

### `/ask` 요청 예시

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "안녕하세요"}'
```

`call_gemini` 함수는 Gemini API가 `429(Too Many Requests)`를 반환하면 1초 대기 후 최대 2번까지 재시도합니다 (총 3회 시도). 429가 아닌 에러는 재시도 없이 즉시 실패합니다.

## 테스트

```bash
pytest
```

`main` 브랜치에 push될 때 GitHub Actions(`.github/workflows/ci.yml`)가 자동으로 테스트를 실행합니다.

## Docker

```bash
docker build -t meww-api .
docker run -p 8000:8000 -e GOOGLE_GEMINI_API_KEY="your-api-key" meww-api
```

## 프로젝트 구조

```
.
├── main.py                 # FastAPI 앱 및 엔드포인트 정의
├── tests/
│   └── test_main.py        # pytest 테스트
├── Dockerfile
├── requirements.txt
└── .github/
    ├── workflows/ci.yml            # CI (push to main 시 테스트 실행)
    └── PULL_REQUEST_TEMPLATE.md    # PR 템플릿
```
