from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    question = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Poll\'s author')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
    
class Choice (models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    choice_content = models.CharField(max_length=250)

    def __str__(self):
        return self.choice_content

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice , on_delete=models.CASCADE, related_name='votes')
    poll = models.ForeignKey(Poll , on_delete=models.CASCADE, related_name='poll')

    class Meta:
        unique_together = ('poll', 'voter')

    def __str__(self):
        return f'{self.voter.username} voted for {self.choice.choice_content}'
