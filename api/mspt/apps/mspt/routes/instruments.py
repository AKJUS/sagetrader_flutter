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


@router.get("/instrument", response_model=List[schemas.Instrument])
def read_instruments(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 200,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Retrieve instruments.
    """
    instruments = crud.instrument.get_multi_for_user(db, owner_uid=current_user.uid, skip=skip, limit=limit)
    return instruments


@router.post("/instrument", response_model=schemas.Instrument)
def create_instrument(
        *,
        db: Session = Depends(get_db),
        instrument_in: schemas.InstrumentCreate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Create new instrument.
    """

    instrument = crud.instrument.get_by_name_owner(db, name=instrument_in.name, owner_uid=current_user.uid)
    if instrument:
        raise HTTPException(
            status_code=400,
            detail="This instrument already exists in the system.",
        )
    instrument_in.name = instrument_in.name.upper()
    instrument_in.owner_uid = current_user.uid
    instrument = crud.instrument.create(db, obj_in=instrument_in)
    return instrument


@router.put("/instrument/{instrument_uid}", response_model=schemas.Instrument)
def update_instrument(
        *,
        db: Session = Depends(get_db),
        instrument_uid: int,
        instrument_in: schemas.InstrumentUpdate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Update an instrument.
    """
    instrument = crud.instrument.get(db, uid=instrument_uid)
    if not instrument:
        raise HTTPException(
            status_code=404,
            detail="This instrument does not exist in the system",
        )
    instrument = crud.instrument.update(db, db_obj=instrument, obj_in=instrument_in)
    return instrument


@router.delete("/instrument/{instrument_uid}", response_model=schemas.InstrumentDelete)
def delete_instrument(
        *,
        db: Session = Depends(get_db),
        instrument_uid: int,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Delete an instrument.
    """
    instrument = crud.instrument.get(db, uid=instrument_uid)
    if not instrument:
        raise HTTPException(
            status_code=404,
            detail="This instrument does not exist in the system",
        )
    instrument = crud.instrument.remove(db, uid=instrument_uid)
    return instrument

