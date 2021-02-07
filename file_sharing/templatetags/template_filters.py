from django import template
from file_sharing.models import FilePost, FileSharing, FileComment


register = template.Library()

@register.filter
def can_comment_check(document, user):

    if document.owner == user:
        return True

    shared = document.filesharing_set.filter(shared_user = user, permission = 1).first()
    if shared == None:
        return False
    return True
