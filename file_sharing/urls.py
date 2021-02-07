from django.urls import path
from file_sharing import views

urlpatterns = [
    path('', views.home, name='file-sharing-home'),
    path('sharedfiles/', views.homeShared, name='file-sharing-home-shared'),
    path('add/', views.fileAdd, name='file-sharing-add-file'),    
    path('filedetails/<int:id>', views.fileDetails, name='file-sharing-file-details'),
    path('sharefile/<int:id>', views.fileShare, name='file-sharing-share-file'),    
    path('sharefile/<int:file_id>/user/<int:user_id>', views.deleteFileShare, name='file-sharing-share-delete-file'),    
]
