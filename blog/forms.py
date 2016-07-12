from django import forms
# from nocaptcha_recaptcha.fields import NoReCaptchaField
from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.Form):

    class Meta:
        model = Comment
        # captcha = NoReCaptchaField()
        fields = ('author', 'text',)
