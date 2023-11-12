import customtkinter
import sqlite3
import bcrypt
from tkinter import *
from tkinter import messagebox
from tkcalendar import *

app = customtkinter.CTk() 
app.geometry("500x360")
app.title('Login')

font1 = ('Helvetica',25,'bold')
font2 = ('Arial',17,'bold')
font3 = ('Arial',12,'bold')
font4 = ('Arial',12,'bold','underline')

db = sqlite3.connect('hospitalDB.db')
cursor = db.cursor()

def pick_date(event):
    global cal

    ventana = Toplevel()
    ventana.grab_set()
    ventana.title("Ingresa fecha de nacimiento")
    ventana.geometry('250x220+590+370')

    cal = Calendar(ventana,text = "Confirmar", selectmode='day',year=2023,month=1,date_pattern="mm/dd/y")
    cal.place(x=0, y=0)
    date = cal.get_date()

    confirmar = customtkinter.CTkButton(ventana,command=grab_date,font=font1,text_color='#fff',text='Confirmar',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=100)
    confirmar.place(x=20, y=190)

def grab_date():
    nacimiento_paciente.delete(0, END)
    nacimiento_paciente.insert(0, cal.get_date())

def guardar_informacion():
    print("guarda")
    id = user_entry2.get()
    nombre = nombre_paciente.get()
    sexo = genero_paciente.get()
    peso = peso_paciente.get()
    estatura = estatura_paciente.get()
    nacimiento = nacimiento_paciente.get()
    ss = ss_paciente.get()
    print(id,nombre,sexo,peso,estatura,nacimiento,ss)
    if id != '' and nombre != '' and sexo != '------' and peso != '' and estatura != '' and nacimiento != '' and ss != '': 
        cursor.execute('INSERT INTO info_paciente VALUES (?, ?, ?, ?, ?, ?, ?)', [id,nombre,sexo,peso,estatura,nacimiento,ss])
        db.commit()
        messagebox.showinfo(title='Exito!',message='Los datos han sido guardados.')
    else:
        messagebox.showerror(title='Error!',message="Ingrese todos los campos requeridos(1).")

def guardar_informacion_doctor():
    id = user_entry2.get()
    nombre = nombre_doctor.get()
    especialiad = especialidad_doctor.get()

    if id != '' and nombre != '' and especialiad != '------': 
        cursor.execute('INSERT INTO info_doctor VALUES (?, ?, ?)', [id,nombre,especialiad])
        db.commit()
        messagebox.showinfo(title='Exito!',message='Los datos han sido guardados.')
    else:
        messagebox.showerror(title='Error!',message="Ingrese todos los campos requeridos(1).")


def guarda_cita():
    print("guarda")
    id = user_entry2.get()
    sintomas = sintomas_paciente.get()
    hora_cita = hora_paciente.get()
    fecha_cita = fecha_paciente.get()
    
    if id != '' and sintomas != '' and hora_cita != '------' and fecha_cita != '': 
        cursor.execute('INSERT INTO citas VALUES (?, ?, ?, ?)', [id,sintomas,hora_cita,fecha_cita])
        db.commit()
        messagebox.showinfo(title='Exito!',message='Los datos han sido guardados.')
    else:
        messagebox.showerror(title='Error!',message="Ingrese todos los campos requeridos(1).")
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
            cursor.execute('INSERT INTO users  VALUES (?, ?, ?)', [username,hashed_password,type_user])
            db.commit()
            messagebox.showinfo(title='Exito!',message='La cuenta ha sido creada.')
    else:
        messagebox.showerror(title='Error!',message="Ingrese todos los campos requeridos.")

def login_account():
    username = user_entry2.get()
    password = pass_entry2.get()
    if username !='' and password !='':
        cursor.execute('SELECT password FROM users WHERE username=?', [username])
        result = cursor.fetchone()
        if result:
            if bcrypt.checkpw(password.encode('utf-8'),result[0]):
                #messagebox.showinfo(title='Exito!',message='Inicio de sesion exitoso.')
                cursor.execute('SELECT user_type FROM users WHERE username = ?', [username])
                tipo = cursor.fetchone()
                if tipo is not None and tipo[0] == "Paciente":
                    menu_paciente()
                else:
                    #messagebox.showinfo(title='Éxito!', message='Inicio de sesión doctor.')
                    menu_doctor()
            else:
                messagebox.showerror(title='Error!',message='Contraseña incorrecta.')
        else:
            messagebox.showerror(title='Error!',message='Usuario incorrecto.')
    else:
        messagebox.showerror(title='Error!',message='Ingrese todos los campos requeridos.')

