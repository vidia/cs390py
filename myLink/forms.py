from flask_wtf import Form
from wtforms import TextField, PasswordField, FileField
from  wtforms import validators
from wtforms.validators import DataRequired


class LoginForm(Form):
    """Form class for user login."""
    email = TextField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class SignupForm(Form):
    # username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])
    # accept_tos = BooleanField('I accept the TOS', [validators.Required()])

class UpdateProfileForm(Form):
    email = TextField('email', validators=[DataRequired()])

    current_password = PasswordField('password')
    new_password = PasswordField('New Password', [
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

    first_name = TextField('First name')
    last_name = TextField('Last name')

    image = FileField(u'Profile Picture')

    ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

    def validate_image(form, field):

        print("Validating the image " + field.data.filename)
        if field.data:
            print("Have data")
            filename = field.data.filename
            return '.' in filename and \
               filename.rsplit('.', 1)[1] in form.ALLOWED_EXTENSIONS
        else:
            return True




"""Testing"""
class UploadForm(Form):
    image = FileField(u'Image File', validators=[DataRequired()])

    ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

    def validate_image(form, field):
        filename = field.data
        return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
#
# def upload(request):
#     form = UploadForm(request.POST)
#     if form.image.data:
#         image_data = request.FILES[form.image.name].read()
#         open(os.path.join(UPLOAD_PATH, form.image.data), 'w').write(image_data)
