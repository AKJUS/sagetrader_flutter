from typing import Optional, List, ForwardRef, Any
from datetime import datetime
from pydantic import BaseModel

from mspt.apps.users import schemas as user_schemas


class BasePaginated(BaseModel):
    count: int
    page: int
    pages: int
    size: int
    next_url: Optional[str] = None
    prev_url: Optional[str] = None


#
# ............................................ Instrument Schemas
#
class InstrumentBase(BaseModel):
    name: str
    owner_uid: Optional[int]
    public: bool = False
    

class InstrumentInDBBase(InstrumentBase):
    uid: int

    class Config:
        orm_mode = True
        
class Instrument(InstrumentInDBBase):
    owner: user_schemas.User

class InstrumentUpdate(Instrument):
    name: Optional[str] = None
    owner: Optional[user_schemas.User] = None

class InstrumentCreate(InstrumentBase):
    pass

class InstrumentDelete(InstrumentInDBBase):
    pass
    

class InstrumentPaginated(BasePaginated):
    items: List[Instrument]

#
# ............................................ Strategy Schemas
#
class StrategyBase(BaseModel):
    name: str
    description: str
    owner_uid: Optional[int]
    public: bool = False


class StrategyInDBBase(StrategyBase):
    uid: int

    class Config:
        orm_mode = True

class Strategy(StrategyInDBBase):
    owner: user_schemas.User

class StrategyUpdate(Strategy):
    name: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[user_schemas.User] = None

class StrategyCreate(StrategyBase):
    pass

class StrategyDelete(StrategyInDBBase):
    pass

class StrategyPlusStats(Strategy):
    total_trades: int
    won_trades: int
    lost_trades: int
    
class StrategyPlusStatsPaginated(BasePaginated):
    items: List[StrategyPlusStats]

#
# ............................................ StrategyImage Schemas
#
class StrategyImageBase(BaseModel):
    strategy_uid: int
    strategy: Strategy
    alt: str
    location: str
    # image: bytes

class StrategyImage(StrategyImageBase):
    uid: int

    class Config:
        orm_mode = True

class StrategyImageLocation(BaseModel):
    uid: int
    strategy_uid: int
    strategy: Strategy
    alt: str
    location: str

    class Config:
        orm_mode = True

class StrategyImageUpdate(StrategyImage):
    strategy: Optional[Strategy] = None
    strategy_uid: Optional[int] = None
    alt: Optional[str] = None
    location: Optional[str] = None
    # image: Optional[bytes] = None

class StrategyImageCreate(StrategyImageBase):
    strategy: Optional[Strategy] = None


#
# ............................................ Style Schemas
#
class StyleBase(BaseModel):
    name: str
    description: str
    owner_uid: Optional[int] = None
    public: bool = False

class StyleInDBBase(StyleBase):
    uid: int

    class Config:
        orm_mode = True
        
class Style(StyleInDBBase):
    owner: Optional[user_schemas.User]

class StyleUpdate(Style):
    name: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[user_schemas.User] = None

class StyleCreate(StyleBase):
    pass

class StyleDelete(StyleInDBBase):
    pass


#
# ............................................ Trade Schemas
#
class TradeBase(BaseModel):
    owner_uid: Optional[int] = None
    public: Optional[bool] = False
    instrument_uid: Optional[int] = None
    strategy_uid: Optional[int] = None
    position: Optional[bool] = True
    outcome: Optional[bool] = True
    status: Optional[bool] = True
    pips: Optional[int] = None
    rr: Optional[float] = None
    style_uid: Optional[int] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    sl: Optional[int] = None
    tp: Optional[int] = None
    tp_reached: Optional[bool] = False
    tp_exceeded: Optional[bool] = False
    full_stop: Optional[bool] = False
    entry_price: Optional[float] = None
    sl_price: Optional[float] = None
    tp_price: Optional[float] = None
    scaled_in: Optional[bool] = False
    scaled_out: Optional[bool] = False
    correlated_position: Optional[bool] = False


class TradeInDBBase(TradeBase):
    uid: int
    instrument: Instrument
    strategy: Strategy
    style: Style

    class Config:
        orm_mode = True

class Trade(TradeInDBBase):
    owner: user_schemas.User

class TradeUpdate(TradeBase):
    uid: int

class TradeCreate(TradeBase):
    pass

class TradeDelete(TradeBase):
     uid: int
     
class TradePaginated(BasePaginated):
    items: List[Trade]

#
# ............................................ TradeImage Schemas
#
class TradeImageBase(BaseModel):
    trade_uid: int
    trade: Trade
    alt: str
    location: str
    # image: bytes

class TradeImage(TradeImageBase):
    uid: int

    class Config:
        orm_mode = True

class TradeImageLocation(BaseModel):
    uid: int
    trade_uid: int
    trade: Trade
    alt: str
    location: str

    class Config:
        orm_mode = True

class TradeImageUpdate(TradeImage):
    trade: Optional[Trade] = None
    trade_uid: Optional[int] = None
    alt: Optional[str] = None
    location: Optional[str] = None
    # image: Optional[bytes] = None

class TradeImageCreate(TradeImageBase):
    trade: Optional[Trade] = None


#
# ............................................ TradingPlan Schemas
#
class TradingPlanBase(BaseModel):
    name: str
    description: str
    owner_uid: Optional[int]
    public: bool = False


class TradingPlanInDBBase(TradingPlanBase):
    uid: int

    class Config:
        orm_mode = True
        
