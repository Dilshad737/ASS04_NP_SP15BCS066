#DILSHAD ALI CHATTHA
from tkinter import *
from chat import *
from PIL import *
import thread


s = socket(AF_INET, SOCK_STREAM)
HOST = gethostname()
PORT = 9003
conn = ''
s.bind((HOST, PORT))

def onClick():
    messageText = textBox.get("0.0",END)#filter
    conn.send(messageText.encode())
    #messageText = messageText.encode()
    displayLocalMessage(chatBox, messageText) #display local
    chatBox.yview(END) #auto-scroll
    textBox.delete("0.0",END) #clear the input box
    #conn.sendall(messageText) #send over socket
    

def onEnterButtonPressed(event):
    textBox.config(state=NORMAL)
    onClick()

def removeKeyboardFocus(event):
	textBox.config(state=DISABLED)

def openConnection():
    s.listen(2) #Listen for 1 other person
    global conn
    conn, addr = s.accept()
    getConnectionInfo(chatBox, 'Connected with: ' + str(addr) + '\n-------------------------------------')

    while 1:
        try:
            data = conn.recv(1024) #Get data from clients
            data = data.decode()
            displayRemoteMessage(chatBox, data) #Display on Remote Windows

        except:
            getConnectionInfo(chatBox, '\n [ Your partner has disconnected ]\n [ Waiting for him to connect..] \n  ')
            openConnection()

    conn.close()

#Base Window
base = Tk()
base.title("Dilshad_Chat Host")
base.geometry("400x450")
base.resizable(width=FALSE, height=FALSE)
base.configure(bg="#d69595")

#Chat
chatBox = Text(base, bd=0, bg="#689099", height="8", width="20", font="Helvetica",)
chatBox.insert(END, "Waiting for your partner to connect..\n")
chatBox.config(state=DISABLED)
sb = Scrollbar(base, command=chatBox.yview, bg = "#34495e")
chatBox['yscrollcommand'] = sb.set

#Send Button
sendButton = Button(base, font="Helvetica", text="SEND", width="50", height=5,
                    bd=0, bg="#BDE096", activebackground="#BDE096", justify="center",
                    command=onClick)

#Text Input
textBox = Text(base, bd=0, bg="#F8B486",width="29", height="5", font="Helvetica")
textBox.bind("<Return>", removeKeyboardFocus)
textBox.bind("<KeyRelease-Return>", onEnterButtonPressed)

#Put everything on the window
sb.place(x=370,y=5, height=350)
chatBox.place(x=15,y=5, height=350, width=355)
sendButton.place(x=255, y=360, height=80, width=130)
textBox.place(x=15, y=360, height=80, width=250)

thread.start_new_thread(openConnection,()) # try listening again upon fail
base.mainloop() #Start the GUI Thread