def login_pantalla():
    global user_entry2
    global pass_entry2

    frame = customtkinter.CTkFrame(app,bg_color='#001220',fg_color='#001220',width=500,height=360)
    frame.place(x=0,y=0)
    app.geometry("500x360")
    imageLogo = PhotoImage(file='images/logo.png')
    imageLogo_label = Label(frame,image=imageLogo,bg='#001220')
    imageLogo_label.place(x=0,y=0)
    frame.imageLogo = imageLogo
    
    login_label2 = customtkinter.CTkLabel(frame,font=font1,text="Inicia Sesion",text_color='#fff',bg_color='#001220')
    login_label2.place(x=280,y=20)
    
    user_entry2 = customtkinter.CTkEntry(frame,font=font2,text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3,placeholder_text='Usuario',placeholder_text_color='#a3a3a3',width=200,height=50)
    user_entry2.place(x=280,y=80)

    pass_entry2 = customtkinter.CTkEntry(frame,font=font2,show='*',text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3,placeholder_text='Contrasena',placeholder_text_color='#a3a3a3',width=200,height=50)
    pass_entry2.place(x=280,y=150)

    login_button2 = customtkinter.CTkButton(frame,command=login_account,font=font2,text_color='#fff',text='Iniciar Sesion',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=120)
    login_button2.place(x=280,y=290)
