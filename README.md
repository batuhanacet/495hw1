# 495hw1

https://ceng495hw1webservice.onrender.com/
username : batuhan
password : acet

This is an Flask Application connected mongodb with pymongo.


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

In application, Only visible Home and Login first. If user not logged in only see products detail and their pages. 

If admin user login, delete button visible in product card in homepage, also see different add button on navbar. They provide add products or user.
Admin can delete users in add remove users tab.

if normal user login, cannot add or remove any user but can write comment in product pages.

i handle this authentication methods with flask_login module.

in homepage we have a little filter button that filters products according to selected category filter.

after logged in profil button appear on navbar, user can see own ratings and reviews.










