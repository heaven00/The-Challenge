The-Challenge
=============

Social Search Engine : -


--This project must be social (Users must be able to sign up for it, they must have a “feed” of others “posts”. Each user can make “posts” and comment on others' “posts”)

--The authentication must be as strong as possible(use good security measures)
Users can upload files along with their posts. The files can be (PDF, DOC, DOCX) only, others are not allowed. Make sure you use good file checking mechanisms to detect these file types. Don't just check the extension string to decide.
If the user clicks on 'share' for any of their posts, you must make a very short URL (i.e., build a URL shortening service) so that they can share that short URL that redirects to their post (which is now automatically made public).

--Make an admin panel to see the analytics of the entire system. You may display as many analytics criteria as you wish(example-Page Views, Unique visitors, etc..). The more the better.

--Now coming to the search engine - the search engine must do full-text searches and you must rank the results based on some algorithm(example-number of repetitions of search term increases rank). Display each results ranking score next to it.
What does the search engine search for?
 - It performs full text searches on users’ posts text content.(Let's assume that anybody can search for everybody's posts.)
 - People can upload files along with their posts. The search engine must search for text inside the PDF files if any and use that also in the ranking process.(only PDF files, other file types can be ignored)

Going to Django 1.4.x framework for the task.

Lets Break down the problems a little bit :-

BACKEND 

The backend needs to be mongo based so, lets just use mongoengine for the job. 
The structure I am thinking would be Post embeded in User and a listfield 'comments'
in posts and also another embedded list document in Post, File which will have the uploaded files and details like file type, file name included in it.

{
 User
	{
	Post[comments]
	[{File}]
	}
}

Lets start with the workflow.

SIGNUP

The user should be able create his own account using his, username, email, password.
A little email confirmation or email or an email telling the user the account has been created would be good enough and as fas as security is confirmed, i think Django provides a decent security implementing the csrf token and injection protection.


POST ADD/EDIT

A form for adding/editing the posts


SHARING

Sharing has two objectives:- 
	Getting the file accessible from an url
	
	URL-shortening
		For this i think the bitly python api would be fine, though would need to 			create an account for it.

ADMIN PANEL ANALYTICS

For now i will just leave it to that i will be using the django-analytics module, if it will be possible or add another document storing info related to this which is a very bad idea and a very expensive quick fix.

SEARCH ENGINE

For the full text searches i will be using django-haystack as abstraction layer and whoosh as search engine.
I will need to create search indexes for all the Posts and Uploaded files.

	

Lets see how it goes down, 
Cheers :)
