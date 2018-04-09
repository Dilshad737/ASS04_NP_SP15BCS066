#DILSHAD ALI CHATTHA
from tkinter import *
from chat import *
from PIL import *
import thread
import tkinter.messagebox
import tkinter.filedialog as fdialog



HOST = gethostname()
PORT = 9003
s = socket(AF_INET, SOCK_STREAM)

def onClick():
    messageText = textBox.get("0.0",END) 
    s.send(messageText.encode()) #send over socket

    displayLocalMessage(chatBox, messageText) #display local
    chatBox.yview(END) #auto-scroll
    textBox.delete("0.0",END) #clear the input box

def onEnterButtonPressed(event):
    textBox.config(state=NORMAL)
    onClick()

def removeKeyboardFocus(event):
	textBox.config(state=DISABLED)

def ReceiveData():
    try:
        s.connect((HOST, PORT))
        getConnectionInfo(chatBox, '[ Connected! ]\n-------------------------------------')
    except:
        getConnectionInfo(chatBox, '[ Cannot connect ]')
        return

    while 1:
        try:
            data = s.recv(1024)
            data = data.decode()
        except:
            getConnectionInfo(chatBox, '\n [ Your partner left.] \n')
            break
        if data != '':
            displayRemoteMessage(chatBox, data)

        else:
            getConnectionInfo(chatBox, '\n [ Your partner left. ] \n')
            break
    s.close()


#Base Window
base = Tk()
base.title("Dilshad_Chat Client")
base.geometry("400x450")
base.resizable(width=FALSE, height=FALSE)
base.configure(bg="#d69595")

#Chat
chatBox = Text(base, bd=0, bg="#259eba", height="8", width="20", font="Helvetica",)
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

thread.start_new_thread(ReceiveData,())
base.mainloop()
