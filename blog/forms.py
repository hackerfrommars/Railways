from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField
from .models import Post, Comment
from django.conf import settings
from django.utils.translation import ugettext as _
import json
import urllib
import urllib.request as urllib2

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        captcha = NoReCaptchaField()
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

    # def __init__(self, *args, **kwargs):
    #     # make the request object available to the form object
    #     self.request = kwargs.pop('request', None)
    #     super(CommentForm, self).__init__(*args, **kwargs)
    #
    # def clean(self):
    #     super(CommentForm, self).clean()
    #
    #     # test the google recaptcha
    #     url = "https://www.google.com/recaptcha/api/siteverify"
    #     values = {
    #         'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
    #         'response': self.request.POST.get(u'g-recaptcha-response', None),
    #         'remoteip': self.request.META.get("REMOTE_ADDR", None),
    #     }
    #     data = urllib.parse.urlencode(values)
    #     req = urllib2.Request(url, data)
    #     response = urllib2.urlopen(req)
    #     result = json.loads(response.read())
    #
    #     # result["success"] will be True on a success
    #     if not result["success"]:
    #         raise forms.ValidationError(_(u'Only humans are allowed to submit this form.'))
    #
    #     return self.cleaned_data
