from .redis_helpers import get_game_state, update_game_state

class TriviaGame:
    def __init__(self, game_id):
        self.game_id = game_id
        self.state = get_game_state(game_id)

    def start_game(self):
        initial_state = {
            'current_round': 1,
            'player1_score': 0,
            'player2_score': 0,
            'current_question': None
        }
        update_game_state(self.game_id, initial_state)

    def ask_question(self, question):
        current_question = {
            'question': question.question_text,
            'options': question.options,
            'answer': question.correct_option
        }
        self.state['current_question'] = current_question
        update_game_state(self.game_id, self.state)
        return current_question

    def process_answer(self, player_id, answer):
        correct_answer = self.state['current_question']['answer']
        if answer == correct_answer:
            self.state[f'player{player_id}_score'] += 1
        update_game_state(self.game_id, self.state)
