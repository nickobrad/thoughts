from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, DateField
from wtforms.validators import Required

class PitchForm(FlaskForm):
    pitch = TextAreaField('Your Pitch', validators = [Required()])
    category = StringField('Pitch category', validators = [Required()])
    submit = SubmitField('Post your pitch')


class CommentForm(FlaskForm):
    comment = StringField ('Comment on this', validators = [Required()])
    submit = SubmitField('Comment')



