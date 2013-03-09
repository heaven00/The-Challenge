"""All the forms for the controller will be here"""
from django import forms
from mongoengine.django.auth import User, MongoEngineBackend
from functions import hybrid_authentication
from SocialSearch.settings import ALLOWED_FILE_TYPES, UPLOAD_MAX_SIZE
from document import Post
from mongoengine.django.storage import GridFSStorage
fs = GridFSStorage()


#Rewriting Django UserCreationForm to support MongoEngine User
class UserCreationForm(forms.Form):
    """
    A form that creates a user from the given username and
    password.
    """
    error_messages = {
        'duplicate_username':"A user with that username already exists.",
        'password_mismatch': "The two password fields didn't match.",
        'email_exists':"User with Email address already exists"
    }
    username = forms.RegexField(label="Username", max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text = "Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only.",
        error_messages = {
            'invalid': "This value may contain only letters, numbers and "
                         "@/./+/-/_ characters."})
    password1 = forms.CharField(label="Password",
        widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
        widget=forms.PasswordInput,
        help_text = "Enter the same password as above, for verification.")
    email = forms.EmailField(label="email",
        help_text = "Enter a Valid email id")

    def clean_username(self):
        username = self.cleaned_data["username"]
        user = User.objects(username=username)
        if len(user) == 0:
            print username
            return username
        else:
            raise forms.ValidationError(self.error_messages['duplicate_username'])
    
    def clean_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        else:
            return password1
        
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects(email=email)
        if len(user) == 0:
            return email
        else: 
            raise forms.ValidationError(self.error_messages['email_exists'])
 
 #!! TODO IF TIME ADD MAIL NOTIFICATION OF ACCOUNT CREATION       
    def save(self, commit=True):
        user = User.create_user(self.cleaned_data['username'], self.cleaned_data['password2'], self.cleaned_data['email'])
        if commit:
            user.save()
        return user
    
    
class AuthenticationForm(forms.Form):
    """
    A form that authenticates the given username/email and password combination
    """
    error_messages = {
        'Incorrect_credentials':"Please enter a correct username and password.",
        'Missing_Credential':"Username/Password missing"
                  }
    
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput)
    
    
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if username and password:
            user = hybrid_authentication(username, password)
            if user is None:
                raise forms.ValidationError(self.error_messages['Incorrect_credentials'])
            else:
                return user
        else:
            raise forms.ValidationError(self.error_messages['Missing_Credential']) 
        
        
        
class PostCreationForm(forms.Form):
    """
    A form to create New Posts for a given User.
    """
    error_messages = {'Login_required':"You need to login First",
                      'File_type':"You can upload only Doc/Docx/PDF files",
                      'User_required':"You must be a user to create a Post",
                      'File_size_exceeded':"The File Size Limit has exceeded",
                      }
    
    user = forms.CharField(label="User", 
                           widget=forms.HiddenInput)
    body = forms.CharField(label="Content",
                          widget=forms.Textarea)    
    file = forms.FileField(label="File")    
    def clean_user(self):
        username = self.cleaned_data["user"]
        if username:
            user = User.objects(username=username)
            if len(user) == 0:
                raise forms.ValidationError(self.error_messages['Login_required']) 
            else:
                return user
        else:
            raise forms.ValidationError(self.error_messages['User_required'])
    
    #! TODO Verify uploaded file and test file uploading
    def clean_file(self):
        file = self.cleaned_data["file"]
        if file:
            content_type = file.content_type.split('/')[0]
            print content_type
            print file.content_type
            if content_type not in ALLOWED_FILE_TYPES:
                raise forms.ValidationError(self.error_messages['File_type'])
            if len(file.name.split('.')) == 1:
                raise forms.ValidationError(self.error_messages['File_type'])
            if file._size > UPLOAD_MAX_SIZE:
                raise forms.ValidationError(self.error_messages['File_size_exceeded'])
            return file
        
    
    def save(self, commit=True):
        post = Post()
        post.user = self.cleaned_data['user']
        post.body = self.cleaned_data['body']
        fs.save(self.cleaned_data['file'].name, self.cleaned_data['file'])
        post.file = self.cleaned_data['file']
        post.save()
        
        
class CommentForm(forms.Form):
    """
    A form that accepts comments
    """
    body = forms.CharField(label='body',
                              widget=forms.Textarea)