


function EditCommentClick(comment_id){
    comment = $(`[label=comment-${comment_id}]`)
    message = comment.find(".article-content").text()
    edit_section = $('[label=comment-edit-section]')    
    post_section = $('[label=comment-post-section]')
        
    edit_section.show();
    post_section.hide();

    edit_section.find('[label=content-body]').val(message);
    edit_section.find('[label=comment-id]').val(comment_id); 

    edit_section[0].scrollIntoView({ behavior: "smooth" });
}


function EditCommentPost(){
    edit_section = $('[label=comment-edit-section]')    
    message = edit_section.find('[label=content-body]').val();
    comment_id = edit_section.find('[label=comment-id]').val(); 
    file_id = $('#file_id').val()  

    //Send to websocket    
    chatSocket.send(JSON.stringify({
        'post_type' : 'edit_comment',
        'message': message,
        'comment_id' : comment_id,
        'file_id' : file_id
    }));
}


function EditCommentApply(data){
    edit_section = $('[label=comment-edit-section]')    
    post_section = $('[label=comment-post-section]')
    comment = $(`[label=comment-${data.comment_id}]`);
    comment.find(".article-content").html(data.message);
    $('html,body').animate({scrollTop: comment.offset().top - 100},'slow');
    
    edit_section.hide();
    post_section.show();
}


function RemoveCommentPost(comment_id){
    file_id = $('#file_id').val()  
    //Send to websocket    
    chatSocket.send(JSON.stringify({
        'post_type' : 'remove_comment',
        'comment_id' : comment_id,
        'file_id' : file_id
    }));
}


function RemoveCommentApply(data){
    comment = $(`[label=comment-${data.comment_id}]`).remove();    
}