from flask import Flask, render_template, redirect, session
from models import connect_db, db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_project"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SECRET_KEY"] = "secret"


connect_db(app)
with app.app_context():
    db.drop_all()
    db.create_all()
    
@app.route('/')
def home():
    """redirect to registration"""
    return redirect('/register')

@app.route('/register', methods=["GET","POST"])
def register_user():
    """display registration form and process new user data"""
    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        new_user = User.register(username=username,pwd=password,first_name=first_name,last_name=last_name,email=email)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        return redirect(f'/users/{username}')
    else:    
        return render_template("registerUserForm.html",form=form)
    
@app.route('/login', methods=["GET","POST"])
def login_user():
    """display login form and login user"""
    form = LoginUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username=username,password=password)
        if user:
            session['username'] = user.username
        return redirect(f'/users/{user.username}')
    else:    
        return render_template("loginUserForm.html",form=form)    
    
@app.route('/users/<username>')
def user_detail(username):
    """display user detail after login"""
    if session['username'] != username:
        return redirect('/')
    else:
        user = db.session.get(User, username)
        feedback = user.feedback
        return render_template('userdetail.html',user=user,feedback=feedback)    

@app.route('/logout')
def logout():
    """log user out, clear session data"""
    session.clear()
    return redirect('/') 

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """delete user"""
    if session['username'] != username:
        return redirect('/')
    else:
        user = db.session.get(User, username)
        db.session.delete(user)
        db.session.commit()
        session.clear()
        return redirect('/')

@app.route('/users/<username>/feedback/add', methods=["GET","POST"])
def add_feedback(username):
    """display feedback form and process feedback data"""
    if session['username'] != username:
        return redirect('/')
    else:
        form = FeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            feedback = Feedback(title=title,content=content,username=username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f'/users/{username}')
        else:
            return render_template('feedbackForm.html',form=form)
        
@app.route('/feedback/<int:feedback_id>/update', methods=["GET","POST"])
def edit_feedback(feedback_id):
    """display feedback form and update feedback data"""
    feedback = db.session.get(Feedback,feedback_id)
    user = db.session.get(User, feedback.username)
    if session['username'] != user.username:
        return redirect('/')
    else:        
        form = FeedbackForm()
        if form.validate_on_submit():
            if form.title.data:
                feedback.title = form.title.data
            if form.content.data:
                feedback.content = form.content.data
            db.session.commit()
            return redirect(f'/users/{user.username}')
        else:
            return render_template('feedbackForm.html',form=form)
        
        
@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    """delete feedback"""
    feedback = db.session.get(Feedback,feedback_id)
    user = db.session.get(User, feedback.username)
    if session['username'] != feedback.username:
        return redirect('/')
    else:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{user.username}')