from django import forms

from .models import Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = {"content"}
        widgets = {
            "content": forms.Textarea(attrs={"placeholder": "今どうしてる？"}),
        }
        labels = {"content": ""}
