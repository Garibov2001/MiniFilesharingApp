from django.shortcuts import render, redirect, get_object_or_404
from file_sharing.forms import CommentForm, FileSharingForm
from file_sharing.models import FilePost, FileSharing, PERMISSION_CHOICES, FileComment, UserLog
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods

@login_required
def home(request):
    log = UserLog()
    log.user = request.user
    log.operating_system = request.user_agent.os.family
    log.browser = request.user_agent.browser.family
    log.ip_address = visitor_ip_address(request)
    log.save()


    context = {
        'files': FilePost.objects.filter(owner=request.user)      
    }
    return render(request, 'file_sharing/home.html', context)


@login_required
def homeShared(request):
    context = {
        'shared_files': FileSharing.objects.filter(shared_user=request.user),       
    }
    return render(request, 'file_sharing/home_shared.html', context)


@login_required
def fileAdd(request):     
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES ) 
        if form.is_valid(): 
            file_post = FilePost()
            file_post.document = form.cleaned_data.get('document')
            file_post.description = form.cleaned_data.get('description')
            file_post.owner = request.user
            file_post.save()                 
            return redirect('file-sharing-home')
    else:
        form = CommentForm()           
    return render(request, 'file_sharing/file_add.html', {'form' : form})


@login_required
def fileShare(request, id):    
    #security check (request user have to be owner of file):
    fileObj = get_object_or_404(FilePost, id = id, owner = request.user)    

    if request.method == 'POST':
        form = FileSharingForm(request.POST) 
        if form.is_valid(): 
            user_info = form.cleaned_data.get("user_info")
            permission = form.cleaned_data.get("permission")            
            
            if user_info == request.user.username or user_info == request.user.email:
                messages.error(request, "Siz ozunuze permission vere bilmezsiniz", extra_tags='danger')
            else:
                isUserExist = False
                for user in User.objects.all():
                    if user.username == user_info or user.email == user_info:
                        isUserExist = True
                        try:
                            # Checking for is this files shared with specified user
                            FileSharing.objects.get(document = fileObj, shared_user = user)  
                            messages.error(request, "File artiq bu username ve ya emailde olan sexsle palyasilib", extra_tags='danger')                                                 
                        except FileSharing.DoesNotExist:
                            share_opt = FileSharing()
                            share_opt.document = fileObj
                            share_opt.shared_user = user
                            share_opt.permission = permission
                            share_opt.save()
                            messages.success(request, f"{user.username} ile paylasildi", extra_tags='success')                                               
                if (not isUserExist):
                    messages.error(request, "Daxil etdiyiniz username ve ya email sistemde yoxdur", extra_tags='danger')                                        
    else:
        form = FileSharingForm()
    context = {
        "form" : form,
        "shared_files" :  FileSharing.objects.filter(document = fileObj)
    }
    return render(request, 'file_sharing/share_file.html', context)


@login_required
def fileDetails(request, id):    
    #security check (request user have to be owner of file):

    fileObj = get_object_or_404(FilePost, id = id)   

    if fileObj.owner != request.user:        
        get_object_or_404(FileSharing, document= fileObj, shared_user = request.user)  

    file_comments = FileComment.objects.filter(document = fileObj)
    context = {
        "file" :  fileObj,
        "file_comments" : file_comments 
    }
    return render(request, 'file_sharing/file_details.html', context)

@login_required
@require_http_methods(["POST"]) # It can be delete too
def deleteFileShare(request, file_id, user_id):    
    #security check (request user have to be owner of file):
    fileObj = get_object_or_404(FilePost, id = file_id, owner = request.user) 
    # Chek is user exist or not:
    shared_user = get_object_or_404(User, id = user_id)
    # Check is user shared with file
    shared_file = get_object_or_404(FileSharing, document = fileObj, shared_user = shared_user)
    shared_file.delete()
    messages.success(request, f"{shared_user.username} ile paylasilma dayandirildi", extra_tags='success')    
    return redirect("file-sharing-share-file", id = file_id)


def visitor_ip_address(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip