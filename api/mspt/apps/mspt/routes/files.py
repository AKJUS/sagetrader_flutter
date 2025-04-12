from typing import List
from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    Form,
)
from sqlalchemy.orm import Session

from mspt.apps.mspt import utils
from mspt.settings.database import get_db
from mspt.utils.create_dirs import resolve_media_dirs_for

router = APIRouter()
db_session = Session()


@router.post("/uploads-handler")
async def handle_file_uploads(
        db: Session = Depends(get_db),
        files: List[UploadFile] = File(...),
        parent: str = Form(...),
        tags: str = Form(...),
        caption: str = Form(...)
    ):
    parent, parent_uid = parent.split('-')
    media_dir = resolve_media_dirs_for(parent)
    images = []

    for _file in files:   
        file_path = media_dir + _file.filename
        resp = await utils.save_or_upload(
            file_path=file_path, 
            img_file=_file, 
            tags=tags,
            caption=caption,
            parent=parent,
            parent_uid=parent_uid,
        )
        utils.persist_image_metadata(
            db=db, 
            parent=parent,
            parent_uid=parent_uid, 
            location=resp.get('url', None),
            public_uid = resp.get('public_uid', None),
            asset_uid = resp.get('asset_uid', None),
            signature = resp.get('signature', None),
            version = resp.get('version', None),
            version_uid = resp.get('version_uid', None)
        )
        images = utils.get_image_response(db=db, parent=parent, parent_uid=parent_uid)
    return images


@router.get("/fetch-files/{parent_uidentifier}")
async def fetch_files(
        *,
        db: Session = Depends(get_db),
        parent_uidentifier: str
    ):
    parent, parent_uid = parent_uidentifier.split('-')
    resolve_media_dirs_for(parent)
    images = utils.get_image_response(db=db, parent=parent, parent_uid=parent_uid)
    return images


@router.delete("/delete-file/{uidentifier}")
async def delete_files(
        *,
        db: Session = Depends(get_db),
        uidentifier: str
    ):
    parent, file_uid = uidentifier.split('-')
    response = utils.delete_images(db=db, parent=parent, file_uid=file_uid)
    return response
