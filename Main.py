import customtkinter
import sqlite3
import bcrypt
from tkinter import *
from tkinter import messagebox

app = customtkinter.CTk() 
app.geometry("500x360")
app.title('Login')

font1 = ('Helvetica',25,'bold')
font2 = ('Arial',17,'bold')
font3 = ('Arial',12,'bold')
font4 = ('Arial',12,'bold','underline')

db = sqlite3.connect('hospitalDB.db')
cursor = db.cursor()

def signup():
    username = user_entry.get()
    password = pass_entry.get()
    type_user = type_combo.get()
    if username != '' and password != '' and type_user != '------':
        cursor.execute('SELECT username From users WHERE username=?', [username])
        if cursor.fetchone() is not None:
            messagebox.showerror(title='Error!',message="El usuario ya existe.")
        else:
            encoded_password = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
            print(hashed_password)
            cursor.execute('INSERT INTO users VALUES (?, ?, ?)', [username,hashed_password,type_user])
            db.commit()
            messagebox.showinfo(title='Exito!',message='La cuenta ha sido creada.')
    else:
        messagebox.showerror(title='Error!',message="Ingrese todos los campos requeridos.")

frame1 = customtkinter.CTkFrame(app,bg_color='#001220',fg_color='#001220',width=500,height=360)
frame1.place(x=0,y=0)

imageLogo = PhotoImage(file='images/logo.png')
imageLogo_label = Label(frame1,image=imageLogo,bg='#001220')
imageLogo_label.place(x=0,y=0)

singup_label = customtkinter.CTkLabel(frame1,font=font1,text="Registrate",text_color='#fff',bg_color='#001220')
singup_label.place(x=280,y=20)

user_entry = customtkinter.CTkEntry(frame1,font=font2,text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3,placeholder_text='Usuario',placeholder_text_color='#a3a3a3',width=200,height=50)
user_entry.place(x=280,y=80)

pass_entry = customtkinter.CTkEntry(frame1,font=font2,show='*',text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3,placeholder_text='Contrasena',placeholder_text_color='#a3a3a3',width=200,height=50)
pass_entry.place(x=280,y=150)

type_label = customtkinter.CTkLabel(frame1,font=font3,text="Tipo de usuario",text_color='#fff',bg_color='#001220')
type_label.place(x=280,y=210)

type_combo = customtkinter.CTkComboBox(frame1,values=['------','Medico','Paciente'],text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',button_color='#004780',dropdown_fg_color='#001a2e',dropdown_hover_color='#006e44',dropdown_text_color='#fff')
type_combo.place(x=280,y=240)

sigunp_button = customtkinter.CTkButton(frame1,command=signup,font=font2,text_color='#fff',text='Registrate',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=120)
sigunp_button.place(x=280,y=290)

login_label = customtkinter.CTkLabel(frame1,font=font3,text='Tienes una cuenta?',text_color='#fff',bg_color='#001220')
login_label.place(x=280,y=330)

login_button = customtkinter.CTkButton(frame1,font=font4,text_color='#00bf77',text='Iniciar Sesion',fg_color='#001220',hover_color='#001220',cursor='hand2',width=40)
login_button.place(x=390,y=330)

app.mainloop()