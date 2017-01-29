from presidency.models import *

error = Error("scheduler test")
db.session.add(error)
db.session.commit()