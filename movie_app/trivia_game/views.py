from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Question, Game, Player
from .game_logic.game import TriviaGame
from .game_logic.redis_helpers import start_player_turn, is_player_turn_active


@require_http_methods(["POST"])
def start_game(request):
    # Create two players and a new game
    player1 = Player.objects.create(name='Player 1')
    player2 = Player.objects.create(name='Player 2')

    game = Game.objects.create(player1=player1, player2=player2)

    # Initialize the TriviaGame and start it
    trivia_game = TriviaGame(game_id=game.id)
    trivia_game.start_game()

    return JsonResponse({"message": "Game started!", "game_id": game.id})


@require_http_methods(["GET"])
def get_question(request):
    game_id = request.GET.get('game_id')
    game = Game.objects.get(id=game_id)

    # Fetch the current question from the game state
    trivia_game = TriviaGame(game_id=game.id)
    current_round = trivia_game.state['current_round']

    # Get a question from the DB for this round
    question = Question.objects.all()[current_round - 1]

    return JsonResponse({
        "question": question.question_text,
        "options": question.options,
        "round": current_round,
    })


@require_http_methods(["POST"])
def submit_answer(request):
    game_id = request.POST.get('game_id')
    player_id = request.POST.get('player_id')
    answer = int(request.POST.get('answer'))  # Answer index submitted by the player

    game = Game.objects.get(id=game_id)
    trivia_game = TriviaGame(game_id=game.id)

    # Process the player's answer and update the game state
    trivia_game.process_answer(player_id, answer)

    return JsonResponse({"message": "Answer submitted!", "player_id": player_id})


@require_http_methods(["GET"])
def get_game_status(request):
    game_id = request.GET.get('game_id')
    game = Game.objects.get(id=game_id)
    trivia_game = TriviaGame(game_id=game_id)

    # Return current game state (scores, current round)
    return JsonResponse({
        "current_round": trivia_game.state['current_round'],
        "player1_score": trivia_game.state['player1_score'],
        "player2_score": trivia_game.state['player2_score'],
        "is_active": game.is_active,
    })
