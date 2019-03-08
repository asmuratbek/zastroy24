from django import forms
from .models import Feedback, Reviews, AffiliateFeedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ('is_read',)



class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        exclude = ('is_active', 'created_at')


class AffiliateFeedbackForm(forms.ModelForm):
    class Meta:
        model = AffiliateFeedback
        exclude = ('is_read', 'created_at')
