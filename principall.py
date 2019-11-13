from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ejercicio.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class ejercicio(db.Model):
   id = db.Column('ejercicio_id', db.Integer, primary_key = True)
   nombre = db.Column(db.String(100))
   ciudad = db.Column(db.String(50))
   trabajo  = db.Column(db.String(100))
   fecha_entrega = db.Column(db.String(50))
   addr = db.Column(db.String(200))
   pin = db.Column(db.String(10))

   def __init__(self, nombre, ciudad, trabajo, fecha_entrega, addr, pin):
       self.nombre = nombre
       self.ciudad = ciudad
       self.trabajo = trabajo
       self.fecha_entrega = fecha_entrega
       self.addr = addr
       self.pin = pin

@app.route('/')
def show_all():
   return render_template('show_all.html', ejercicios = ejercicio.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['nombre'] or not request.form['ciudad'] or not request.form['trabajo'] or not request.form['fecha_entrega'] or not request.form['addr']:
         flash('Please enter all the fields', 'error')
      else:
         ejercicio1 = ejercicio(request.form['nombre'], request.form['ciudad'], request.form['trabajo'], request.form['fecha_entrega'], request.form['addr'], request.form['pin'])

         db.session.add(ejercicio1)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

@app.route("/update", methods=["POST"])
def update():
    nombre = request.form.get("oldnombre")
    ejercicio = ejercicio.query.filter_by(nombre=nombre).first()
    return render_template('update.html', result = ejercicio, oldname = nombre)

@app.route("/update_record", methods=["POST"])
def update_record():
    nombre = request.form.get("oldnombre")
    ejercicio = ejercicio.query.filter_by(nombre=nombre).first()
    ejercicio.nombre = request.form['nombre']
    ejercicio.ciudad = request.form['ciudad']
    ejercicio.trabajo = request.form['trabajo']
    ejercicio.fecha_entrega = request.form['fecha_entrega']
    ejercicio.addr = request.form['addr']
    ejercicio.pin = request.form['pin']
    db.session.commit()
    return redirect('/')

@app.route("/delete", methods=["POST"])
def delete():
    name = request.form.get("oldname")
    ejercicio1 = ejercicio.query.filter_by(nombre=name).first()
    db.session.delete(ejercicio1)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
