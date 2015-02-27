from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class product_submit(Form):
    sku = StringField('sku', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    weight = StringField('weight', validators=[DataRequired()])
    company = StringField('company', validators=[DataRequired()])
    stock_location = StringField('stock_location', validators=[DataRequired()])
    place_of_origin = StringField('place_of_origin', validators=[DataRequired()])
    qty = StringField('qty', validators=[DataRequired()])
    orig_stock = StringField('orig_stock', validators=[DataRequired()])
