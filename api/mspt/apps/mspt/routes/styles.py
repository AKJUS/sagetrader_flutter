from typing import List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session

from mspt.apps.mspt import (
    schemas,
    crud
)
from mspt.apps.users import models as user_models
from mspt.settings.database import get_db
from mspt.settings.security import (
    get_current_active_user
)

router = APIRouter()
db_session = Session()

#
# ........ Style Routes .........
#
@router.get("/style", response_model=List[schemas.Style])
def read_styles(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Retrieve styles.
    """
    styles = crud.style.get_multi(db, skip=skip, limit=limit)
    return styles


@router.post("/style", response_model=schemas.Style)
def create_style(
        *,
        db: Session = Depends(get_db),
        style_in: schemas.StyleCreate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Create new style.
    """
    style = crud.style.get_by_name(db, name=style_in.name)
    if style:
        raise HTTPException(
            status_code=400,
            detail="This style already exists in the system.",
        )
    style_in.owner_uid = None
    style = crud.style.create(db, obj_in=style_in)
    return style


@router.put("/style/{style_uid}", response_model=schemas.Style)
def update_style(
        *,
        db: Session = Depends(get_db),
        style_uid: int,
        style_in: schemas.StyleUpdate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Update an style.
    """
    style = crud.style.get(db, uid=style_uid)
    if not style:
        raise HTTPException(
            status_code=404,
            detail="This style does not exist in the system",
        )
    style = crud.style.update(db, db_obj=style, obj_in=style_in)
    return style


@router.delete("/style/{style_uid}", response_model=schemas.StyleDelete)
def delete_style(
        *,
        db: Session = Depends(get_db),
        style_uid: int,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Delete an style.
    """
    style = crud.style.get(db, uid=style_uid)
    if not style:
        raise HTTPException(
            status_code=404,
            detail="This style does not exist in the system",
        )
    style = crud.style.remove(db, uid=style_uid)
    return style
