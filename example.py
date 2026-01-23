"""
FSTDB (File System Tree Database) 사용 예제

이 예제는 파일 시스템의 특정 경로를 기준으로 
파일/폴더 이름이 특정 패턴(이름___id_숫자)을 만족하는 객체를 레코드로 인식하는 
트리 기반 데이터베이스 라이브러리의 사용법을 보여줍니다.
"""

import tempfile
import shutil
from pathlib import Path
from fstdb import TreeDB
from fstdb.factory import DBFactory
from fstdb.tree import TreeNode
from fstdb.db.record import Record
from fstdb.db.tree_db import TreeDB as BaseTreeDB


# 커스텀 TreeNode 서브클래스
class CustomNode(TreeNode):
    """커스텀 TreeNode 클래스 - 추가 기능을 가진 노드"""
    
    def __init__(self, name: str, parent=None):
        super().__init__(name, parent)
        self.created_at = None  # 추가 속성 예시
    
    def get_info(self) -> str:
        """노드 정보를 반환하는 커스텀 메서드"""
        return f"CustomNode: {self.name} (path: {'/'.join(self.full_name)})"


# 커스텀 Record 서브클래스
class CustomRecord(Record):
    """커스텀 Record 클래스 - 추가 기능을 가진 레코드"""
    
    def __init__(self, id: int, path: Path):
        super().__init__(id, path)
        self.metadata = {}  # 추가 속성 예시
    
    def get_info(self) -> str:
        """레코드 정보를 반환하는 커스텀 메서드"""
        return f"CustomRecord: ID={self.id}, Path={self.path}"


# 커스텀 TreeDB 서브클래스
class CustomTreeDB(TreeDB[CustomNode, CustomRecord]):
    """커스텀 TreeDB 클래스 - 추가 기능을 가진 데이터베이스"""
    
    def get_all_records_info(self) -> list:
        """모든 레코드의 정보를 반환하는 커스텀 메서드"""
        return [self.get_record(record_id).get_info() for record_id in self.ids]
    
    def get_record_count_by_type(self) -> dict:
        """레코드 타입별 개수를 반환하는 커스텀 메서드"""
        file_count = 0
        dir_count = 0
        
        for record_id in self.ids:
            record = self.get_record(record_id)
            if record.path.is_file():
                file_count += 1
            elif record.path.is_dir():
                dir_count += 1
        
        return {"files": file_count, "directories": dir_count}