class TradingPlan(TradingPlanInDBBase):
    owner: user_schemas.User

class TradingPlanUpdate(TradingPlan):
    name: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[user_schemas.User] = None

class TradingPlanCreate(TradingPlanBase):
    pass

class TradingPlanDelete(TradingPlanInDBBase):
    pass



class TradingPlanPaginated(BasePaginated):
    items: List[TradingPlan]


#
# ............................................ Tasks/Notes Schemas
#
class TaskBase(BaseModel):
    name: str
    description: str
    owner_uid: Optional[int]
    public: bool = False

class TaskInDBBase(TaskBase):
    uid: int

    class Config:
        orm_mode = True
        
class Task(TaskInDBBase):
    owner: user_schemas.User

class TaskUpdate(Task):
    name: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[user_schemas.User] = None

class TaskCreate(TaskBase):
    pass

class TaskDelete(TaskInDBBase):
    pass

class TaskPaginated(BasePaginated):
    items: List[Task]

#
# ............................................ Study Schemas
#

class StudyBase(BaseModel):
    name: str
    description: str
    owner_uid: Optional[int]
    public: bool = False

class StudyInDBBase(StudyBase):
    uid: int

    class Config:
        orm_mode = True
        
class Study(StudyInDBBase):
    owner: user_schemas.User

class StudyUpdate(Study):
    name: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[user_schemas.User] = None
    # attributes: Optional[List['Attribute']] = []

class StudyCreate(StudyBase):
    # attributes: Optional[List['Attribute']] = []
    pass

class StudyDelete(StudyInDBBase):
    # attributes: Optional[List['Attribute']] = []
    pass


class StudyPaginated(BasePaginated):
    items: List[Study]
    
#
# ............................................ StudyItem Schemas
#
class StudyItemBase(BaseModel):
    description: str
    study_uid: str
    instrument_uid: int
    position: bool
    outcome: bool
    pips: int
    rrr: float
    style_uid: int
    description: str
    date: datetime
    public: bool = False

class StudyItem(StudyItemBase):
    uid: int
    instrument: Instrument
    style: Style

    class Config:
        orm_mode = True

class StudyItemUpdate(StudyItem):
    study_uid: Optional[str] = None
    instrument_uid: Optional[int] = None
    instrument: Optional[Instrument] = None
    position: Optional[bool] = True
    outcome: Optional[bool] = True
    pips: Optional[int] = 0
    rrr: Optional[str] = None
    style_uid: Optional[int] = None
    style: Optional[Style] = None
    description: Optional[str] = None
    date: Optional[datetime] = None

class StudyItemCreate(StudyItemBase):
    pass


class StudyItemPaginated(BasePaginated):
    items: List[StudyItem]

#
# ............................................ StudyItemImage Schemas
#
class StudyItemImageBase(BaseModel):
    study_uid: int
    study: Study
    alt: str
    location: str
    # image: bytes

class StudyItemImage(StudyItemImageBase):
    uid: int

    class Config:
        orm_mode = True

class StudyItemImageLocation(BaseModel):
    uid: int
    study_uid: int
    study: Study
    alt: str
    location: str

    class Config:
        orm_mode = True

class StudyItemImageUpdate(StudyItemImage):
    study: Optional[Strategy] = None
    study_uid: Optional[int] = None
    alt: Optional[str] = None
    location: Optional[str] = None
    # image: Optional[bytes] = None

class StudyItemImageCreate(StudyItemImageBase):
    study: Optional[Strategy] = None


#
# ............................................ Attribute Schemas
#

class AttributeBase(BaseModel):
    name: str
    description: str
    study_uid: str
    public: bool = False

class Attribute(AttributeBase):
    uid: int
    # study: Study
    studyitems: List['StudyItem'] = []

    class Config:
        orm_mode = True

class AttributeUpdate(Attribute):
    name: Optional[str] = None
    description: Optional[str] = None
    study_uid: Optional[str] = None

class AttributeCreate(AttributeBase):
    pass

# GenericImageLocation : AllinOne
class GenericImageLocation(BaseModel):
    uid: int
    study_uid: int
    study: Study
    strategy_uid: int
    strategy: Strategy
    trade_uid: int
    trade: Trade
    alt: str
    location: str


#  ========================================================
#  ====       FowardRef for self-referencing models    ====
#  ========================================================

# ========================================================== # StudyWithAttrs
StudyWithAttrs = ForwardRef('Attribute')

class StudyWithAttrs(Study):
    attributes: List['Attribute'] = []

StudyWithAttrs.update_forward_refs()


# ========================================================== # StudyItemWithAttrs
StudyItemWithAttrs = ForwardRef('Attribute')



class StudyItemWithAttrsPaginated(BasePaginated):
    items: List[StudyItemWithAttrs]


class StudyItemWithAttrs(StudyItem):
    attributes: List['Attribute'] = []

StudyItemWithAttrs.update_forward_refs()

# ========================================================== # StudyItemUpdateWithAttrs
StudyItemUpdateWithAttrs = ForwardRef('Attribute')

class StudyItemUpdateWithAttrs(StudyItemUpdate):
    attributes: Optional[List['Attribute']] = []

StudyItemUpdateWithAttrs.update_forward_refs()

# ========================================================== # StudyItemCreateWithAttrs
StudyItemCreateWithAttrs = ForwardRef('Attribute')

class StudyItemCreateWithAttrs(StudyItemBase):
    attributes: Optional[List['Attribute']] = []

StudyItemCreateWithAttrs.update_forward_refs()