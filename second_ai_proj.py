from tkinter import *
from tkinter import filedialog
import os
import Bay
import time
from search import *
import logging

root = Tk()
root.title("TeamKitty AI Project")
width= root.winfo_screenwidth()               
height= root.winfo_screenheight()               
root.geometry("%dx%d" % (width, height))
root.resizable(False,False)
 
#FRAME FOR CONTAINERS VIEW
containers = []
bay = Bay.Bay()
global containers_frame, cells
containers_frame = Frame(root, width=1200, height=800)
containers_frame.pack()
containers_frame.place(anchor='center', bordermode=INSIDE, relx=0.5, rely=0.5)

#DROP OF MENU FOR TYPE OF JOB OPTIONS
jobs = ["Load", "Unload", "Balance Ship"]
jobs_click = StringVar()
jobs_click.set("Select Job")

#USER STACK: keeps track of who is logged in
user = []

#LOG FILE
logging.basicConfig(filename='log.log', format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)

def select_container_click(event):
     label_info = event.widget.grid_info()
     if event.widget.cget("text") == "No Ship" or event.widget.cget("text") == "UNUSED" or event.widget.cget("text") == "NAN": 
          print('RETURN')
          return
     x = label_info['row']
     y = label_info['column']
     container_index = [x,y]
     bay.appendIndex(container_index)
     containers[12*x+y].config(bg="green")

for i in range(8):
        for j in range(12):
            #pos = str(i) + ", " + str(j)
            label = Label(containers_frame, text="No Ship", width=10, height=5,borderwidth=1, relief="solid")
            label.grid(row=i, column=j)
            label.bind('<Button-1>', select_container_click)
            containers.append(label)

#UPDATE FRAME OF CONTAINERS
def updateContainerFrame(cells):
    a = 0
    b = 0
    for i in range(7,-1,-1):
         for j in range(0,12):
            containers[12*a+b].config(text=cells[12*i+j][3])
            if containers[12*a+b].cget("text") != "UNUSED":
                 if containers[12*a+b].cget("text") == "NAN":
                      containers[12*a+b].config(bg="black") 
                 else:
                      containers[12*a+b].config(bg="red")
            else:
                containers[12*a+b].config(bg="SystemButtonFace")
            b += 1 
         a+=1
         b = 0
#CLICK EVENT FOR SELECTING MANAFEST FILE
def select_txt_file_click():
    desktop_dir = "C:\\Users\\" + os.environ.get('USERNAME') + "\\OneDrive\\Desktop"
    containers_frame.filename = filedialog.askopenfilename(initialdir=desktop_dir, title="Select A File", filetypes=(("Text documents", "*.txt"),))
    cells = bay.parseManifest(containers_frame.filename)
    updateContainerFrame(cells)
    jobs_drop_menu.config(state="normal")
    
#JOB SUBMIT BUTTON WILL AUTOMATICALLY FIND THE FASTEST WAY TO DO THE JOB
def job_submit_click():
     select_txt_file_button.config(state=DISABLED)
     containers_selected = []
     global unload # used for logging unload movement everytime screen is updated
     if jobs_click.get() == "Unload":
          cells = bay.getCells()
          print(len(cells))
          containers_index = bay.getIndex()
          for i in containers_index:
               containers_selected.append(cells[12*(7-i[0]) + i[1]])
          unload = containers_selected
          containers_nodes = search(cells, containers_selected)
          #nodes_keys = list(bay.getContainersNodes().keys())
          #updateContainerFrame(containers_nodes[nodes_keys[-1]])
          bay.setContainersNodes(containers_nodes)
          node_keys = list(bay.getContainersNodes().keys())
          bay.setContainersNodesKeys(node_keys)
          next_move_button.config(state="normal")
     elif jobs_drop_menu.cget() == "Select Job":
        print("Select job")


#Button press shows the container to move
def next_move_click():
     updateContainerFrame(bay.getNextContainersNodes())
     if jobs_click.get() == "Unload" and len(unload):
          logging.info(f"Unloaded {str(unload.pop(0))}.")
     if len(bay.getContainersNodesKeys()) == 0:
          next_move_button.config(state="disabled")
          jobs_drop_menu.config(state='normal')
          job_submit_button.config(state='normal')
          select_txt_file_button.config(state=NORMAL)

def log(case):
     if case == 1:
          # user is logging in
          if user and len(str(username_entry.get())):
               logging.info(user.pop() + " has logged out")
               username_entry.delete(0,END)
          if not user and len(str(username_entry.get())):
               log_button.config(state="normal")
               logging.info(username_entry.get() + " has logged in") 
               user.append(username_entry.get()) 
               username_entry.delete(0,END)
     elif case == 2:
          # user is logging a comment
          if len(str(log_text_box.get("1.0", "end-1c"))) and len(user):
               logging.info(f'{user[0]}: "{log_text_box.get("1.0", "end-1c")}"')
               log_text_box.delete("1.0","end")
     elif case == 3:
          # atomic movement is logged
          print("logging move") 

select_txt_file_button = Button(root, text="Select Manifest", padx=8, pady=12, command=select_txt_file_click)
select_txt_file_button.place(x=width-int(width/6), y=height-int(height/5))



jobs_drop_menu = OptionMenu(root, jobs_click, *jobs)
jobs_drop_menu.config(state="disabled")
jobs_drop_menu.place(x=width-int(width/6), y=200)

job_submit_button = Button(root, text="Submit", command=job_submit_click)
job_submit_button.place(x=width-int(width/6), y=240)

next_move_button = Button(root, text="Next Move", command=next_move_click)
next_move_button.config(state="disabled")
next_move_button.place(x=int(width/2), y=height - 200)

# BUTTONS FOR LOGGING INFORMATION
username_label = Label(root, text="Name:")
username_entry = Entry(root)
login_button = Button(root, text="Login", command=lambda: log(1))
log_button = Button(root, text="Post Log", command=lambda: log(2))
log_text_box = Text(root, width=25, height=5)
text_label = Label(root, text = "Log")

log_button.config(state="disabled")

username_label.grid(row=2,column=0, pady=10)
username_entry.grid(row=2,column=1, pady=10)
login_button.grid(row=3,column=0, columnspan=1, pady=10)
log_button.grid(row=3,column=1, columnspan=2, padx=25 ,pady=10)
text_label.grid(row=0, column=0, columnspan=2, padx=20)
log_text_box.grid(row=1,column=0, columnspan=2, padx=20)
root.mainloop()
