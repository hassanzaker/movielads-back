import redis
from django.core.cache import cache

redis_client = redis.StrictRedis()

def get_game_state(game_id):
    return cache.get(f'game_state_{game_id}')

def update_game_state(game_id, state):
    cache.set(f'game_state_{game_id}', state, timeout=3600)

def start_player_turn(game_id, player_id):
    cache.set(f'player_{player_id}_turn_{game_id}', True, timeout=30)
    redis_client.publish(f'game_{game_id}_channel', f"Player {player_id}'s turn")

def is_player_turn_active(game_id, player_id):
    return cache.get(f'player_{player_id}_turn_{game_id}') is not None

# Redis Pub/Sub logic
def subscribe_to_game_channel(game_id, callback):
    pubsub = redis_client.pubsub()
    pubsub.subscribe(f'game_{game_id}_channel')

    for message in pubsub.listen():
        if message['type'] == 'message':
            callback(message['data'])
