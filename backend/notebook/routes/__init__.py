"""
Copyright © retnikt <_@retnikt.uk> 2020
This software is licensed under the MIT Licence: https://opensource.org/licenses/MIT
"""
from fastapi import APIRouter

from .oauth2 import router as auth
from .profile import router as profile
from .password import router as password

router = APIRouter()
router.include_router(auth, prefix="/oauth2")
router.include_router(profile, prefix="/profile")
router.include_router(password, prefix="/password")
