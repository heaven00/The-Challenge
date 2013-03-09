"""All the forms for the controller will be here"""
from django import forms
from mongoengine.django.auth import User


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
        
    def save(self, commit=True):
        user = User.create_user(self.cleaned_data['username'], self.cleaned_data['password2'], self.cleaned_data['email'])
        if commit:
            user.save()
        return user