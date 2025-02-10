# Conscience System

![PyPI - Version](https://img.shields.io/pypi/v/conscience-system)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/conscience-system)
![PyPI - License](https://img.shields.io/pypi/l/conscience-system)
![PyPI - Downloads](https://img.shields.io/pypi/dm/conscience-system)

Django 기반 백엔드 시스템을 손쉽게 구성할 수 있는 자동화 도구입니다.

## 주요 기능

- 🚀 GUI 기반의 간편한 설정
- 🔧 Django 프로젝트 자동 구성
- 🗄️ 데이터베이스 마이그레이션 자동화
- 🔒 환경 변수 자동 설정
- 📦 의존성 자동 설치
- 🖥️ 개발 서버 자동 실행

## 설치 방법

```bash
# 신규 설치
pip install conscience-system

# 업그레이드
pip install -U conscience-system
```

## 시스템 요구사항

- Python 3.8 이상
- macOS
- PostgreSQL

## 사용 방법

1. 터미널에서 실행:

```bash
conscience-system
```

2. GUI 설정:

   - 서비스 이름 입력 (예: my_service)
   - Database URL 입력 (예: postgresql://user:password@localhost:5432/dbname)

3. "서비스 설정 및 실행" 버튼 클릭

## 자동 설정되는 항목

- ✅ 프로젝트 기본 구조
- ✅ 가상환경 설정
- ✅ Django 설정
- ✅ 데이터베이스 연결
- ✅ 마이그레이션
- ✅ CORS 설정
- ✅ 환경 변수
- ✅ Git 초기화

## 버전 기록

### 0.1.0 (2024-03-19)

- 패키지 구조 개선
- 문서화 강화

[이전 버전 기록 보기](https://github.com/seunghyunyu/conscience-system/releases)

## 개발자 가이드

### 개발 환경 설정

```bash
# 저장소 복제
git clone https://github.com/Kr-TeamWise/conscience-system
cd conscience-system

# 개발 의존성 설치
pip install -e ".[dev]"
```

### 코드 스타일

```bash
# 코드 포맷팅
black .
isort .

# 린트 체크
flake8
```

### 새 버전 배포

1. 버전 업데이트 (pyproject.toml)
2. 변경사항 커밋
3. 배포:

```bash
# 빌드
python -m build

# PyPI 배포
python -m twine upload dist/*
```

## 문제 해결

문제가 발생하면 [이슈 트래커](https://github.com/seunghyunyu/conscience-system/issues)를 확인하거나 새 이슈를 등록해주세요.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
이하 주요 라이언스는 Conscience Partners Inc. 에서 제공하는 라이선스입니다.
참여 개발자는 kris, dale, paul 입니다.

## 기여하기

모든 종류의 기여를 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 연락처

Seunghyun Yu - yush7881@gmail.com

프로젝트 링크: [https://github.com/Kr-TeamWise/conscience-system](https://github.com/Kr-TeamWise/conscience-system)
