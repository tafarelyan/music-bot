from pony.orm import *

from database import db


class User(db.Entity):
    user_id = Required(int)
    username = Optional(str)
    first_name = Required(str)
    last_name = Optional(str)
    title = Required(str)
    video_url = Required(str)

