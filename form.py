from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,DecimalField,DateField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
       username = StringField('username',validators=[DataRequired()])
       password = PasswordField('password',validators=[DataRequired()])
       submit =SubmitField('login')

class Oilsampleform(FlaskForm):
       oilname = StringField('oilname',validators=[DataRequired()])
       wellname = StringField('wellname',validators=[DataRequired()])
       batchno  = DecimalField('batchno',validators=[DataRequired()])
      
       submit =SubmitField('submit')


class Oilinfoform(FlaskForm):
       sampletype= StringField('sampletype',validators=[DataRequired()])
       layer= StringField('layer',validators=[DataRequired()])
       wellname = StringField('wellname',validators=[DataRequired()])
       initialdepth = DecimalField('initialdepth',validators=[DataRequired()])
       terminationdepth  = DecimalField('terminationdepth',validators=[DataRequired()])
       samplebucket = StringField('samplebucket',validators=[DataRequired()])
       
       submit =SubmitField('submit')

class Corebaseform(FlaskForm):
       oilname = StringField('oilname',validators=[DataRequired()])
       coretimes= DecimalField('coretimes',validators=[DataRequired()])
       batchno  = DecimalField('batchno',validators=[DataRequired()])
       wellname = StringField('wellname',validators=[DataRequired()])
       topdepth= DecimalField('topdepth',validators=[DataRequired()])
       bottomdepth  = DecimalField('bottomdepth',validators=[DataRequired()])
       coretotallength= DecimalField('coretotallength',validators=[DataRequired()])
       harvestrate= DecimalField('harvestrate',validators=[DataRequired()])
       
       submit =SubmitField('submit')
