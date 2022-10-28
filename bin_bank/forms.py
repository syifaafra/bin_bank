from django import forms

class FeedbackForm(forms.Form):
    feedback = forms.CharField(label="Comment", required=True, max_length = 100, widget=forms.Textarea(attrs = {'type' : 'text', 'placeholder': 'Write your feedback'}))
