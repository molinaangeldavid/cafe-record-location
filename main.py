from ast import Pass
from lib2to3.pgen2.token import NEWLINE
from attrs import validators
from flask import Flask,render_template,url_for,request
from flask_bootstrap import Bootstrap4
from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,validators,SubmitField
import csv

app = Flask(__name__)
app.secret_key = 'My pen is yellow'
class MyForm(FlaskForm):
    cafe_name = StringField(label='Coffe Name', validators=[validators.DataRequired('Name required')])
    cafe_location = StringField(label='Cafe Location',validators=[validators.DataRequired('Location required'),validators.URL(message='Must be an URL input')])
    open_hour = StringField(label='Open hour',validators=[validators.DataRequired('Open hour required')])
    close_hour = StringField(label='Close hour',validators=[validators.DataRequired('Close hour required')])
    coffee_rank = SelectField(label='Coffee quality',choices=['☕','☕☕','☕☕☕','☕☕☕☕','☕☕☕☕☕'], validators=[validators.DataRequired()])
    wifi_rank = SelectField(label='Wifi quiality',choices=['✘','💪','💪💪','💪💪💪','💪💪💪💪','💪💪💪💪💪'], validators=[validators.DataRequired()])
    energy_rank = SelectField(label='Energy',choices=['✘','🔌','🔌🔌','🔌🔌🔌','🔌🔌🔌🔌','🔌🔌🔌🔌🔌'], validators=[validators.DataRequired()])
    submit = SubmitField(label='Add coffee')

bootstrap = Bootstrap4(app)

def open_csvfile():
    cafes = []
    with open('cafe-data.csv', newline='',encoding='utf-8')as data:
        read_file = csv.reader(data,delimiter=',')
        for item in read_file:
            cafes.append(item)
        return cafes
            
def write_csvfile(n,l,op,cl,cof,wifi,ener):
    with open('cafe-data.csv', 'a', newline='', encoding='utf-8') as csv_file:
        write_file = csv.writer(csv_file,delimiter=',')
        write_file.writerow([n,l,op,cl,cof,wifi,ener])
            
@app.route('/')
def main():
    url_for('static', filename='css/styles.css')
    return render_template('index.html')

@app.route('/coffee')
def coffee():
    url_for('static', filename='css/styles.css')    
    data = open_csvfile()
    return render_template('coffee.html', data=data)

@app.route('/add', methods=['GET','POST'])
def add():
    form = MyForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form['cafe_name']
        location = request.form['cafe_location']
        open_hour = request.form['open_hour']
        close_hour = request.form['close_hour']
        coffee_r = request.form['coffee_rank']
        wifi_r = request.form['wifi_rank']
        energy_r = request.form['energy_rank']
        write_csvfile(f'\n{name}',location,open_hour,close_hour,coffee_r,wifi_r,energy_r)
    return render_template('add.html', form=form)



if __name__ == '__main__':
    
    app.run(debug=True)
