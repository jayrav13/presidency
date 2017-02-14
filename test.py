from presidency.models import *

print( [wh.to_json() for wh in WhiteHouse.query.all()] )