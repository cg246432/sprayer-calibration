import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField, StringField, FieldList, FormField
from wtforms.validators import DataRequired
from urllib.parse import parse_qs

load_dotenv()

app = Flask(__name__, template_folder='templates')

# For Flask-WTF forms
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
# Flask Bootstrap
Bootstrap(app)


# Define Sprayer Settings
class SprayerForm(FlaskForm):
    sprayer_width = FloatField("Effective Spray Width in Inches. Nozzle Spacing x Number of Nozzles if unknown.", validators=[DataRequired()])
    test_length = FloatField("Length of Test Area in Feet.", validators=[DataRequired()])
    test_time = FloatField("Time it took to Traverse Length of Test Area in Seconds.", validators=[DataRequired()])
    flow_rate = FloatField("Ounces per minute from Sprayer.", validators=[DataRequired()])
    sprayer_size = FloatField("Size of Sprayer Tank in Gallons.")
    submit = SubmitField("Submit")

class IngredientForm(FlaskForm):
    name = StringField("Name of Ingredient.")
    amount = FloatField("Rate per 1,000 Sq. Ft. in Ounces.")
    add = SubmitField("Add")

class IngredientsForm(FlaskForm):
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)

@app.route('/', methods=['GET', 'POST'])
def index():
    initial_form = SprayerForm()
    message = ""
    if initial_form.validate_on_submit():
        test_area_per_thousand = 1000.0 / ((initial_form.sprayer_width.data / 12.0) * initial_form.test_length.data)
        ounces_per_test_area = (initial_form.flow_rate.data / 60.0) * initial_form.test_time.data
        ounces_per_thousand = test_area_per_thousand * ounces_per_test_area
        gallons_per_thousand = ounces_per_thousand / 128.0
        return render_template('index.html', form=initial_form, ounce_result=ounces_per_thousand, gallon_result=gallons_per_thousand, sprayer_size=initial_form.sprayer_size.data)
    else:
        message = "Input data into all fields."
    return render_template('index.html', form=initial_form, message=message, result=None)
