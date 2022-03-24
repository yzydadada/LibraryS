from flask import Blueprint

bp = Blueprint('studyroom', __name__)

from app.studyroom import routes