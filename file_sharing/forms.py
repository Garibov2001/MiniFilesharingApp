from file_sharing.models import  FilePost, PERMISSION_CHOICES, FileSharing
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = FilePost
        fields = ['document', 'description']

class FileSharingForm(forms.ModelForm):
    user_info = forms.CharField(required=True)
    permission = forms.ChoiceField(choices=PERMISSION_CHOICES, widget=forms.Select(),required=True)
    class Meta:
        model = FileSharing
        fields = ['user_info', 'permission']