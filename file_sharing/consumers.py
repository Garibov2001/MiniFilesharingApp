import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
from file_sharing.models import FileComment, FilePost, FileSharing
from django.shortcuts import get_object_or_404

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['file_id']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    #Userdan gelen message burdadir
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json["post_type"] == "add_comment" :
            result = self.add_comment(self.scope["user"], text_data_json["message"], text_data_json["file_id"])
        elif text_data_json["post_type"] == "edit_comment" :
            result = self.edit_comment(self.scope["user"], text_data_json["message"], text_data_json["comment_id"], text_data_json["file_id"])
        elif text_data_json["post_type"] == "remove_comment" :
            result = self.remove_comment(self.scope["user"], text_data_json["comment_id"], text_data_json["file_id"])

        result['type'] = 'chat_message'
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, result)

    # Receive message from room group
    def chat_message(self, event):

        if (event["post_type"] == "add_comment"):
            self.send(text_data=json.dumps({
                'post_type': event["post_type"],
                'message': event["message"],
                'user' : event["user"].username,
                'comment_date' : event["comment_date"].strftime("%d.%m.%Y"),
                'comment_id' : event["comment_id"],
            }))

        elif (event["post_type"] == "edit_comment"):
            self.send(text_data=json.dumps({
                'post_type': event["post_type"],
                'message': event["message"],
                'user' : event["user"].username,
                'comment_id' : event["comment_id"],
                'file_id' : event["file_id"],
                'comment_date' : event["comment_date"].strftime("%d.%m.%Y"),
            }))

        elif (event["post_type"] == "remove_comment"):
            self.send(text_data=json.dumps({
                'post_type': event["post_type"],
                'comment_id' : event["comment_id"],
            }))

    def edit_comment(self, user, message, comment_id, file_id):
        # document exist or not
        document = get_object_or_404(FilePost, id = file_id)
        # comment exist or not
        comment = get_object_or_404(FileComment, id = comment_id, document = document, comment_owner = user)                

        comment.content = message
        comment.save()

        return {
            'post_type' : 'edit_comment',
            'user' : user,
            'message' : message,
            'comment_date' : comment.comment_date,
            'file_id' : file_id,
            'comment_id' : comment_id,
        }
        
    def add_comment(self, user, message, file_id):
        # document exist or not
        document = get_object_or_404(FilePost, id = file_id)
        # Does user have permission to add comment?

        if not FilePost.objects.filter(id = file_id, owner = user).exists():
            shared_file = get_object_or_404(FileSharing, document = document, shared_user = user, permission = 1)        
        
        comment = FileComment()
        comment.document = document
        comment.comment_owner = user
        comment.content = message
        comment.comment_date = datetime.now()
        new_comment = comment.save()

        return {
            'post_type' : 'add_comment',
            'user' : user,
            'message' : message,
            'comment_date' : comment.comment_date,
            'comment_id' : comment.id
        }

    def remove_comment(self, user, comment_id, file_id):
         # document exist or not
        document = get_object_or_404(FilePost, id = file_id)
        # comment exist or not    
        comment = get_object_or_404(FileComment, id = comment_id)

        if (user == document.owner):
            comment.delete()
        else:
            shared_file = get_object_or_404(FileSharing, document = document, shared_user = user, permission = 1)
            comment.delete()
        return {
            'post_type' : 'remove_comment',
            'comment_id' : comment_id
        }
        

        comment = get_object_or_404(FileComment, id = comment_id, document = document, comment_owner = user)                

