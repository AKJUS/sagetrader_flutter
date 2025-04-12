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

router = APIRouter()
db_session = Session()


@router.get("/trade", response_model=schemas.TradePaginated)
def read_trades(
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
    Retrieve trades.
    """
    trades = crud.trade.get_paginated_multi(
        db, 
        request=request,
        page=page, 
        size=size, 
        owner_uid=current_user.uid,
        shared=shared,
        sort_on=sort_on,        
        sort_order=sort_order
    )
    return trades


@router.post("/trade", response_model=schemas.Trade)
def create_trade(
        *,
        db: Session = Depends(get_db),
        trade_in: schemas.TradeCreate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Create new trade.
    """
    trade_in.owner_uid = current_user.uid
    trade = crud.trade.create(db, obj_in=trade_in)
    trade.date = str(trade.date)
    return trade


@router.put("/trade/{trade_uid}", response_model=schemas.Trade)
def update_trade(
        *,
        db: Session = Depends(get_db),
        trade_uid: int,
        trade_in: schemas.TradeUpdate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Update an trade.
    """
    trade = crud.trade.get(db, uid=trade_uid)
    if not trade:
        raise HTTPException(
            status_code=404,
            detail="This trade does not exist in the system",
        )
    trade = crud.trade.update(db, db_obj=trade, obj_in=trade_in)
    trade.date = str(trade.date)
    return trade


@router.delete("/trade/{trade_uid}", response_model=schemas.TradeDelete)
def delete_trade(
        *,
        db: Session = Depends(get_db),
        trade_uid: int,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Delete an trade.
    """
    trade = crud.trade.get(db, uid=trade_uid)
    if not trade:
        raise HTTPException(
            status_code=404,
            detail="This trade does not exist in the system",
        )
    trade = crud.trade.remove(db, uid=trade_uid)
    trade.date = str(trade.date)
    return trade