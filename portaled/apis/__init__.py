from fastapi import APIRouter
from .user import user_apis
from .profile import profile_apis
from .post import post_apis
from .comment import comment_apis
from .event import event_apis
from .document import document_apis
from .category import category_apis
from .institution import institution_apis
from .grade import grade_apis
from .announcement import announcement_apis


apis_router = APIRouter(prefix="/apis")
apis_router.include_router(announcement_apis)
apis_router.include_router(category_apis)
apis_router.include_router(comment_apis)
apis_router.include_router(document_apis)
apis_router.include_router(event_apis)
apis_router.include_router(grade_apis)
apis_router.include_router(institution_apis)
apis_router.include_router(post_apis)
apis_router.include_router(profile_apis)
apis_router.include_router(user_apis)
