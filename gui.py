from tkinter import *
import requests
import ast


def sing_in(email, password, lf):
	email = email.get()
	password = password.get()
	req = requests.post('http://localhost:5000/', data={'username':email, 'password':password})
	if req.text == 'NOT OK':
		error = Label(lf, text='Недействительные данные', fg='red')
		error.pack(pady=15)
	else:
		data = ast.literal_eval(req.text)
		lf.destroy()
		home_page_form(data)

def register(email, pw, fn, ln, rf):
	email = email.get()
	password = pw.get()
	firstname = fn.get()
	lastname = ln.get()
	req = requests.post('http://localhost:5000/reg', data={'username':email, 'password':password, 'firstname':firstname, 'lastname':lastname})
	if req.text == 'OK':
		rf.destroy()
		login_form()
	else:
		error = Label(rf, text=req.text, fg='red')
		error.pack(pady=15)

def login_form():
	login_frame = Frame(root)
	login_frame.pack()

	email_lb = Label(login_frame, text='Электронная почта')
	email_lb.pack()
	email = Entry(login_frame, width=25)
	email.pack()
	pw_lb = Label(login_frame, text='Пароль')
	pw_lb.pack(pady=(15,0))
	pw = Entry(login_frame, width=25)
	pw.config(show='*')
	pw.pack()
	login = Button(login_frame, text='Войти', command=login_wrapper(sing_in, email, pw, login_frame))
	sing_up = Button(login_frame, text='Зарегистрироваться', command=register_form_wrapper(register_form, login_frame))
	login.pack(pady=(15, 15))
	sing_up.pack(pady=(0, 15))

def register_form_wrapper(func, lf):
	def wrapper():
		return func(lf)
	return wrapper

def register_wrapper(func, email, password, fn, ln, rf):
	def wrapper():
		return func(email, password, fn, ln, rf)
	return wrapper

def login_wrapper(func, email, password, lf):
	def wrapper():
		return func(email, password, lf)
	return wrapper

def back(email, pw, fn, ln, rf):
	rf.destroy()
	login_form()

def send_survey_wrapper(func, entry, theme):
	def wrapper():
		return func(entry, theme)
	return wrapper

def send_survey(entry, theme):
	temp = []
	for el in entry:
		temp.append(el.get())
	req = requests.post('http://localhost:5000/voting_load', data={'theme':theme.get(), 'entry':temp})

	

def create_survey_form():
	def generate_entry(var):
		for _ in range(int(var)):
			temp = Entry(survey, width=25)
			temp.pack()
			entry.append(temp)
		create = Button(survey, text='Создать', command=send_survey_wrapper(send_survey, entry, theme))
		create.pack()

	tkvar = IntVar(0)
	choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	survey = Toplevel(root)
	theme = Entry(survey, width=25)
	theme.pack()
	entry = []
	popupMenu = OptionMenu(survey, tkvar, *choices, command=generate_entry)
	popupMenu.pack()

def home_page_form(data):
	user_data = data
	home_page_frame = Frame(root)
	home_page_frame.pack()
	home_page_left_frame = Frame(home_page_frame)
	home_page_left_frame.pack(side=LEFT)
	create_survey = Button(home_page_left_frame, text='Создать форму голосования', command=create_survey_form)
	create_survey.pack()
	listbox = Listbox(home_page_left_frame, width=32, height=256, bg='red')
	listbox.pack()
	voting_frame = Frame(home_page_frame, width=512, height=256, bg='black')
	voting_frame.pack(side=LEFT)

def register_form(login_frame):
	login_frame.destroy()
	register_frame = Frame(root)
	register_frame.pack()

	email_lb = Label(register_frame, text='Электронная почта')
	email_lb.pack()
	email = Entry(register_frame, width=25)
	email.pack()
	pw_lb = Label(register_frame, text='Пароль')
	pw_lb.pack(pady=(15,0))
	pw = Entry(register_frame, width=25)
	pw.config(show='*')
	pw.pack()
	fn_lb = Label(register_frame,text='Имя')
	fn_lb.pack(pady=(15,0))
	first_name = Entry(register_frame, width=25)
	first_name.pack()
	ln_lb = Label(register_frame,text='Фамилия')
	ln_lb.pack(pady=(15,0))
	last_name = Entry(register_frame, width=25)
	last_name.pack()
	sing_up = Button(register_frame, text='Зарегистрироваться', command=register_wrapper(register, email, pw, first_name, last_name, register_frame))
	sing_up.pack(pady=(15, 0))
	back_but = Button(register_frame, text='Назад', command=register_wrapper(back, email, pw, first_name, last_name, register_frame))
	back_but.pack(pady=(30, 15))

root = Tk()

login_form()

root.mainloop()
























