


from flask import Blueprint, render_template, request as req, redirect, session
import models.model as model
auth = Blueprint('auth',__name__, template_folder="../templates", static_folder="../static")



@auth.route('/')
@auth.route('/index')
def index():
    if 'username' in session:
        if model.get_info_player(session['username']):
            infoplayer = model.get_info_player(session['username'])
            return render_template('player/dashboard.html', data={'infoplayer': infoplayer})
        else:
            return "BAD USERNAME: {} not allowed, 403 FORBIDDEN, ".format(session['username']), 403
    else:
        return redirect("/login")



@auth.route('/login', methods=['GET','POST'])
def login():
    if req.method == 'GET':
        return render_template('auth/login.html')
    if req.method == 'POST':
        username = req.form.get('username')
        password = req.form.get('password')

        if username is not None:
            result = model.login(username, password)
            if result:
                session['username'] = username
                return redirect('/index')
            else:
                return "<a href='/login'>Invalid username/password</a>"
        else:
            return "<a href='/login'>Please Input Correct Username</a>"




@auth.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/index')



@auth.route('/register',methods=['GET','POST'])
def register():
    if req.method == 'GET':
        return render_template('auth/register.html')
    if req.method == 'POST':
        username = req.form.get('username')
        password = req.form.get('password')
        mercname = req.form.get('mercname')

        if any([username is None, password is None]):
            return "<a href='/register'>Please input correct Data!</a>"
        else:
            model.register(username,password, mercname)
            return redirect('/login')
