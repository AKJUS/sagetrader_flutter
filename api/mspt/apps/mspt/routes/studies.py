from typing import List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Request
)
from sqlalchemy.orm import Session

from mspt.apps.mspt import (
    schemas,
    crud,
)
from mspt.apps.users import models as user_models
from mspt.settings.database import get_db
from mspt.settings.security import (
    get_current_active_user
)
from mspt.utils.create_dirs import resolve_media_dirs_for

router = APIRouter()
db_session = Session()


#
# ........ Study Routes .........
#


@router.get("/study", response_model=schemas.StudyPaginated)
def read_studies(
        *,
        db: Session = Depends(get_db),
        request: Request,
        page: int = 1,
        size: int = 20,
        shared: bool = False,
        sort_on: str = 'uid',
        sort_order: str = 'desc',
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Retrieve studies.
    """
    studies = crud.study.get_paginated_multi(
        db, 
        request=request,
        page=page, 
        size=size, 
        owner_uid=current_user.uid,
        shared=shared,
        sort_on=sort_on,        
        sort_order=sort_order
    )
    return studies


@router.post("/study", response_model=schemas.Study)
def create_study(
        *,
        db: Session = Depends(get_db),
        study_in: schemas.StudyCreate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Create new study.
    """
    study_in.owner_uid = current_user.uid
    study = crud.study.create(db, obj_in=study_in)
    return study


@router.put("/study/{study_uid}", response_model=schemas.Study)
def update_study(
        *,
        db: Session = Depends(get_db),
        study_uid: int,
        study_in: schemas.StudyUpdate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Update an study.
    """
    study = crud.study.get(db, uid=study_uid)
    if not study:
        raise HTTPException(
            status_code=404,
            detail="This study does not exist in the system",
        )
    study = crud.study.update(db, db_obj=study, obj_in=study_in)
    return study


@router.delete("/study/{study_uid}", response_model=schemas.StudyDelete)
def delete_study(
        *,
        db: Session = Depends(get_db),
        study_uid: int,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Delete an study.
    """
    study = crud.study.get(db, uid=study_uid)
    if not study:
        raise HTTPException(
            status_code=404,
            detail="This study does not exist in the system",
        )
    study = crud.study.remove(db, uid=study_uid)
    return study


#
# ........ Study Item Routes .........
#


@router.get("/studyitems/{study_uid}", response_model=schemas.StudyItemPaginated)
def read_study_items(
        *,
        db: Session = Depends(get_db),
        request: Request,
        study_uid: int,
        page: int = 1,
        size: int = 20,
        shared: bool = False,
        sort_on: str = 'uid',
        sort_order: str = 'desc',
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Retrieve studyitems.
    """
    s_items = crud.studyitem.get_paginated_multi(
        db, 
        request=request,
        page=page, 
        size=size, 
        owner_uid=None,
        shared=shared,
        sort_on=sort_on,        
        sort_order=sort_order,
        other_filters=[{'field': 'study_uid', 'op': '==', 'value': study_uid}] if study_uid else []
    )
    return s_items


@router.post("/studyitems", response_model=schemas.StudyItemWithAttrs)
def create_studyitems(
        *,
        db: Session = Depends(get_db),
        studyitem_in: schemas.StudyItemCreateWithAttrs,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Create new studyitem.
    """
    studyitem = crud.studyitem.create(db, obj_in=studyitem_in)
    # studyitem.date = str(studyitem.date)
    return studyitem


@router.put("/studyitems/{studyitem_uid}", response_model=schemas.StudyItemWithAttrs)
def update_studyitems(
        *,
        db: Session = Depends(get_db),
        studyitem_uid: int,
        studyitem_in: schemas.StudyItemUpdateWithAttrs,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Update an studyitems.
    """
    studyitem = crud.studyitem.get(db, uid=studyitem_uid)
    if not studyitem:
        raise HTTPException(
            status_code=404,
            detail="This studyitem does not exist in the system",
        )

    studyitem = crud.studyitem.update(db, db_obj=studyitem, obj_in=studyitem_in)
    # studyitem.date = str(studyitem.date)
    return studyitem


@router.delete("/studyitems/{studyitem_uid}", response_model=schemas.StudyItem)
def delete_studyitems(
        *,
        db: Session = Depends(get_db),
        studyitem_uid: int,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Delete an studyitem.
    """
    studyitem = crud.studyitem.get(db, uid=studyitem_uid)
    if not studyitem:
        raise HTTPException(
            status_code=404,
            detail="This studyitem does not exist in the system",
        )
    studyitem = crud.studyitem.remove(db, uid=studyitem_uid)
    return studyitem


#
# ........ Attribute Routes .........
#

@router.get("/attribute/{study_uid}", response_model=List[schemas.Attribute])
def read_attributes(
        *,
        db: Session = Depends(get_db),
        study_uid: int,
        skip: int = 0,
        limit: int = 100,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Retrieve Attrs.
    """
    attrs = crud.attribute.get_multi_by_study(db, study_uid=study_uid, skip=skip, limit=limit)
    return attrs


@router.post("/attribute", response_model=schemas.Attribute)
def create_attribute(
        *,
        db: Session = Depends(get_db),
        attrs_in: schemas.AttributeCreate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Create new attr.
    """
    attrs = crud.attribute.create(db, obj_in=attrs_in)
    return attrs


@router.put("/attribute/{attr_uid}", response_model=schemas.Attribute)
def update_attribute(
        *,
        db: Session = Depends(get_db),
        attr_uid: int,
        attr_in: schemas.AttributeUpdate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Update an attr.
    """
    attr = crud.attribute.get(db, uid=attr_uid)
    if not attr:
        raise HTTPException(
            status_code=404,
            detail="This attribute does not exist in the system",
        )
    attr = crud.attribute.update(db, db_obj=attr, obj_in=attr_in)
    return attr


@router.delete("/attribute/{attr_uid}", response_model=schemas.Attribute)
def delete_attribute(
        *,
        db: Session = Depends(get_db),
        attr_uid: int,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Delete an attr.
    """
    attr = crud.attribute.get(db, uid=attr_uid)
    if not attr:
        raise HTTPException(
            status_code=404,
            detail="This attribute does not exist in the system",
        )
    attr = crud.attribute.remove(db, uid=attr_uid)
    return attr

