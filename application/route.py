import sqlite3
from flask import Flask, render_template, request, url_for, redirect, abort, flash, Blueprint
from application.forms import formulario, form_crea_articulos, Form_Comentarios, Form_Login, Form_Signup
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_required, logout_user, login_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from application.bd import get_db_connection, close_db

mainpages_bp = Blueprint('mainpages_bp', __name__)

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index')) 


@auth_bp.route("/login", methods = ['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = Form_Login()

	if request.method == 'POST':
		print('Solicitud POST')
		if form.validate_on_submit():
			print('Formulario validado')
			conn = sqlite3.connect('database.db')
			curs = conn.cursor()
			curs.execute("SELECT * FROM login_usuario WHERE usuario = (?)", [form.usuario.data])
			if curs.fetchone() == None:
				flash('No existe usuario')
				return render_template('login_form.html', form=form)

			else:
				curs.execute("SELECT * FROM login_usuario WHERE usuario = (?)", [form.usuario.data])
				user = list(curs.fetchone())
				Us = load_user(user[0])
				print(f"US: {Us}")
				if form.usuario.data == Us.usuario and check_password_hash(Us.password, form.password.data):
					print('email y password correctos')
					login_user(Us, remember = form.remember.data)
					Umail = list({form.usuario.data})[0].split('@')[0]
					print('Logged in successfully ' + Umail)
					return redirect(url_for('index'))
				
				else:
					flash('Contraseña incorrecta')
	
	return render_template("login_form.html", form=form)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
	form = Form_Signup(request.form)
	if request.method == "POST":
		usuario= form.usuario.data
		password = form.password.data
		pass_crypt = generate_password_hash(password, 'sha256')

		conn = get_db_connection()
		conn.execute('INSERT INTO login_usuario (usuario, password) VALUES (?,?)', (usuario, pass_crypt))
		conn.commit()
		close_db()

		return redirect(url_for('index'))
	
	else:
		return render_template("signup_form.html", form=form)

@mainpages_bp.route("/")
def index():
	return render_template("index.html")



@mainpages_bp.route("/contacto", methods=["GET", "POST"])
def contacto():
	form = formulario(request.form)
	if request.method == "POST":
		nombre= form.name.data
		email= form.email.data
		text=  form.text.data
		print(nombre + email + text)

		conn = get_db_connection()
		conn.execute('INSERT INTO contacto (nombre, email, mensaje) VALUES (?,?,?)',
			(nombre, email, text))
		conn.commit()
		close_db()

		return redirect(url_for('mainpages_bp.index'))
	
	else:
		return render_template("contacto.html", form=form)

@mainpages_bp.route("/crear_articulos", methods=["GET", "POST"])
def crea_articulos():
	form = form_crea_articulos(request.form)
	if request.method == "POST":
		titulo= form.titulo.data
		articulo = form.articulo.data

		conn = get_db_connection()
		conn.execute('INSERT INTO articulos (titulo, articulo) VALUES (?,?)',
			(titulo, articulo))
		conn.commit()
		close_db()

		return redirect(url_for('mainpages_bp.index'))
		# A modificar después 
	
	else:
		return render_template("crea_articulos.html", form=form)


@mainpages_bp.route("/mensajes")
def mensajes():
	conn = get_db_connection()
	mensajes = conn.execute('SELECT * FROM contacto').fetchall()
	close_db()
	return render_template('mensajes.html', mensajes=mensajes)

@mainpages_bp.route("/articulos")
def articulos():
	conn = get_db_connection()
	articulos = conn.execute('SELECT * FROM articulos ORDER BY fecha DESC').fetchall()
	close_db()
	return render_template('articulos.html', articulos=articulos)

@mainpages_bp.route("/articulos_admin")
def articulos_admin():
	conn = get_db_connection()
	articulos = conn.execute('SELECT * FROM articulos ORDER BY fecha DESC').fetchall()
	close_db()
	return render_template('articulos_admin.html', articulos=articulos)



@mainpages_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_post(id):
	conn = get_db_connection()
	articulo = conn.execute('SELECT * FROM articulos WHERE id=?', (id,)).fetchone()
	close_db()
	if articulo is None:
		abort(404)

	form = form_crea_articulos(request.form)

	if request.method == "POST":
		titulo= form.titulo.data
		articulo = form.articulo.data

		conn = get_db_connection()
		conn.execute('UPDATE articulos SET titulo = ?, articulo= ? WHERE id=?', (titulo, articulo, id))

		conn.commit()
		close_db()

		return redirect(url_for('mainpages_bp.articulos'))

	form.titulo.data = articulo["titulo"]
	form.articulo.data = articulo["articulo"]


	return render_template('edit_post.html', form=form)

@mainpages_bp.route("/<int:id>/borrar", methods=["GET", "POST"])
def borrar_articulo(id):
	conn = get_db_connection()
	articulo = conn.execute('SELECT * FROM articulos WHERE id=?', (id,)).fetchone()
	conn.commit()
	close_db()
	
	if request.method == "POST":
		conn = get_db_connection()
		articulo = conn.execute('DELETE FROM articulos WHERE id=?', (id,))
		conn.commit()
		close_db()


	return redirect(url_for('mainpages_bp.articulos'))

@mainpages_bp.route("/<int:id>/articulo")
def ver_articulo(id):

	form = Form_Comentarios(request.form)

	conn = get_db_connection()
	articulo = conn.execute('SELECT * FROM articulos WHERE id=?', (id,)).fetchone()
	conn.commit()
	close_db()

	if request.method == "POST":
		autor = form.autor.data
		comentario = form.comentario.data

	return render_template("ver_articulo.html", articulo=articulo, form=form)

if __name__ == '__main__':
	app.run(debug=True)

