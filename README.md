# FSTDB - File System Tree Database

파일 시스템 기반 트리 데이터베이스 라이브러리

## 개요

FSTDB는 파일 시스템의 특정 경로를 기준으로 파일/폴더 이름이 특정 패턴(`이름___id_숫자`)을 만족하는 객체를 레코드로 인식하는 트리 기반 데이터베이스 라이브러리입니다. 실제 파일 시스템과 직접 연동되어 파일/폴더를 생성하고 삭제할 수 있습니다.
- 파일 시스템은 DB와 다르게 편집기에서 원하는 항목을 쉽게 찾아 열람할 수 있다.
- DB는 id를 기반으로 참조가 편리하고 파일의 실제 저장 경로에 종속되지 않는다.
- 따라서 레코드들을 파일 시스템에 저장하며 id를 기반으로 db 처럼 다룰 수 있는 라이브러리를 개발함

## 주요 특징

- 🌳 **트리 구조 기반**: 디렉터리 구조를 트리로 표현하여 계층적 데이터 관리
- 📁 **파일 시스템 연동**: 실제 파일/폴더를 생성하고 삭제하는 기능 제공
- 🔍 **패턴 기반 레코드 인식**: `이름___id_숫자` 패턴을 만족하는 파일/폴더를 자동으로 레코드로 인식
- 🎨 **확장 가능한 아키텍처**: 제네릭 타입을 활용하여 커스텀 Node, Record, TreeDB 클래스 생성 가능
- 📊 **다양한 시각화**: 트리 구조를 텍스트나 pandas DataFrame으로 변환 가능
- 🔧 **하위 데이터베이스 조회**: 특정 경로의 하위 트리를 별도의 데이터베이스로 조회 가능

## 설치

```bash
pip install fstdb
```

## 요구사항

- Python 3.8 이상
- pandas (시각화 기능 사용 시)

## 기본 사용법

### 1. 기본 TreeDB 사용

```python
from pathlib import Path
from fstdb import TreeDB
from fstdb.factory import DBFactory

# Factory 생성
factory = DBFactory()
db = factory.create_tree_db(path=Path("./my_database"))

# 레코드 조회
print(f"총 레코드 개수: {len(db)}")
print(f"레코드 ID 목록: {sorted(db.ids)}")

# 특정 레코드 조회
record = db.get_record(1)
print(f"레코드 ID: {record.id}, 경로: {record.path}")

# 새 레코드 생성 (실제 파일/폴더 생성)
new_id = db.create_record("new_file___id_10.py")

# 레코드 삭제 (실제 파일/폴더 삭제)
db.remove_record(1)

# 하위 데이터베이스 조회
sub_db = db.get_sub_db("data")
```

### 2. 레코드 패턴

레코드로 인식되려면 파일/폴더 이름이 다음 패턴을 만족해야 합니다:

```
이름___id_숫자[.확장자]
```

예시:
- `user___id_1.py` ✅
- `product___id_2.txt` ✅
- `data___id_3` ✅ (폴더)
- `document___id_5.md` ✅

- 패턴은 변경 가능

### 3. 파일 구조화 예시

FSTDB를 사용하려면 데이터베이스 루트 디렉터리를 지정하고, 그 아래에 `이름___id_숫자` 패턴을 가진 파일/폴더를 배치하면 됩니다.

#### 기본 구조 예시

```
my_database/                    # 데이터베이스 루트 경로
├── user___id_1.py              # 레코드 ID: 1
├── product___id_2.txt          # 레코드 ID: 2
├── document___id_5.md          # 레코드 ID: 5
└── data/                       # 일반 폴더 (레코드 아님)
    ├── a___id_3.json            # 레코드 ID: 3
    └── b___id_4                # 레코드 ID: 4 (폴더)
```

#### 중요한 규칙

1. **루트 경로 자체는 확인하지 않음**: 루트 디렉터리(`my_database`) 자체는 레코드로 인식되지 않으며, 그 하위 항목만 순회합니다.

2. **패턴을 만족하는 항목만 레코드**: `이름___id_숫자` 패턴을 만족하는 파일/폴더만 레코드로 인식됩니다.

3. **일반 폴더는 무시**: 패턴을 만족하지 않는 일반 폴더(예: `data/`, `category/`)는 레코드가 아니지만, 그 안의 레코드를 찾기 위한 경로로 사용됩니다.

4. **확장자 유무**: 
   - 확장자가 있으면 파일로 인식 (예: `user___id_1.py`)
   - 확장자가 없으면 폴더로 인식 (예: `backup___id_7`)

5. **중첩 구조 지원**: 레코드는 루트 아래 어느 깊이에 있어도 인식됩니다.

#### 실제 사용 예시

