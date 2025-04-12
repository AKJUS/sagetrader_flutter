from typing import Optional
from sqlalchemy.orm import Session

from mspt.apps.users import models
from mspt.apps.users import schemas
from mspt.settings.security import verify_password, get_password_hash
from mspt.apps.mixins.crud import CRUDMIXIN


class CRUDUser(CRUDMIXIN[models.User, schemas.UserCreate, schemas.UserUpdate]):
    def get_by_email(self, db_session: Session, *, email: str) -> Optional[models.User]:
        result = db_session.query(models.User).filter(models.User.email == email).first()
        return result

    def create(self, db_session: Session, *, obj_in: schemas.UserCreate) -> models.User:
        db_obj = models.User(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            is_superuser=obj_in.is_superuser,
        )
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def authenticate(
        self, db_session: Session, *, email: str, password: str
    ) -> Optional[models.User]:
        user = self.get_by_email(db_session, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: models.User) -> bool:
        return user.is_active

    def is_superuser(self, user: models.User) -> bool:
        return user.is_superuser


user = CRUDUser(models.User)
