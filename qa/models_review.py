from django.db import models
from martor.models import MartorField

from django.db.models.signals import post_save
from django.dispatch import receiver
from random import choice
from simple_history.models import HistoricalRecords
from django.urls import reverse

from .models import User
from .models_qa import Question, Answer


LOW_QUALITY_CHOICES = [
    ('Looks_OK', 'Looks Ok'),
    ('Edit', 'Edit'),
    ('Recommend_Delete', 'Recommend Delete'),
    ('Recommend_Close', 'Recommend Close'),
    ('Skip', 'Skip'),
]

WHY_LOW_QUALTY = [
    ('Answer_Less_Than_200', 'Answer is Less than 200 Words'),
    ('Question_Less_Than_200', 'Question is Less than 200 Words'),
    ('Comment_As_Answer', 'Comment as Answer'),
]

SUGGEST_CHOICES = [
    ('User', 'User'),
    ('Automatic', 'Automatic')
]

class LowQualityPostsCheck(models.Model):
    suggested_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    suggested_through = models.CharField(max_length=30, choices=SUGGEST_CHOICES)
    low_is = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    low_ans_is = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    why_low_quality = models.CharField(max_length=30, choices=WHY_LOW_QUALTY)
    is_completed = models.BooleanField(default=False)

    how_many_votes_on_OK = models.IntegerField(default=0)
    how_many_votes_on_deleteIt = models.IntegerField(default=0)
    how_many_votes_on_close = models.IntegerField(default=0)

    at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "review_lowqualitypostscheck"
        # this is to ignore the existing 'review_lowqualitypostscheck' table when is set to False, 
        # no database table creation or deletion operations will be performed for this model. 
        managed = False
        app_label = 'qa'

    def __str__(self):
        if self.low_is:
            return f"[Q] {self.why_low_quality} - [Q] - {self.low_is.title}"
        else:
            return f"[A] {self.why_low_quality} - [A] - {self.low_ans_is.body}"


class ReviewLowQualityPosts(models.Model):
    reviewers = models.ManyToManyField(User, related_name="reviewers")
    review_of = models.ForeignKey(LowQualityPostsCheck, on_delete=models.CASCADE)
    reviewActions = models.CharField(max_length=30, choices=LOW_QUALITY_CHOICES, blank=True, null=True)
    is_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True)
    is_question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "review_reviewlowqualityposts"
        # this is to ignore the existing 'review_reviewlowqualityposts' table when is set to False, 
        # no database table creation or deletion operations will be performed for this model. 
        managed = False
        app_label = 'qa'

    def __str__(self):
        if self.is_reviewed:
            return f"Reviewed"
        else:
            return f"Pending"