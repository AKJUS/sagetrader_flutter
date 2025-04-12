from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session


from mspt.apps.users import models as user_models
from mspt.settings.database import get_db
from mspt.settings.security import (
    get_current_active_user
)

router = APIRouter()
db_session = Session()


@router.get("/peformance-measures")
def trade_stats(
        db: Session = Depends(get_db),
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Calculate Trading Statistics.
    """

    # 1. Stategy Win Rates
    # overal peformance
    # by pair
    # by style
    # by position type

    # 2. RiskReward
    # overal peformance
    # by pair
    # by style
    # by strategy

    # 3. Average Pips Lost/Gained
    # overal peformance
    # by pair
    # by strategy
    # by style

    # 3. Intsrument Peformances
    # overal peformance
    # by strategy
    # by style
    # by position type

    # 2. Other Stats

    return {}
