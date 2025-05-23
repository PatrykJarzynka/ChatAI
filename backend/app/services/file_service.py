from typing import Sequence, List
from sqlmodel import Session, select
from tables.file import File

class FileService:

    def __init__(self, session: Session):
        self.session = session

    def save_file(self, file: File) -> None:
        self.session.add(file)
        self.session.commit()
        self.session.refresh(file)

    def get_user_files_by_ids(self, files_ids: List[int], user_id: int) -> Sequence[File]:
        statement = select(File).where(
            (File.user_id == user_id) &
            (File.id.in_(files_ids)) # type: ignore
        )

        return self.session.exec(statement).all()