# 빌드 및 PyPI 배포 가이드

## 1. 개발 환경 설정

```bash
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화 (Windows)
venv\Scripts\activate

# 가상 환경 활성화 (Linux/Mac)
source venv/bin/activate

# 필요한 패키지 설치
pip install --upgrade pip
pip install build twine wheel
```

## 2. 빌드

```bash
# 소스 배포판과 wheel 파일 생성
python -m build

# 또는 (구식 방법)
python setup.py sdist bdist_wheel
```

빌드 결과물은 `dist/` 폴더에 생성됩니다.

## 3. PyPI에 업로드

### 테스트 PyPI에 먼저 업로드

```bash
# 테스트 PyPI에 업로드
python -m twine upload --repository testpypi dist/*

# 업로드된 패키지 테스트
pip install --index-url https://test.pypi.org/simple/ fstdb
```

### 실제 PyPI에 업로드

```bash
# 실제 PyPI에 업로드
python -m twine upload dist/*
```

## 4. PyPI 계정 설정

1. [PyPI](https://pypi.org/account/register/)에 계정 생성
2. [TestPyPI](https://test.pypi.org/account/register/)에도 계정 생성
3. API 토큰 생성:
   - PyPI: Account Settings → API tokens
   - 토큰 생성 후 `~/.pypirc` 파일에 저장하거나 환경 변수로 설정

### `~/.pypirc` 파일 설정 (선택사항)

```
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-token-here
```

## 5. 버전 업데이트

버전을 업데이트할 때는 다음 파일들을 수정하세요:

- `pyproject.toml`의 `version` 필드
- `setup.py`의 `version` 필드
- `fstdb/__init__.py`의 `__version__`

## 6. 간편 스크립트

### Windows (build_and_publish.bat)

```batch
@echo off
echo Building package...
python -m build
echo.
echo Uploading to PyPI...
python -m twine upload dist/*
echo Done!
```

### Linux/Mac (build_and_publish.sh)

```bash
#!/bin/bash
echo "Building package..."
python -m build
echo ""
echo "Uploading to PyPI..."
python -m twine upload dist/*
echo "Done!"
```

## 주의사항

- PyPI에 업로드한 버전은 삭제할 수 없습니다. 테스트 PyPI에서 먼저 확인하세요.
- 버전 번호는 항상 증가시켜야 합니다.
- `README.md`와 `LICENSE` 파일을 포함했는지 확인하세요.
