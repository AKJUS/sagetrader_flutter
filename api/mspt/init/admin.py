import logging, coloredlogs

from mspt.apps.users import crud
from mspt.settings import config
from mspt.apps.users.schemas import UserCreate

coloredlogs.install()
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def create_super_user(db_session):
    logger.info("Check Super User ")

    user = crud.user.get_by_email(db_session, email=config.FIRST_SUPERUSER_EMAIL)
    if not user:
        user_in = UserCreate(
            first_name="System",
            last_name="Administrator",
            email=config.FIRST_SUPERUSER_EMAIL,
            password=config.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db_session, obj_in=user_in)
    else:
        pass
    
    logger.info("SuperUser Check Success")
