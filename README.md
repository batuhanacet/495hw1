# 495hw1

https://ceng495hw1webservice.onrender.com/

username : batuhan
password : acet
isAdmin : True

username : yetkisizbatuhan
password : acet
isAdmin : false

username : user
password : user
isAdmin : false

This application is a Flask Application connected MongoDB with pymongo. I choose Flask because the connection to MongoDB is a very simple one-line code. Also, Flask uses Jinja templates, which provide easily manipulated HTML files. 

i have 3 collection in 1 db,

Products collection consist of 
_id:
type: [cloth,computer,monitor,slack]
name:
description:
price:
seller:
image:
size: -> only for cloth type
colour: -> only for cloth type
spec: -> only for computer and monitor type

Users collection consist of:
_id:
username:
password:
isAdmin:

Reviews collection consist of:
_id:
user_id:
product_id:
rating:
review:

In the application, only the homepage and Login tabs are visible. If the users are not logged in, they only see products detail and their pages. 

After the admin user login, the delete button is visible in the product card on the homepage. Also, see the different add buttons on the navbar. These buttons allow adding products or users.
Admin can delete users in the "Add and Remove Users" tab.

If the standard user login, the user cannot add or remove any user but can write a comment on product pages. Also cannot remove any product.

I handle this authentication method with the flask_login module.

On the homepage, a small filter button filters products according to the selected category filter.

After logging in, the profile button appears on the navbar, and users can see their ratings and reviews on their profile page.










