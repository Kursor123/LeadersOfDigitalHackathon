from flask import Flask, request
import pymysql
import hashlib
from urllib.parse import unquote
from pymysql.cursors import DictCursor


app = Flask(__name__)

@app.route('/', methods=['POST'])
def login():
	data = request.get_data()
	data = data.decode('UTF-8').split('&')
	username = unquote(data[0][data[0].find('=') + 1:])
	password = hashlib.md5(data[1][data[1].find('=') + 1:].encode('UTF-8')).hexdigest()
	connection = pymysql.connect(
		host='localhost',
		user='root',
		password='hl2ar2smg1ep3',
		db='usersdb',
		charset='utf8mb4',
		cursorclass=DictCursor,
	)
	cur = connection.cursor()
	cur.execute("SELECT * FROM Users where email=%s", (username, ))
	db_data = cur.fetchone()
	connection.close()
	if db_data and username == db_data['email'] and password == db_data['password']:
		return db_data
	else:
		return 'NOT OK'

@app.route('/voting_load', methods=['POST'])
def load():
	data = request.get_data()
	data = data.decode('UTF-8').split('&')
	print(data)
	return 'OK'

@app.route('/reg', methods=['POST'])
def register():
	try:
		data = request.get_data()
		data = data.decode('UTF-8').split('&')
		username = unquote(data[0][data[0].find('=') + 1:])
		password = hashlib.md5(data[1][data[1].find('=') + 1:].encode('UTF-8')).hexdigest()
		firstname = unquote(data[2][data[2].find('=') + 1:])
		lastname = unquote(data[3][data[3].find('=') + 1:])
		connection = pymysql.connect(
			host='localhost',
			user='root',
			password='hl2ar2smg1ep3',
			db='usersdb',
			charset='utf8mb4',
			cursorclass=DictCursor,
			autocommit=True
		)
		cur = connection.cursor()
		sql = "INSERT INTO Users (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)"
		cur.execute(sql, (firstname, lastname, username, password))
	except pymysql.err.DataError:
		connection.close()
		return 'Введены некорректные данные'
	except pymysql.err.IntegrityError:
		connection.close()
		return 'Данный адрес электронной почты уже зарегистрирован.'
	else:
		connection.close()
		return 'OK'

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)













