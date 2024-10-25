from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=255)
    options = models.JSONField()  # Store multiple options
    correct_option = models.IntegerField()  # Index of the correct option

    def __str__(self):
        return self.question_text

class Player(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Game(models.Model):
    player1 = models.ForeignKey(Player, related_name='player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='player2', on_delete=models.CASCADE)
    current_round = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Game between {self.player1.name} and {self.player2.name}"
