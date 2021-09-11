import tkinter as tk
import tkinter.messagebox
import pickle
import time
import chat_utils as cu
import json
from chat_client_class import *
import argparse
import threading

parser = argparse.ArgumentParser(description='chat client argument')
parser.add_argument('-d', type=str, default=None, help='server IP addr')
args = parser.parse_args()

client = Client(args) 
client.init_chat()
    

window = tk.Tk()
window.title('Welcome to Chat System!')
window.geometry('450x300')

canvas = tk.Canvas(window, height=300, width=500, bg = 'darkviolet')
canvas.pack(side='top')
tk.Label(window, text='User name: ').place(x=50, y= 150)
tk.Label(window, text='Password: ').place(x=50, y= 190)
var_usr_name = tk.StringVar()
var_usr_name.set('')
entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
entry_usr_name.place(x=160, y=150)
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=160, y=190)
usr_name = ''
def usr_login():
    global usr_name
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    
    try:
        with open('usrs_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
            
    except FileNotFoundError:
        with open('usrs_info.pickle', 'wb') as usr_file:
            usrs_info = {'admin': 'admin'}
            pickle.dump(usrs_info, usr_file)
            
    if usr_name in usrs_info:
        
        if usr_pwd == usrs_info[usr_name]:
            ok = tk.messagebox.showinfo(title='Welcome', message='Chat away! ' + usr_name) 
            client.login(usr_name)
            if ok == 'ok':
                chat()
                
        else:
            tk.messagebox.showerror(message='Your password is wrong, try again.')
    else:
        is_sign_up = tk.messagebox.askyesno('You have not signed up yet. Sign up now?')
        
        if is_sign_up:
            usr_sign_up()

            
def usr_sign_up():
    def sign_to_Chat_System():
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        nn = new_name.get()
        with open('usrs_info.pickle', 'rb') as usr_file:
            exist_usr_info = pickle.load(usr_file)
        if np != npf:
            tk.messagebox.showerror('Error', 'Password and confirm password must be the same!')
        elif nn in exist_usr_info:
            tk.messagebox.showerror('Error', 'The user has already signed up!')
        else:
            exist_usr_info[nn] = np
            with open('usrs_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            tk.messagebox.showinfo('Welcome', 'You have successfully signed up!')
            window_sign_up.destroy()
            
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('350x200')
    window_sign_up.title('Sign up window')
    canvas = tk.Canvas(window_sign_up, height=300, width=500, bg = 'darkviolet')
    canvas.pack(side='top')

    new_name = tk.StringVar()
    new_name.set('')
    tk.Label(window_sign_up, text='User name: ').place(x=10, y= 10)
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
    entry_new_name.place(x=150, y=10)

    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='Password: ').place(x=10, y=50)
    entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_usr_pwd.place(x=150, y=50)

    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='Confirm password: ').place(x=10, y= 90)
    entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_usr_pwd_confirm.place(x=150, y=90)

    btn_comfirm_sign_up = tk.Button(window_sign_up, text='Sign up', command=sign_to_Chat_System)
    btn_comfirm_sign_up.place(x=150, y=130)

btn_login = tk.Button(window, text='Login', command=usr_login)
btn_login.place(x=170, y=230)
btn_sign_up = tk.Button(window, text='Sign up', command=usr_sign_up)
btn_sign_up.place(x=270, y=230)


def chat():     
    window.destroy()
    window_chat = tk.Tk()
    window_chat.geometry('800x500')
    window_chat.title('Chat window')

    f_msglist = tk.Frame(window_chat)
    f_msgsend = tk.Frame(window_chat)
    f_floor = tk.Frame(window_chat)
    f_show = tk.Frame(window_chat)
    
    def msgsend():
        msg = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'\n'
        txt_msglist.insert(tk.END,str(usr_name) + ' ' + msg,'green')
        txt_msglist.insert(tk.END,txt_msgsend.get('0.0',tk.END),'green')
        string = str(txt_msgsend.get('0.0',tk.END)[:-1])

        if string == 'q':
            window_chat.destroy()


    #        client.system_msg = ''   
        else:            
#            txt_msglist.insert(tk.END,client.proc(string) + '\n')
#            client.output()
#            txt_msgsend.delete('0.0',tk.END)
            client.console_input.append(string)
#        client.proc()
#        txt_msglist.insert(tk.END,client.proc() + '\n')
#        client.system_msg = ''   
#        client.output()
            txt_msgsend.delete('0.0',tk.END)
    
    def refresh():
        while True:
#            msg = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'\n'
#            txt_msglist.insert(tk.END,str(usr_name) + ' ' + msg,'green')
            client.run_chat()
            if client.system_msg != '':
                txt_msglist.insert(tk.END,client.system_msg + '\n')
#                client.console_input.append(client.system_msg)
#            
                client.output()
#        string = str(txt_msgsend.get('0.0',tk.END)[:-1])
#        if len(client.proc(string)) > 0:
#            txt_msglist.insert(tk.END,client.proc() + '\n')
##            client.system_msg = ''
#            client.output()
#            txt_msgsend.delete('0.0',tk.END)
#
##        while True:
##            peer_msg = client.get_msgs()
##            if len(peer_msg) > 0 :
##                txt_msglist.insert(tk.END,client.proc('') + '\n')
##                client.output()
#    def sendMsgEvent(event):        #发送消息事件
#        if event.keysym == "Return":  #按回车键可发送
#          refresh()
            
    def cancel():
        txt_msgsend.delete('0.0',tk.END)

    txt_msglist = tk.Text(f_msglist, font=("Times", "15"), 
               width=60,height=20,
               spacing2=5,                          
               bd=2,                         
               padx=5,pady=5)   
                             
    txt_msglist.tag_config('green',foreground = 'blue') 
    
    txt_msgsend = tk.Text(f_msgsend,font=("Times", "15"), 
               width=60,height=5,                 
               spacing2=5,                       
               bd=2,                      
               padx=5,pady=5) 
    
#    txt_msgsend.bind("<KeyPress-Return>", sendMsgEvent)
#    while True:
#        peer_msg = client.get_msgs()
#        if len(peer_msg) > 0 :
#            txt_msglist.insert(tk.END,client.proc('') + '\n')
#            client.output()
#        time.sleep(60)
#    start_thread = threading.Thread(target = t1)
    reading_thread = threading.Thread(target = refresh)
    reading_thread.daemon = True
#    start_thread.start()
    reading_thread.start()
    
    
    button_send = tk.Button(f_floor,text = 'Send',command = msgsend)
    button_cancel = tk.Button(f_floor,text = 'Cancel',command = cancel) 
#    button_refresh = tk.Button(f_floor,text = 'Refresh',command = refresh)

    
    txt_show = tk.Text(f_show,font=("Times", "15"),  
               width=30,height=20,                  
               spacing2=5,              
               bd=2,                             
               padx=5,pady=5)    
    
    txt_show.insert(tk.END,cu.menu)
    
    f_msglist.grid(row = 0,column = 0 ) 
    f_msgsend.grid(row = 1,column = 0)  
    f_floor.grid(row = 2,column = 0)   
    f_show.grid(row = 0, column = 1)
    
    txt_msglist.grid()  
    txt_msgsend.grid() 
    txt_show.grid()
    button_send.grid(row = 0,column = 0)
    button_cancel.grid(row = 0,column = 1)
#    button_refresh.grid(row = 0,column = 2)
    
    tk.mainloop()

window.mainloop()    
