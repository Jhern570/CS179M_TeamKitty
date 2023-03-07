from tkinter import *
from tkinter import filedialog
import os
import Bay
import time
from search import *

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
     if jobs_click.get() == "Unload":
          cells = bay.getCells()
          print(len(cells))
          containers_index = bay.getIndex()
          for i in containers_index:
               containers_selected.append(cells[12*(7-i[0]) + i[1]])
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
     if len(bay.getContainersNodesKeys()) == 0:
          next_move_button.config(state="disabled")
          jobs_drop_menu.config(state='normal')
          job_submit_button.config(state='normal')
          select_txt_file_button.config(state=NORMAL)


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
root.mainloop()