def main():
    """FSTDB 기본 사용 예제: 파일 생성, 조회, 추가, 삭제"""
    print("=" * 60)
    print("FSTDB (File System Tree Database) 사용 예제")
    print("=" * 60)
    
    # 임시 디렉터리 생성
    temp_dir = tempfile.mkdtemp()
    test_path = Path(temp_dir) / "test_db"
    test_path.mkdir(parents=True, exist_ok=True)
    
    try:
        print(f"\n테스트 경로: {test_path}")
        
        # 1. ___id_ 패턴에 맞는 파일 5개 생성
        print("\n[1단계] ___id_ 패턴에 맞는 파일 5개 생성")
        test_files = [
            "user___id_1.py",
            "product___id_2.txt",
            "data/a___id_3.json",
            "data/b___id_4",  # 폴더 (확장자 없음)
            "document___id_5.md"
        ]
        
        for file_name in test_files:
            file_path = test_path / file_name
            # 부모 디렉터리 생성
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 마지막 부분의 이름으로 확장자 확인
            last_part = file_path.name
            if last_part and '.' in last_part and not last_part.startswith('.'):
                # 확장자가 있으면 파일
                file_path.touch()
                print(f"  ✓ 파일 생성: {file_name}")
            else:
                # 확장자가 없으면 폴더
                file_path.mkdir(exist_ok=True)
                print(f"  ✓ 폴더 생성: {file_name}")
        
        # 2. Factory 생성 및 커스텀 TreeDB 생성
        print("\n[2단계] Factory 생성 및 커스텀 TreeDB 생성")
        factory = DBFactory[CustomNode, CustomRecord, CustomTreeDB](
            NodeClass=CustomNode, 
            TreeDBClass=CustomTreeDB,
            RecordClass=CustomRecord
        )
        db = factory.create_tree_db(path=test_path)  # 커스텀 TreeDB를 반환함
        
        print(f"  ✓ 커스텀 Factory 생성 완료 (CustomNode, CustomTreeDB, CustomRecord 사용)")
        print(f"  ✓ TreeDB 생성 완료")
        print(f"  데이터베이스 경로: {db.tree.name}")
        
        # 3. 파일 조회
        print("\n[3단계] 파일 조회")
        print(f"  총 레코드 개수: {len(db)}")
        print(f"  레코드 ID 목록: {sorted(db.ids)}")
        
        print("\n  모든 레코드 정보:")
        for record_id in sorted(db.ids):
            record = db.get_record(record_id)
            file_type = "파일" if record.path.is_file() else "폴더"
            print(f"    ID {record.id}: {record.path.name} ({file_type})")
            print(f"      경로: {record.path}")
            # 커스텀 Record의 get_info() 메서드 사용
            print(f"      커스텀 정보: {record.get_info()}")
        
        # 커스텀 TreeDB 메서드 사용
        print("\n  커스텀 TreeDB 기능:")
        print(f"    레코드 타입별 개수: {db.get_record_count_by_type()}")
        print(f"    모든 레코드 정보 (커스텀 메서드):")
        for info in db.get_all_records_info():
            print(f"      - {info}")
        
        # 4. 새 레코드 추가
        print("\n[4단계] 새 레코드 추가")
        new_record_name = "new_record.py"
        new_record_id = db.create_record(new_record_name)
        print(f"  ✓ 레코드 추가 완료: {new_record_name} (ID: {new_record_id})")
        print(f"  현재 레코드 개수: {len(db)}")
        print(f"  레코드 ID 목록: {sorted(db.ids)}")
        
        # 추가된 레코드 확인
        new_record = db.get_record(new_record_id)
        print(f"  추가된 레코드 경로: {new_record.path}")
        print(f"  파일 존재 여부: {new_record.path.exists()}")
        
        # 5. 레코드 삭제
        print("\n[5단계] 레코드 삭제")
        if db.ids:
            delete_id = sorted(db.ids)[0]  # 첫 번째 레코드 삭제
            delete_record = db.get_record(delete_id)
            delete_path = delete_record.path
            
            print(f"  삭제할 레코드: ID {delete_id} ({delete_path.name})")
            print(f"  삭제 전 파일 존재 여부: {delete_path.exists()}")
            
            db.remove_record(delete_id)
            
            print(f"  ✓ 레코드 삭제 완료: ID {delete_id}")
            print(f"  삭제 후 레코드 개수: {len(db)}")
            print(f"  삭제 후 레코드 ID 목록: {sorted(db.ids)}")
            print(f"  삭제 후 파일 존재 여부: {delete_path.exists()}")
        
        # 6. 최종 상태 확인 및 하위 데이터베이스 조회
        print("\n[6단계] 최종 상태 확인 및 하위 데이터베이스 조회")
        print(f"  최종 레코드 개수: {len(db)}")
        print(f"  최종 레코드 ID 목록: {sorted(db.ids)}")
        
        print("\n  트리 구조:")
        viewer = factory.create_viewer(db)
        print(viewer.to_text())
        
        # 하위 데이터베이스 조회
        print("\n  'data' 하위 데이터베이스 조회:")
        try:
            sub_db = db.get_sub_db("data")
            print(f"    하위 레코드 개수: {len(sub_db)}")
            print(f"    하위 레코드 ID 목록: {sorted(sub_db.ids)}")
            
            print("\n    하위 트리 구조:")
            sub_viewer = factory.create_viewer(sub_db)
            print(sub_viewer.to_text())
            print(sub_viewer.to_df())
            
            print("\n    하위 레코드 상세 정보:")
            for record_id in sorted(sub_db.ids):
                record = sub_db.get_record(record_id)
                file_type = "파일" if record.path.is_file() else "폴더"
                print(f"      ID {record.id}: {record.path.name} ({file_type})")
                print(f"        경로: {record.path}")
        except ValueError as e:
            print(f"    오류: {e}")
        
        print("\n" + "=" * 60)
        print("예제 실행 완료!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 임시 디렉터리 정리
        if Path(temp_dir).exists():
            shutil.rmtree(temp_dir)
            print(f"\n임시 디렉터리 정리 완료: {temp_dir}")


if __name__ == "__main__":
    main()
