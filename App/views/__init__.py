# blue prints are imported 
# explicitly instead of using *
from .auth import auth_views
from .game import game_views
from .howtoplay import howtoplay_views
from .index import index_views
from .user import user_views
from .user_history import user_history_views
from .user_search import user_search_views


views = [
    auth_views,
    game_views,
    howtoplay_views,
    index_views,
    user_views,
    user_history_views,
    user_search_views]
# blueprints must be added to this list