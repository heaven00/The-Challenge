"""Will be adding all the functions that i will be using in the controller here"""
from mongoengine.django.auth import User
from document import Comment, Post
from django.core.validators import email_re
from mongoengine.django.storage import GridFSStorage
fs = GridFSStorage()

def hybrid_authentication(username=None,password=None):
    try:
        if email_re.search(username):
            user = User.objects(email=username).first()
        else:
            user = User.objects(username=username).first()
        if len(user) != 0:
            if password and user.check_password(password):
                    return user
            else:
                return None
        else:
            return None
    except:
        return None
    
def add_comment(post_id,body,user):
    try:
        post = Post.objects(post_id=post_id).first()
        print body
        comment = Comment(body=body,user=User.objects(username=user).first())
        print comment.body
        post.comment.append(comment)
        post.save()
        return post
    except Exception,error:
        print "function error %s"%error
        return None
    
def add_post(user,body,file=None):
    try:
        post = Post()
        post.body = body
        post.user = User.objects(username=user).first()
        print file
        if file:
            post.file = file
            fs.save(post.file,file.read())
        post.save()
        return post
    except Exception,error:
        print error
        return None