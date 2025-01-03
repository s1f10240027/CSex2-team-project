from django.db import models
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
import os

#アイコンのファイル名の編集
def user_icon_upload_to(instance, _):
    user_id = instance.id 
    email = instance.email.split('@')[0]
    return f"user_icons/user_{user_id}_{email}.jpg" 

# 同名のファイルの上書き
class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(self.path(name)) 
        return name

# 1ゲームの管理
class GameSession(models.Model):
    session_id = models.IntegerField(unique=True)               # 乱数(リザルトで非ログインの人も登録可にするために)
    current_question = models.IntegerField(default=0)           # 終了問題数
    correct = models.IntegerField(default=0)                    # 正解数
    answer_times = models.JSONField(default=list)               # 回答時間
    max_streak = models.IntegerField(default=0)                 # 最高連続正解数
    streak = models.IntegerField(default=0)                     # 現在の連続正解数
    genre = models.CharField(max_length=100, default="All")     # ジャンル

# アカウントデータ
class Account(models.Model):
    username = models.CharField(max_length=10) 
    email = models.EmailField() 
    password = models.CharField(max_length=255)
    best_score = models.FloatField(default=0)
    recent_score = models.FloatField(default=0)
    correct_musics = models.JSONField(default=list)
    userIcon = models.ImageField(upload_to=user_icon_upload_to, storage=OverwriteStorage(), null=True, blank=True)
    first_login = models.DateTimeField(default=timezone.now) 
    last_login = models.DateTimeField(default=timezone.now) 

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save()

