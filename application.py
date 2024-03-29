from flask import Flask, request, render_template, url_for, redirect
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, flash, current_user, logout_user
application = Flask(__name__)
application.debug=True
application.secret_key = '\xba\x99K~:\x14mV\x98\x1e@\x8c\x9e\x04\xd4\x90\x13\xc4*\xd3\xe7xa\xc7'

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'teacher'

studentgrades={}
test=None

class Student():
    def __init__(name, grade):
        self.name=name
        self.grade=grade

class Test():
    def __init__(self, size, key):
        self.size=size
        self.key=key
    def grade(self, request):
        count=0.0
        for k in request.form:
            if k=='name':
                pass
            elif self.key.get(k)==request.form.get(k):
                count+=1.0
        return (count/(len(self.key)))*100
    def length(self):
        return self.size+1

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active
 
    def is_active(self):
        return self.active
 
 
class Anonymous():
    name = u"Anonymous"
 
 
USERS = {
    1: User(u"Teacher", 1),
}
USER_NAMES = dict((u.name, u) for u in USERS.itervalues())


@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))

@application.route('/maybe')
def mayb():
    return 'huh'
@application.route('/')
def main():
    global test
    if test is None:
        return 'No Test Loaded'
    return render_template('testtake.html', i=test.length())
    
@application.route("/teacher", methods=['GET', 'POST'])
def logins():
    if current_user.is_active()==True:
        return render_template("teachon.html")
    if request.method =='POST':
        if request.form.get('Password')=='thisisateacherpassword':
            if login_user(USER_NAMES[request.form.get("username")]):
                flash('Logged in Successfully.')
                return render_template("teachon.html")
            else:
                flash('Sorry, couldn\'nt login')
    return render_template("login.html")

@application.route('/teststart')
@login_required
def testcount():
    return render_template('teacherlog.html')

@application.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("logins"))
    
@application.route('/faq')
def faq():
    return render_template('faq.html')

@application.route('/submit/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if studentgrades.get(request.form.get('name'))==None:
            studentgrades[request.form.get('name')]=test.grade(request)
        else:
            return 'This student has already submitted'
        return 'Test submitted'
    else:
        return 'GET on login not supported'
        
@application.route('/keytaker/', methods=['POST'])
@login_required
def keytake():
    key={}
    for i in request.form:
        key[i]=request.form.get(i)
    z=len(request.form)
    global test
    test=Test(z, key)
    global studentgrades
    studentgrades={}
    flash('Submitted')
    return render_template('teachon.html')
        

@application.route('/keymaker/', methods=['POST'])
@login_required
def teachlog():
    if request.method == 'POST':
        x= int(request.form.get('number'))
        y= int(request.form.get('frq'))
        return render_template("keymaker.html", i=x, n=y)
    
@application.route('/grades/')
@login_required
def viewgrades():
    global studentgrades
    sgrades={}
    u=studentgrades.iterkeys()
    for i in studentgrades.iterkeys():
        sgrades[unicode(i)]=unicode(studentgrades[i])
    q=sgrades.iterkeys()
    return render_template("gradeview.html", grades=sgrades, z=len(sgrades), x=q)
    
    
if __name__ == "__main__":
    login_manager.init_app(application)
    application.run()
    