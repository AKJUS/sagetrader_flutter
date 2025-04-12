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


@router.get("/trading-plan", response_model=schemas.TradingPlanPaginated)
def read_trading_plans(
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
    Retrieve trading plans.
    """
    t_plans = crud.trading_plan.get_paginated_multi(
        db, 
        request=request,
        page=page, 
        size=size, 
        owner_uid=current_user.uid,
        shared=shared,
        sort_on=sort_on,        
        sort_order=sort_order
    )
    return t_plans


@router.post("/trading-plan", response_model=schemas.TradingPlan)
def create_trading_plan(
        *,
        db: Session = Depends(get_db),
        plan_in: schemas.TradingPlanCreate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Create new trading plan.
    """
    t_plan = crud.trading_plan.get_by_name_owner(db, name=plan_in.name, owner_uid=current_user.uid)
    if t_plan:
        raise HTTPException(
            status_code=400,
            detail="A trading plan with this name already exists",
        )
    plan_in.owner_uid = current_user.uid
    trading_plan = crud.trading_plan.create(db, obj_in=plan_in)
    return trading_plan


@router.put("/trading-plan/{plan_uid}", response_model=schemas.TradingPlan)
def update_trading_plan(
        *,
        db: Session = Depends(get_db),
        plan_uid: int,
        plan_in: schemas.TradingPlanUpdate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Update an trading_plan.
    """
    trading_plan = crud.trading_plan.get(db, uid=plan_uid)
    if not trading_plan:
        raise HTTPException(
            status_code=404,
            detail="This trading_plan does not exist in the system",
        )
    trading_plan = crud.trading_plan.update(db, db_obj=trading_plan, obj_in=plan_in)
    return trading_plan


@router.delete("/trading-plan/{plan_uid}", response_model=schemas.TradingPlanDelete)
def delete_trading_plan(
        *,
        db: Session = Depends(get_db),
        plan_uid: int,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Delete an trading_plan.
    """
    trading_plan = crud.trading_plan.get(db, uid=plan_uid)
    if not trading_plan:
        raise HTTPException(
            status_code=404,
            detail="This trading_plan does not exist in the system",
        )
    trading_plan = crud.trading_plan.remove(db, uid=plan_uid)
    return trading_plan