def registrate_pantalla():
    global user_entry
    global  pass_entry
    global  type_combo

    frame = customtkinter.CTkFrame(app,bg_color='#001220',fg_color='#001220',width=500,height=360)
    frame.place(x=0,y=0)
    app.geometry("500x360")
    imageLogo = PhotoImage(file='images/logo.png')
    imageLogo_label = Label(frame,image=imageLogo,bg='#001220')
    imageLogo_label.place(x=0,y=0)
    frame.imageLogo = imageLogo

    singup_label = customtkinter.CTkLabel(frame,font=font1,text="Registrate",text_color='#fff',bg_color='#001220')
    singup_label.place(x=280,y=20)

    user_entry = customtkinter.CTkEntry(frame,font=font2,text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3,placeholder_text='Usuario',placeholder_text_color='#a3a3a3',width=200,height=50)
    user_entry.place(x=280,y=80)

    pass_entry = customtkinter.CTkEntry(frame,font=font2,show='*',text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3,placeholder_text='Contrasena',placeholder_text_color='#a3a3a3',width=200,height=50)
    pass_entry.place(x=280,y=150)

    type_label = customtkinter.CTkLabel(frame,font=font3,text="Tipo de usuario",text_color='#fff',bg_color='#001220')
    type_label.place(x=280,y=210)

    type_combo = customtkinter.CTkComboBox(frame,values=['------','Medico','Paciente'],text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',button_color='#004780',dropdown_fg_color='#001a2e',dropdown_hover_color='#006e44',dropdown_text_color='#fff')
    type_combo.place(x=280,y=240)

    sigunp_button = customtkinter.CTkButton(frame,command=signup,font=font2,text_color='#fff',text='Registrate',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=120)
    sigunp_button.place(x=280,y=290)

    login_label = customtkinter.CTkLabel(frame,font=font3,text='Tienes una cuenta?',text_color='#fff',bg_color='#001220')
    login_label.place(x=280,y=330)

    login_button = customtkinter.CTkButton(frame,command=login_pantalla,font=font4,text_color='#00bf77',text='Iniciar Sesion',fg_color='#001220',hover_color='#001220',cursor='hand2',width=40)
    login_button.place(x=390,y=330)

def info_paciente():
    frame3 = customtkinter.CTkFrame(app,bg_color='#001220',fg_color='#001220',width=800,height=600)
    frame3.place(x=0,y=0)
    app.geometry("800x600")
    imageLogo = PhotoImage(file='images/logo.png')
    imageLogo_label = Label(frame3,image=imageLogo,bg='#001220')
    imageLogo_label.place(x=0,y=140)
    frame3.imageLogo = imageLogo

    global nombre_paciente
    global genero_paciente
    global peso_paciente
    global estatura_paciente
    global nacimiento_paciente
    global ss_paciente

    def regresar():
        frame3.destroy()
        menu_paciente()

    info_label = customtkinter.CTkLabel(frame3,font=font1,text="Informacion de usuario",text_color='#fff',bg_color='#001220')
    info_label.place(x=320,y=10)

    nombre_paciente = customtkinter.CTkEntry(frame3,font=font2,text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3,placeholder_text='Nombre',placeholder_text_color='#a3a3a3',width=400,height=50)
    nombre_paciente.place(x=320,y=80)

    genero_label = customtkinter.CTkLabel(frame3,font=font3,text="Sexo",text_color='#fff',bg_color='#001220')
    genero_label.place(x=320,y=150)

    genero_paciente = customtkinter.CTkComboBox(frame3,values=['------','Femenino','Masculino'],text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',button_color='#004780',dropdown_fg_color='#001a2e',dropdown_hover_color='#006e44',dropdown_text_color='#fff')
    genero_paciente.place(x=320,y=180)

    nacimiento_label = customtkinter.CTkLabel(frame3,font=font3,text="Fecha de nacimiento",text_color='#fff',bg_color='#001220')
    nacimiento_label.place(x=500,y=150)

    nacimiento_paciente = customtkinter.CTkEntry(frame3,font=font2,text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3, width=200,height=30)
    nacimiento_paciente.place(x=500,y=180)
    nacimiento_paciente.insert(0,"dd/mm/yyyy")
    nacimiento_paciente.bind("<1>", pick_date)

    peso_paciente = customtkinter.CTkEntry(frame3,font=font2,text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3,placeholder_text='Peso KG',placeholder_text_color='#a3a3a3',width=100,height=50)
    peso_paciente.place(x=320,y=240)

    estatura_paciente = customtkinter.CTkEntry(frame3,font=font2,text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3,placeholder_text='Estatura',placeholder_text_color='#a3a3a3',width=100,height=50)
    estatura_paciente.place(x=450,y=240)
    
    # nacimiento_btn = customtkinter.CTkButton(frame3,command=get_date,font=font2,text_color='#fff',text='Registrate',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=120)
    # nacimiento_btn.place(x=580,y=250)

    ss_paciente = customtkinter.CTkEntry(frame3,font=font2,text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3,placeholder_text='Numero Seguro Social',placeholder_text_color='#a3a3a3',width=400,height=50)
    ss_paciente.place(x=320,y=310)

    guardar_button = customtkinter.CTkButton(frame3,command=guardar_informacion,font=font2,text_color='#fff',text='Guardar informacion',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=120)
    guardar_button.place(x=320,y=380)

    back_btn = customtkinter.CTkButton(frame3,command=regresar,font=font3,text_color='#fff',text='Regresar',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=60)
    back_btn.place(x=0,y=0)

def info_doctor():
    frame3 = customtkinter.CTkFrame(app,bg_color='#001220',fg_color='#001220',width=800,height=600)
    frame3.place(x=0,y=0)
    app.geometry("800x600")
    imageLogo = PhotoImage(file='images/logo.png')
    imageLogo_label = Label(frame3,image=imageLogo,bg='#001220')
    imageLogo_label.place(x=0,y=140)
    frame3.imageLogo = imageLogo

    global nombre_doctor
    global especialidad_doctor

    def regresar():
        frame3.destroy()
        menu_doctor()

    info_label = customtkinter.CTkLabel(frame3,font=font1,text="Informacion de doctor",text_color='#fff',bg_color='#001220')
    info_label.place(x=320,y=10)

    nombre_doctor = customtkinter.CTkEntry(frame3,font=font2,text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3,placeholder_text='Nombre',placeholder_text_color='#a3a3a3',width=400,height=50)
    nombre_doctor.place(x=320,y=80)

    especialidad_doctor = customtkinter.CTkComboBox(frame3,values=['------','Pediatria','Gastroentereologo','General','Cardiologia'],text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',button_color='#004780',dropdown_fg_color='#001a2e',dropdown_hover_color='#006e44',dropdown_text_color='#fff')
    especialidad_doctor.place(x=320,y=150)

    guardar_button = customtkinter.CTkButton(frame3,command=guardar_informacion_doctor,font=font2,text_color='#fff',text='Guardar informacion',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=120)
    guardar_button.place(x=320,y=200)

    back_btn = customtkinter.CTkButton(frame3,command=regresar,font=font3,text_color='#fff',text='Regresar',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=60)
    back_btn.place(x=0,y=0)

def menu_paciente():
    def pick_datess(event):
        global cal

        ventana = Toplevel()
        ventana.grab_set()
        ventana.title("Ingresa fecha de nacimiento")
        ventana.geometry('250x220+590+370')

        cal = Calendar(ventana,text = "Confirmar", selectmode='day',year=2023,month=1,date_pattern="mm/dd/y")
        cal.place(x=0, y=0)
        date = cal.get_date()

        confirmar = customtkinter.CTkButton(ventana,command=grab_dates,font=font1,text_color='#fff',text='Confirmar',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=100)
        confirmar.place(x=20, y=190)

    def grab_dates():
        fecha_paciente.delete(0, END)
        fecha_paciente.insert(0, cal.get_date())

    frame = customtkinter.CTkFrame(app,bg_color='#001220',fg_color='#001220',width=800,height=600)
    frame.place(x=0,y=0)
    app.geometry("800x600")
    imageLogo = PhotoImage(file='images/logo.png')
    imageLogo_label = Label(frame,image=imageLogo,bg='#001220')
    imageLogo_label.place(x=0,y=0)
    frame.imageLogo = imageLogo

    global sintomas_paciente
    global hora_paciente
    global fecha_paciente

    def regresar():
        frame.destroy()
        login_pantalla()

    paciente_label = customtkinter.CTkLabel(frame,font=font1,text="Menu Paciente",text_color='#fff',bg_color='#001220')
    paciente_label.place(x=320,y=10)

    informacion_paciente = customtkinter.CTkButton(frame,command=info_paciente,font=font2,text_color='#fff',text='Editar informacion de paciente',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=100)
    informacion_paciente.place(x=320,y=50)

    indicaciones_paciente = customtkinter.CTkButton(frame,font=font2,text_color='#fff',text='Receta',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=30)
    indicaciones_paciente.place(x=320,y=100)
    
    agenda_label = customtkinter.CTkLabel(frame,font=font1,text="Agenda cita",text_color='#fff',bg_color='#001220')
    agenda_label.place(x=320,y=140)

    sintomas_label = customtkinter.CTkLabel(frame,font=font2,text="Sintomas",text_color='#fff',bg_color='#001220')
    sintomas_label.place(x=320,y=170)

    sintomas_paciente = customtkinter.CTkTextbox(frame,font=font3,text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3,width=400,height=150)
    sintomas_paciente.place(x=320,y=195)

    hora_label = customtkinter.CTkLabel(frame,font=font2,text="Selecciona horario",text_color='#fff',bg_color='#001220')
    hora_label.place(x=320,y=360)

    hora_paciente = customtkinter.CTkComboBox(frame,values=['------','9:00AM','10:00AM','11:00AM','12:00AM','01:00PM','02:00PM','03:00PM'],text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',button_color='#004780',dropdown_fg_color='#001a2e',dropdown_hover_color='#006e44',dropdown_text_color='#fff')
    hora_paciente.place(x=320,y=380)

    fecha_label = customtkinter.CTkLabel(frame,font=font2,text="Fecha de nacimiento",text_color='#fff',bg_color='#001220')
    fecha_label.place(x=500,y=360)

    fecha_paciente = customtkinter.CTkEntry(frame,font=font2,text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3, width=200,height=30)
    fecha_paciente.place(x=500,y=380)
    fecha_paciente.insert(0,"dd/mm/yyyy")
    fecha_paciente.bind("<1>", pick_datess)

    guarda_btn = customtkinter.CTkButton(frame,command=guarda_cita,font=font3,text_color='#fff',text='Guardar cita',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=60)
    guarda_btn.place(x=320,y=430)

    back_btn = customtkinter.CTkButton(frame,command=regresar,font=font3,text_color='#fff',text='Salir',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=60)
    back_btn.place(x=0,y=0)

def menu_doctor():
    frame = customtkinter.CTkFrame(app,bg_color='#001220',fg_color='#001220',width=800,height=600)
    frame.place(x=0,y=0)
    app.geometry("800x600")
    imageLogo = PhotoImage(file='images/logo.png')
    imageLogo_label = Label(frame,image=imageLogo,bg='#001220')
    imageLogo_label.place(x=0,y=0)
    frame.imageLogo = imageLogo

    global sintomas_paciente
    global hora_paciente
    global fecha_paciente

    def regresar():
        frame.destroy()
        login_pantalla()

    menu_label = customtkinter.CTkLabel(frame,font=font1,text="Menu Doctor",text_color='#fff',bg_color='#001220')
    menu_label.place(x=320,y=10)

    ver_pacientes = customtkinter.CTkButton(frame,font=font2,text_color='#fff',text='Ver Pacientes',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=100)
    ver_pacientes.place(x=320,y=50)

    informacion = customtkinter.CTkButton(frame,command=info_doctor,font=font2,text_color='#fff',text='Informacion de doctor',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=100)
    informacion.place(x=320,y=100)
    
    back_btn = customtkinter.CTkButton(frame,command=regresar,font=font3,text_color='#fff',text='Salir',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=60)
    back_btn.place(x=0,y=0)

frame = customtkinter.CTkFrame(app,bg_color='#001220',fg_color='#001220',width=500,height=360)
frame.place(x=0,y=0)

imageLogo = PhotoImage(file='images/logo.png')
imageLogo_label = Label(frame,image=imageLogo,bg='#001220')
imageLogo_label.place(x=0,y=0)

singup_label = customtkinter.CTkLabel(frame,font=font1,text="Inicia",text_color='#fff',bg_color='#001220')
singup_label.place(x=280,y=20)
inicio_button = customtkinter.CTkButton(frame,command=registrate_pantalla,font=font2,text_color='#fff',text='Registrate',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=120)
inicio_button.place(x=280,y=290)

app.mainloop()