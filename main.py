from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    addr = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)


db.create_all()


@app.route('/')
def home():
    all_clients = Cliente.query.all()
    return render_template('home.html', clientes=all_clients)


@app.route('/add', methods=['GET', 'POST'])
def add_cliente():
    cliente_novo = Cliente(
        name=request.form['name'],
        email=request.form['email'],
        addr=request.form['addr'],
        phone=request.form['phone']
    )
    db.session.add(cliente_novo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit', methods=['GET', 'POST'])
def edit_cliente():
    if request.method == 'POST':
        cliente_id = request.form['id']
        cliente_editar = Cliente.query.get(cliente_id)
        cliente_editar.name = request.form['nameedit']
        cliente_editar.email = request.form['emailedit']
        cliente_editar.addr = request.form['addredit']
        cliente_editar.phone = request.form['phoneedit']
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete')
def delete_cliente():
    cliente_id = request.args.get('id')
    print('enter')
    cliente_selecionado = Cliente.query.get(cliente_id)
    db.session.delete(cliente_selecionado)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
