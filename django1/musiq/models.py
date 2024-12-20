from django.db import models

class GameSession(models.Model):
    session_id = models.IntegerField(unique=True)      #乱数(リザルトで非ログインの人も登録可にするために)
    current_question = models.IntegerField(default=0)         # 終了問題数
    correct = models.IntegerField(default=0)        # 正解数
    answer_times = models.JSONField(default=list)   # 回答時間
    max_streak = models.IntegerField(default=0)     # 最高連続正解数
    streak = models.IntegerField(default=0)         # 現在の連続正解数
    genre = models.CharField(max_length=100, default="All")