```python
from pathlib import Path
from fstdb.factory import DBFactory

# 위의 구조로 파일을 준비한 후
factory = DBFactory()
db = factory.create_tree_db(path=Path("./my_database"))

# 모든 레코드 조회
print(f"총 레코드: {len(db)}")  # 7개 (ID: 1, 2, 3, 4, 5, 6, 7)
print(f"레코드 ID: {sorted(db.ids)}")  # [1, 2, 3, 4, 5, 6, 7]

# 특정 하위 경로의 레코드만 조회
sub_db = db.get_sub_db("data")
print(f"data 하위 레코드: {sorted(sub_db.ids)}")  # [3, 4]
```

### 4. 트리 구조 시각화

```python
from fstdb.factory import DBFactory

factory = DBFactory()
db = factory.create_tree_db(path=Path("./my_database"))

# 텍스트로 트리 구조 출력
viewer = factory.create_viewer(db)
print(viewer.to_text())

# pandas DataFrame으로 변환
df = viewer.to_df()
print(df)
```

## 고급 사용법: 커스텀 클래스

FSTDB는 제네릭 타입을 활용하여 커스텀 클래스를 만들 수 있습니다.

### 커스텀 Node, Record, TreeDB 정의

```python
from fstdb import TreeDB
from fstdb.factory import DBFactory
from fstdb.tree import TreeNode
from fstdb.db.record import Record
from pathlib import Path

# 커스텀 TreeNode 서브클래스
class CustomNode(TreeNode):
    def __init__(self, name: str, parent=None):
        super().__init__(name, parent)
        self.created_at = None
    
    def get_info(self) -> str:
        return f"CustomNode: {self.name}"

# 커스텀 Record 서브클래스
class CustomRecord(Record):
    def __init__(self, id: int, path: Path):
        super().__init__(id, path)
        self.metadata = {}
    
    def get_info(self) -> str:
        return f"CustomRecord: ID={self.id}, Path={self.path}"

# 커스텀 TreeDB 서브클래스
class CustomTreeDB(TreeDB[CustomNode, CustomRecord]):
    def get_all_records_info(self) -> list:
        """모든 레코드의 정보를 반환"""
        return [self.get_record(record_id).get_info() 
                for record_id in self.ids]
    
    def get_record_count_by_type(self) -> dict:
        """레코드 타입별 개수를 반환"""
        file_count = sum(1 for id in self.ids 
                        if self.get_record(id).path.is_file())
        dir_count = sum(1 for id in self.ids 
                       if self.get_record(id).path.is_dir())
        return {"files": file_count, "directories": dir_count}

# Factory 생성 및 사용
factory = DBFactory[CustomNode, CustomRecord, CustomTreeDB](
    NodeClass=CustomNode,
    TreeDBClass=CustomTreeDB,
    RecordClass=CustomRecord
)

db = factory.create_tree_db(path=Path("./my_database"))

# 커스텀 메서드 사용
print(db.get_all_records_info())
print(db.get_record_count_by_type())
```

## 주요 클래스

### TreeDB

트리 기반 데이터베이스의 메인 클래스입니다.

**주요 메서드:**
- `get_record(id: int) -> Record`: ID로 레코드 조회
- `create_record(name: RecordPath) -> int`: 새 레코드 생성 (파일/폴더 생성)
- `remove_record(id: int) -> None`: 레코드 삭제 (파일/폴더 삭제)
- `get_sub_db(name: RecordPath) -> TreeDB`: 하위 데이터베이스 조회
- `__len__() -> int`: 레코드 개수 반환
- `__contains__(id: int) -> bool`: 레코드 존재 여부 확인

**주요 속성:**
- `ids: Set[int]`: 모든 레코드 ID 집합
- `tree: NodeType`: 루트 트리 노드

### DBFactory

데이터베이스 및 관련 객체를 생성하는 팩토리 클래스입니다.

**주요 메서드:**
- `create_tree_db(path: Optional[Path]) -> TreeDB`: TreeDB 인스턴스 생성
- `create_viewer(tree_db: TreeDB) -> TreeDBViewer`: 시각화 도구 생성

### TreeDBViewer

트리 구조를 다양한 형태로 변환하는 클래스입니다.

**주요 메서드:**
- `to_text() -> str`: 트리 구조를 텍스트 문자열로 변환
- `to_df() -> pd.DataFrame`: 트리 구조를 pandas DataFrame으로 변환

## 장점

1. **파일 시스템과의 직접 연동**: 데이터베이스 작업이 실제 파일 시스템에 반영됩니다
2. **계층적 데이터 관리**: 디렉터리 구조를 트리로 표현하여 복잡한 데이터 구조를 쉽게 관리할 수 있습니다
3. **확장성**: 제네릭 타입을 활용하여 프로젝트에 맞는 커스텀 클래스를 쉽게 만들 수 있습니다
4. **타입 안정성**: Python의 타입 힌트를 적극 활용하여 타입 안정성을 보장합니다
5. **직관적인 API**: 간단하고 직관적인 API로 쉽게 사용할 수 있습니다

## 사용 예제

전체 사용 예제는 `example.py` 파일을 참고하세요.

```python
# example.py 실행
python example.py
```

## 라이선스

MIT License
