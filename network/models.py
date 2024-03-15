from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    

class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    message = models.TextField(max_length=250)
    timeStamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.author} posted: {self.message}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="User_who_is_following")
    followedBy = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="User_who_is_being_followed")

    def __str__(self):
        return f"{self.user} is followed by {self.followedBy}"

class Like(models.Model):
    post_Liked = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="Post_liked")
    likedBy = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, related_name="User_who_liked_the_post")

    def __str__(self):
        return f"{self.likedBy} liked: {self.post_Liked}"