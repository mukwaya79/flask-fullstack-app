from flask import Flask,render_template,url_for,redirect,flash,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from form import LoginForm, Oilsampleform, Oilinfoform, Corebaseform
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user



app = Flask(__name__)
app.config['SECRET_KEY'] ='kalenzo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db =SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key =True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role     = db.Column(db.String(15))

    def __repr__(self):
        return '<User %r>' % self.username

class Oilsample(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    oilname = db.Column(db.String(150), nullable=False)
    wellname = db.Column(db.String(100), nullable=False)
    batchno    = db.Column(db.Float,nullable=False)
    recorddate = db.Column(db.DateTime,default =datetime.now())

    def __repr__(self):
        return '<Oilsample %r>' % self.oilname

class Oilinfo(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    sampletype = db.Column(db.String(150), nullable=False)
    wellname = db.Column(db.String(100), nullable=False)
    layer = db.Column(db.String(150), nullable=False)
    initialdepth = db.Column(db.Float, nullable=False)
    terminationdepth = db.Column(db.Float, nullable=False)
    samplebucket= db.Column(db.String(100), nullable=False)
    uploaddate = db.Column(db.DateTime,default =datetime.now())

    def __repr__(self):
        return '<Oilinfo %r>' % self.sampletype

class Corebase(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    oilname = db.Column(db.String(150), nullable=False)
    wellname = db.Column(db.String(100), nullable=False)
    batchno = db.Column(db.Float, nullable=False)
    coretimes = db.Column(db.Float, nullable=False)
    topdepth = db.Column(db.Float, nullable=False)
    bottomdepth = db.Column(db.Float, nullable=False)
    coretotallength = db.Column(db.Float, nullable=False)
    harvestrate= db.Column(db.Float, nullable=False)
    recorddate = db.Column(db.DateTime,default =datetime.now())

    def __repr__(self):
        return '<Corebase %r>' % self.harvestrate

@app.route('/dashbord',)

def dashboard():
    return render_template('dashboard.html')

@app.route('/',methods =['GET'])
def signin():
    form = LoginForm()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()
    if request.method == 'POST' :
            user= User.query.filter_by(username=form.username.data).first()
            if user:
                if user.password == form.password.data :
                    login_user(user)
                    flash('You are Welcome','success')
                    return redirect(url_for('dashboard'))

                else:
                    flash('login Unsuccessful','danger')
                    return redirect(url_for('signin'))

            else:
                 flash('invalid credentials','danger')
                 return redirect(url_for('signin'))
             
    return render_template('login.html',title='login', form=form)


@app.route('/oilsample/new', methods=['GET','POST'])
def new_oilsample():

    form = Oilsampleform()
    if request.method == 'POST':
        oilsample=Oilsample(oilname=form.oilname.data,wellname=form.wellname.data,batchno=form.batchno.data)
        db.session.add(oilsample)
        db.session.commit()

        flash('Data successfully Added','success')
        return redirect(url_for('oilsample'))

    return render_template('create_oilsample.html',form=form)

@app.route('/oilinfo/new', methods=['GET','POST'])
def new_oilinfo():

    form = Oilinfoform()
    if request.method == 'POST':
        oilinfo= Oilinfo(wellname=form.wellname.data,sampletype=form.sampletype.data,layer=form.layer.data,
        initialdepth=form.initialdepth.data,terminationdepth=form.terminationdepth.data,samplebucket=form.samplebucket.data)
        db.session.add(oilinfo)
        db.session.commit()

        flash('Data successfully Added','success')
        return redirect(url_for('oilinfo'))

    return render_template('create_oilinfo.html',form=form)


@app.route('/corebase/new', methods=['GET','POST'])
def new_corebase():

    form = Corebaseform()
    if request.method == 'POST':
        corebase=Corebase(oilname=form.oilname.data,wellname=form.wellname.data,batchno=form.batchno.data
        ,coretimes=form.coretimes.data,topdepth=form.topdepth.data,bottomdepth=form.bottomdepth.data,coretotallength=form.coretotallength.data,
        harvestrate=form.harvestrate.data)
        db.session.add(corebase)
        db.session.commit()

        flash('Data successfully Added','success')
        return redirect(url_for('corebase'))

    return render_template('create_corebase.html',form=form)

@app.route('/oilinfo')
@login_required
def oilinfo():
    infos = Oilinfo.query.all()

    return render_template('oilinfo.html',infos=infos)

@app.route('/oilsample')
@login_required
def oilsample():
    infos = Oilsample.query.all()

    return render_template('oilsample.html',infos=infos)

@app.route('/corebase')
@login_required
def corebase():
    infos = Corebase.query.all()

    return render_template('corebase.html',infos=infos)

@app.route('/navigation')
@login_required
def navigation():
    return render_template('navigation.html')

@app.route('/logout')
@login_required
def logout():

    logout_user()
    flash('login to continue','danger')
    return redirect(url_for('login'))

@app.route('/corebase/<id>/update', methods=['GET','POST'])
def corebaseupdate(id):
    corebase1 = Corebase.query.get_or_404(id)
    
    if request.method == 'POST':
        
        corebase1.oilname = request.form['oilname']
        corebase1.wellname = request.form['wellname']
        corebase1.batchno = request.form['batchno']
        corebase1.coretimes = request.form['coretimes']
        corebase1.topdepth = request.form['topdepth']
        corebase1.bottomdepth = request.form['bottomdepth']
        corebase1.coretotallength = request.form['coretotallength']
        corebase1.harvestrate = request.form['harvestrate']

        try:
            db.session.commit()

            flash('corebase data has been successfully updated','success')
            return redirect(url_for('corebase'))
        
        except:
            return 'there is an issue updating the info'

    else:
        return render_template('corebase_update.html',corebase1=corebase1)

@app.route('/oilinfo/<id>/update', methods=['GET','POST'])
def oilinfoupdate(id):
    oilinfo1 = Oilinfo.query.get_or_404(id)
    
    if request.method == 'POST':
        
        oilinfo1.sampletype = request.form['sampletype']
        oilinfo1.wellname = request.form['wellname']
        oilinfo1.layer = request.form['layer']
        oilinfo1.initialdepth = request.form['initialdepth']
        oilinfo1.terminationdepth = request.form['terminationdepth']
        oilinfo1.samplebucket = request.form['samplebucket']
        

        try:
            db.session.commit()

            flash('Oilinfo data has been successfully updated','success')
            return redirect(url_for('oilinfo'))
        
        except:
            return 'there is an issue updating the info'

    else:
        return render_template('oilinfo_update.html',oilinfo1 = oilinfo1)

@app.route('/oilsample/<id>/update', methods=['GET','POST'])
def oilsampleupdate(id):
    oilsample1 = Oilsample.query.get_or_404(id)
    
    if request.method == 'POST':
        
        oilsample1.oilname = request.form['oilname']
        oilsample1.wellname = request.form['wellname']
        oilsample1.batchno = request.form['batchno']

        try:
            db.session.commit()

            flash('Oilsample data has been successfully updated','success')
            return redirect(url_for('oilsample'))
        
        except:
            return 'there is an issue updating the info'

    else:
        return render_template('oilsample_update.html',oilsample1 = oilsample1)



@app.route('/corebase/delete/<int:id>')
def deletecorebase(id):

    item_to_delete = Corebase.query.get_or_404(id)
    try:
        flash('item Successfully deleted','success')
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('corebase'))
    
    except:
        flash('Unable to delete ','danger')
        return redirect(url_for('corebase'))

@app.route('/oilinfo/delete/<int:id>')
def deleteoilinfo(id):

    item_to_delete = Oilinfo.query.get_or_404(id)
    try:
        flash('item Successfully deleted','success')
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('oilinfo'))
    
    except:
        flash('Unable to delete ','danger')
        return redirect(url_for('oilinfo'))

@app.route('/oilsample/delete/<int:id>')
def deleteoilsample(id):

    item_to_delete = Oilsample.query.get_or_404(id)
    try:
        flash('item Successfully deleted','success')
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('oilsample'))
    
    except:
        flash('Unable to delete ','danger')
        return redirect(url_for('oilsample'))



















if __name__ == '__main__':
    app.run(debug=True)





