import json
import threading
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import redis
import uuid

# Initialize Redis instance
redis_instance = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

rooms = set([str(x) for x in range(1000, 10000)])


class GameRoomConsumer(WebsocketConsumer):

    def connect(self):
        self.room_group_name = None
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            # Reject connection if user is not authenticated
            self.close()
        else:
            self.user_id = str(self.user.id)

            game_rooms = set()
            rooms = redis_instance.lrange('game_rooms', 0, -1)
            found_room = None

            for room in rooms:
                room_info = json.loads(room)
                game_rooms.add(room_info['room_name'])

                if room_info['player_count'] == 1 or self.user_id in room_info['players']:
                    found_room = room_info
                    break

            if found_room:
                if self.user_id in found_room['players']:
                    self.room_group_name = found_room['room_name']
                else:
                    self.room_group_name = found_room['room_name']
                    found_room['player_count'] += 1
                    found_room['players'].append(self.user_id)
                    redis_instance.lset('game_rooms', rooms.index(room), json.dumps(found_room))
            else:
                self.room_group_name = f'room_{self.next_available_room(game_rooms)}'
                new_room = {
                    'room_name': self.room_group_name,
                    'player_count': 1,
                    'players': [self.user_id]
                }
                redis_instance.rpush('game_rooms', json.dumps(new_room))

            # Store initial game state in Redis (e.g., questions and current question index)
            game_state_key = f"{self.room_group_name}_state"
            if not redis_instance.exists(game_state_key):
                initial_state = {
                    'current_question_index': 0,
                    'players_answers': {},
                    'players_scores': {}
                }
                redis_instance.set(game_state_key, json.dumps(initial_state))

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()

            if found_room and found_room['player_count'] == 2:
                self.players = found_room['players']
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'start_game',
                    }
                )

    def disconnect(self, close_code):
        if close_code == 1006:
            print(f"User {self.user} disconnected with close code {close_code}")
            return

        rooms = redis_instance.lrange('game_rooms', 0, -1)
        for room in rooms:
            room_info = json.loads(room)
            if room_info['room_name'] == self.room_group_name:
                if close_code == 2531:
                    redis_instance.lrem('game_rooms', 0, json.dumps(room_info))
                    return
                if room_info['player_count'] == 2:
                    room_info['players'].remove(self.user_id)
                    room_info['player_count'] -= 1
                    redis_instance.lset('game_rooms', rooms.index(room), json.dumps(room_info))
                    # Notify the other player that this player has left
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'player_left',
                        }
                    )
                else:
                    if self.user_id in room_info['players']:
                        redis_instance.lrem('game_rooms', 0, json.dumps(room_info))
                break

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def player_left(self, event):
        self.send(text_data=json.dumps({
            'message': 'Player Left',
        }))

    def start_game(self, event):
        # List of questions
        self.questions = [
            {"question": "What is the largest planet in our solar system?",
             "options": ["Earth", "Mars", "Jupiter", "Saturn"],
             "correct": "Jupiter",
             "score": 10},

            {"question": "Which country is known as the Land of the Rising Sun?",
             "options": ["China", "Japan", "South Korea", "India"],
             "correct": "Japan",
             "score": 10},

            {"question": "What is the chemical symbol for gold?",
             "options": ["Au", "Ag", "Fe", "Pb"],
             "correct": "Au",
             "score": 10},

            {"question": "Who wrote 'Romeo and Juliet'?",
             "options": ["Charles Dickens", "Jane Austen", "William Shakespeare", "Mark Twain"],
             "correct": "William Shakespeare",
             "score": 10},

            {"question": "What is the capital of Australia?",
             "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
             "correct": "Canberra",
             "score": 10},

            {"question": "How many continents are there?",
             "options": ["5", "6", "7", "8"],
             "correct": "7",
             "score": 10},

            {"question": "What is the hardest natural substance on Earth?",
             "options": ["Iron", "Diamond", "Graphite", "Gold"],
             "correct": "Diamond",
             "score": 10},

            {"question": "Which ocean is the largest?",
             "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
             "correct": "Pacific Ocean",
             "score": 10},

            {"question": "What is the tallest mountain in the world?",
             "options": ["Mount Kilimanjaro", "Mount Everest", "K2", "Denali"],
             "correct": "Mount Everest",
             "score": 10},

            {"question": "Which element is needed for combustion to occur?",
             "options": ["Hydrogen", "Carbon", "Oxygen", "Nitrogen"],
             "correct": "Oxygen",
             "score": 10},
        ]
        self.send_question_to_users()

    def send_question_to_users(self):
        # Retrieve the current game state from Redis
        game_state_key = f"{self.room_group_name}_state"
        game_state = json.loads(redis_instance.get(game_state_key))

        current_question_index = game_state['current_question_index']
        current_question = self.questions[current_question_index]

        # Reset answers for the new question
        print(game_state)
        game_state['players_answers'] = {}
        redis_instance.set(game_state_key, json.dumps(game_state))

        # Broadcast the current question to both players
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_question',
                'question': current_question['question'],
                'options': current_question['options'],
            }
        )

        # # Start a 30-second timer for the question
        # self.timer = threading.Timer(30.0, self.collect_answers_and_send_result)
        # self.timer.start()

    def send_question(self, event):
        # Send the question to both players
        self.send(text_data=json.dumps({
            'message': 'New Question',
            'question': event['question'],
            'options': event['options'],
        }))

    def receive(self, text_data):
        data = json.loads(text_data)
        print("YY", data)
        if data['type'] == 'leave_game':
            self.disconnect(close_code=1000)
        elif data['type'] == 'answer':
            user_id = str(self.user.id)

            # Retrieve the current game state from Redis
            game_state_key = f"{self.room_group_name}_state"
            game_state = json.loads(redis_instance.get(game_state_key))

            # Store the player's answer in the Redis state
            game_state['players_answers'][user_id] = data['answer']
            redis_instance.set(game_state_key, json.dumps(game_state))
            # print(user_id, data['answer'])
            # If both users have answered, process the answers immediately
            if len(game_state['players_answers']) == 2:
                # print("KK", self.timer)
                # if hasattr(self, 'timer') and self.timer is not None:
                #     print("uu", self.timer)
                #     # Cancel the timer since both players have answered
                #     self.timer.cancel()
                self.collect_answers_and_send_result(data, user_id)

    def collect_answers_and_send_result(self, data, user_id):
        # Retrieve the current game state from Redis
        game_state_key = f"{self.room_group_name}_state"
        game_state = json.loads(redis_instance.get(game_state_key))

        players_answers = game_state['players_answers']
        current_question_index = game_state['current_question_index']
        correct_answer = self.questions[current_question_index]['correct']
        question_score = self.questions[current_question_index]['score']
        score = 0
        if correct_answer == players_answers[user_id]:
            score = data['remaining_time'] + question_score

        if user_id in game_state['players_scores']:
            game_state['players_scores'][user_id] += score
        else:
            game_state['players_scores'][user_id] = score

        # Send the results to both players
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_result',
                'correct_answer': correct_answer,
                'players_answers': players_answers,
                'players_scores': game_state['players_scores']
            }
        )

        # Move to the next question or end the game
        game_state['current_question_index'] += 1
        redis_instance.set(game_state_key, json.dumps(game_state))

        if game_state['current_question_index'] < len(self.questions):
            self.send_question_to_users()  # Send the next question
        else:
            self.end_game()  # If no more questions, end the game

    def send_result(self, event):
        # Send results to both players
        self.send(text_data=json.dumps({
            'message': 'Result',
            'correct_answer': event['correct_answer'],
            'players_answers': event['players_answers'],
            'players_scores': event['players_scores']
        }))

    def end_game(self):
        # Notify both players that the game has ended
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_end_message',
                'message': 'The game has ended!',
            }
        )
        # Clean up Redis state
        game_state_key = f"{self.room_group_name}_state"
        redis_instance.delete(game_state_key)
        self.disconnect(close_code=2531)

    def send_end_message(self, event):
        self.send(text_data=json.dumps({
            'message': event['message'],
        }))

    def next_available_room(self, used_rooms):
        available_rooms = rooms - used_rooms
        return available_rooms.pop()
