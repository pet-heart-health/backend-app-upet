from fastapi import APIRouter, Depends, status
from config.db import get_db

from routes.user import endpoint 
from fastapi import HTTPException

from schemas.review import ReviewSchemaGet, ReviewSchemaPost
from services.reviewService import ReviewService

reviews = APIRouter()
tag = "Reviews"
endpoint = "/reviews"

@reviews.post(endpoint +"/{petowner_id}", response_model=ReviewSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_review(petowner_id: int, review: ReviewSchemaPost, db = Depends(get_db)):
    return ReviewService.create_new_review(petowner_id, review, db)

@reviews.get(endpoint, response_model=list[ReviewSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_reviews(db = Depends(get_db)):
    return ReviewService.get_all_reviews(db)

