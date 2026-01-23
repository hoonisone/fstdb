from fstdb import DBFactory, TreeDB, TreeNode, Record
from pathlib import Path
from fstdb.db.path_manager import RecordPath

from typing_extensions import Self



class CustomNode(TreeNode):
    ...

class CustomRecord(Record):

    @property
    def config_file_path(self)->Path:
        if self.path.is_dir():
            return self.path/"config.py"
        else:
            return self.path


class CustomDB(TreeDB[CustomNode, CustomRecord]):
    ...    

CustomFactory = DBFactory[CustomNode, CustomRecord, CustomDB]
def get_factory()->CustomFactory:
    return CustomFactory(CustomNode, CustomDB, CustomRecord)

factory = get_factory()
db = factory.create_tree_db(Path("/home/resource/2_rsc3"))
db = db.get_sub_db("_elements/1_dataset")
viewer = factory.create_viewer(db)
print(viewer.to_text())
record = db.get_record(1)
print(type(record))
print(record.config_file_path)