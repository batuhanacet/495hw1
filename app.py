from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, UserMixin, LoginManager,current_user
from pymongo import MongoClient
from bson.objectid import ObjectId
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

client = MongoClient("mongodb+srv://batuhanacet:ceng495hw1@cluster0.mzzdi07.mongodb.net/?retryWrites=true&w=majority")
db = client.gettingStarted

login_manager = LoginManager()
login_manager.init_app(app)



#login logout routes

class User(UserMixin):
    def __init__(self, id, username, password, isAdmin):
        self.id = id
        self.username = username
        self.password = password
        self.isAdmin = isAdmin

    def get_id(self):
        return str(self.id)
    
# Define the user_loader callback function
@login_manager.user_loader
def load_user(user_id):
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if user:
        return User(user['_id'], user['username'], user['password'], user['isAdmin'])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        # Check if the username and password are correct
        user = db.users.find_one({'username': username, 'password': password})
        if user is not None:
            user_obj = User(user['_id'], user['username'], user['password'], user['isAdmin'] )
            login_user(user_obj)
            return redirect(url_for('home'))

        # If the username or password is incorrect, show an error message
        flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

#---------------------------------------------------------------

@app.route('/adduser', methods=['POST'])
def adduser():
    username = request.form['username']
    password = request.form['password']
    isAdmin = request.form['isAdmin']

    db.users.insert_one({
        'username': username, 
        'password': password, 
        'isAdmin': True if isAdmin=='true' else False
        })

    return redirect(url_for('users'))

@app.route('/profile')
@login_required
def profile():
    if current_user.is_authenticated:    
        loggedIn = True
        isAdmin= current_user.isAdmin
        name = current_user.username    
    else:
        loggedIn = False
        isAdmin = False
    reviews = db.reviews.find({'user_id':ObjectId(current_user.id)})

    return render_template('profile.html',reviews=reviews,name=name,loggedIn = loggedIn, isAdmin = isAdmin)



@app.route('/addComment', methods=['POST'])
def addComment():
    product_id = request.form['item_id']
    rating = int(request.form['rating'])
    review = request.form['review']

    if current_user.is_authenticated: 
        user_id = current_user.id

        existingReview = db.reviews.find_one({'user_id': ObjectId(user_id), 'product_id': ObjectId(product_id)})

        if existingReview:
            db.reviews.update_one(
                            {'user_id': ObjectId(user_id), 'product_id': ObjectId(product_id)},
                            {'$set': {'rating': rating, 'review': review}})
        else:

            db.reviews.insert_one({
                            'user_id': ObjectId(user_id), 
                            'product_id': ObjectId(product_id),
                            'rating': rating, 
                            'review': review})
    
    return redirect(url_for('home'))


#render html templates



@app.route('/item/<item_id>')
def item(item_id):
    item = db.products.find_one({'_id': ObjectId(item_id)})
    reviews = db.reviews.find({'product_id':ObjectId(item_id)})
    if current_user.is_authenticated:    
        loggedIn = True
        isAdmin= current_user.isAdmin    
    else:
        loggedIn = False
        isAdmin = False
    return render_template('product.html', item=item, reviews = reviews, loggedIn = loggedIn, isAdmin = isAdmin)


@app.route("/")
def home():
    category = request.args.get('category')
    if category:
        products = db.products.find({'type':category})
    else:
        products = db.products.find()    
    
    if current_user.is_authenticated:    
        loggedIn = True
        isAdmin= current_user.isAdmin    
    else:
        loggedIn = False
        isAdmin = False
    
    return render_template("home.html",products=products, category = category, loggedIn = loggedIn, isAdmin = isAdmin)

@app.route("/loginPage")
def loginPage():
    return render_template("login.html")

@app.route("/clothForm")
def clothForm():
    if current_user.is_authenticated:    
        loggedIn = True
        isAdmin= current_user.isAdmin    
    else:
        loggedIn = False
        isAdmin = False
    return render_template("clothForm.html", loggedIn = loggedIn, isAdmin = isAdmin)

@app.route("/computerForm")
def computerForm():
    if current_user.is_authenticated:    
        loggedIn = True
        isAdmin= current_user.isAdmin    
    else:
        loggedIn = False
        isAdmin = False
    return render_template("computerForm.html", loggedIn = loggedIn, isAdmin = isAdmin)

@app.route("/monitorForm")
def monitorForm():
    if current_user.is_authenticated:    
        loggedIn = True
        isAdmin= current_user.isAdmin    
    else:
        loggedIn = False
        isAdmin = False
    return render_template("monitorForm.html", loggedIn = loggedIn, isAdmin = isAdmin)

@app.route("/snackForm")
def snackForm():
    if current_user.is_authenticated:    
        loggedIn = True
        isAdmin= current_user.isAdmin    
    else:
        loggedIn = False
        isAdmin = False
    return render_template("snackForm.html", loggedIn = loggedIn, isAdmin = isAdmin)

@app.route("/users")
def users():
    if current_user.is_authenticated:    
        loggedIn = True
        isAdmin= current_user.isAdmin    
    else:
        loggedIn = False
        isAdmin = False
    users = db.users.find()
    return render_template("users.html",users=users, loggedIn = loggedIn, isAdmin = isAdmin)


#-------------------------------

#delete routes 

@app.route('/deleteUser', methods=['POST'])
def deleteUser():
    user_id = request.form['user_id']
    db.users.delete_one({'_id': ObjectId(user_id)})
    return redirect(url_for('users'))

@app.route('/delete', methods=['POST'])
def deleteProduct():
    item_id = request.form['item_id']
    db.products.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('home'))

#----------------------------------------------

#inserting product form routes inside

@app.route('/submit-clothForm', methods=['POST'])
def submit_clothForm():
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    seller = request.form['seller']
    image = request.form['image']
    size = request.form['size']
    colour = request.form['colour']

    db.products.insert_one({
        'type': 'cloth',
        'name': name, 
        'description': description, 
        'price': price,
        'seller': seller,
        'image': image,
        'size':size,
        'colour':colour
        })

    return redirect(url_for('home'))


@app.route('/submit-computerForm', methods=['POST'])
def submit_computerForm():
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    seller = request.form['seller']
    image = request.form['image']
    spec = request.form['spec']

    db.products.insert_one({
        'type':'computer',
        'name': name, 
        'description': description, 
        'price': price,
        'seller': seller,
        'image': image,
        'spec':spec
        })

    return redirect(url_for('home'))

@app.route('/submit-monitorForm', methods=['POST'])
def submit_monitorForm():
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    seller = request.form['seller']
    image = request.form['image']
    spec = request.form['spec']

    db.products.insert_one({
        'type':'monitor',
        'name': name, 
        'description': description, 
        'price': price,
        'seller': seller,
        'image': image,
        'spec':spec
        })

    return redirect(url_for('home'))

@app.route('/submit-snackForm', methods=['POST'])
def submit_snackForm():
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    seller = request.form['seller']
    image = request.form['image']

    db.products.insert_one({
        'type':'snack',
        'name': name, 
        'description': description, 
        'price': price,
        'seller': seller,
        'image': image
        })

    return redirect(url_for('home'))

if __name__ =="__main__":
    app.run()