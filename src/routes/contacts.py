from typing import List, Optional
from fastapi import Path, Depends, HTTPException, Query, status, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter
from src.database.db import get_db
from src.schemas import ContactModel, ContactFavoriteModel, ContactResponse
from src.repository import contacts as rep_contact
from src.services.auth import auth_service
from src.services.role import RoleAccess
from src.database.models import User, Role


router = APIRouter(prefix="/contacts", tags=["contact"])

allowed_operation_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_create = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_update = RoleAccess([Role.admin, Role.moderator])
allowed_operation_remove = RoleAccess([Role.admin])

@router.get("/all", response_model = List[ContactResponse], dependencies=[Depends(allowed_operation_update)], summary="Get all contacts if you are admin or moderator ")
async def get_all_contact(
        skip: int = 0,
        limit: int = Query(default=10, le=100, ge=10),
        favorite: bool = None,
        db: Session = Depends(get_db), current_user: User = Depends(auth_service.token_manager.get_current_user)):
    contacts = await rep_contact.get_all_contacts(db=db, skip=skip, limit=limit, favorite=favorite)
    return contacts

@router.get("", response_model = List[ContactResponse], dependencies=[Depends(allowed_operation_get)], summary="Get contacts only for user")
async def get_contact(
        skip: int = 0,
        limit: int = Query(default=10, le=100, ge=10),
        favorite: bool = None,
        db: Session = Depends(get_db), current_user: User = Depends(auth_service.token_manager.get_current_user)):
    contacts = await rep_contact.get_contacts(db=db, skip=skip, user=current_user, limit=limit, favorite=favorite)
    return contacts



@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(allowed_operation_get)])
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.token_manager.get_current_user)):
    contact = await rep_contact.get_contact_by_id(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.post("",   response_model=ContactResponse, status_code=status.HTTP_201_CREATED, dependencies=[
        Depends(allowed_operation_create),
        Depends(RateLimiter(times=2, seconds=5)),
    ], description="Two attempt on 5 second")
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.token_manager.get_current_user)):
    contact = await rep_contact.get_contact_by_email(body.email, db, current_user)
    if contact:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Email is exist!"
        )
    try:
        contact = await rep_contact.create(body, db, current_user)
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_404_INVALID_REQUEST, detail=f"Error: {err}"
        )
    return contact


@router.put("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(allowed_operation_update)])
async def update_contact(
        body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.token_manager.get_current_user)):
    contact = await rep_contact.update(contact_id, body, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.patch("/contact_id/favorite", response_model=ContactResponse, dependencies=[Depends(allowed_operation_update)])
async def favorite_update(
        body: ContactFavoriteModel,
        contact_id: int = Path(ge=1),
        db: Session = Depends(get_db), current_user: User = Depends(auth_service.token_manager.get_current_user)
):
    contact = await rep_contact.favorite_update(contact_id, body, db,  current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(allowed_operation_get)])
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.token_manager.get_current_user)):
    contact = await rep_contact.delete(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return None


@router.get("/search_by/{query}", response_model=List[ContactResponse], tags=['search'], summary="Search contacts by name, lastname, email",
            dependencies=[Depends(allowed_operation_get)])
async def search_by(query: Optional[str] = None,
                         db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.token_manager.get_current_user)):
    contacts = await rep_contact.search_contacts(query, db, current_user)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")

    return contacts


@router.get("/search/birtdays", response_model=List[ContactResponse], dependencies=[Depends(allowed_operation_get)])
async def search_contacts(
        days: int = Query(default=7, le=30, ge=1),
        skip: int = 0,
        limit: int = Query(default=10, le=30, ge=1),
        db: Session = Depends(get_db), current_user: User = Depends(auth_service.token_manager.get_current_user)
):
    contacts = None
    if days:
        par = {
            "days": days,
            "skip": skip,
            "limit": limit,
        }
        contacts = await rep_contact.search_birthday(par, db, current_user)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No contacts found")
    return contacts


