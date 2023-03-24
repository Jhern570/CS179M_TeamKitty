from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import Bay
import time
import math
from search import *


root = Tk()
root.title("TeamKitty AI Project")
width_root= root.winfo_screenwidth()               
height_root= root.winfo_screenheight()               
root.geometry("%dx%d" % (width_root, height_root))
root.resizable(True,True)
 
frame_width = width_root - 500
frame_height = height_root - 400

cell_width = 7
cell_heigth = 3

containers = []
bay = Bay.Bay()
global containers_frame, cells,name_new_container, weight_new_container, name_text, weight_text
name_new_container = ""
weight_new_container =""
#containers_frame = Frame(root, width=1200, height=800)
containers_frame = Frame(root, width=frame_width, height=frame_height)
containers_frame.pack(expand="true")
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
            #pos = str(i) + ", " + str(j)                         10         5
            label = Label(containers_frame, text="No Ship", width=cell_width, height=cell_heigth,borderwidth=1, relief="solid")
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
    if bay.getBayState() == 1:
         bay.restart()
    desktop_dir = "C:\\Users\\" + os.environ.get('USERNAME') + "\\OneDrive\\Desktop"
    containers_frame.filename = filedialog.askopenfilename(initialdir=desktop_dir, title="Select A File", filetypes=(("Text documents", "*.txt"),))
    cells = bay.parseManifest(containers_frame.filename)
    updateContainerFrame(cells)
    bay.setBayState()
    jobs_drop_menu.config(state="normal")

    
def load_another_contaiener_button_click(name, weight):
      if name == "" or weight == "":
            messagebox.showinfo(title=None, message="Name or Weight is Empty")
            return   
      try:
           weight_int = int(weight)
      except:
            messagebox.showinfo(title=None, message="Enter correct weight")
            return
      if weight_int < 0 or len(weight) > 5:
           messagebox.showinfo(title=None, message="Enter correct weight")
           return
      weight = "0" * (5-len(weight)) + weight

      cells = bay.getCells()
      nodes = {}
      nodes[0] = cells

      best_position = search_load(cells)

      cells[12* best_position[0] + best_position[1]][3] = name
      cells[12* best_position[0] + best_position[1]][2] = weight
      
      nodes[1] = cells
      nodes_keys = [0,1]
      bay.setContainersNodes(nodes)
      bay.setContainersNodesKeys(nodes_keys)
      next_move_button.config(state="normal")      

def open_new_load_window():
     load = Toplevel(root)
     load.title("Load Container")
     load.geometry("350x110")
     description_label = Label(load, text="Enter the name and weight of the container you are loading")
     description_label.grid(row=0, column=0, columnspan=2)
     name_label = Label(load, text = "Enter name: ")
     name_label.grid(row=1, column= 0, padx = (0,0), pady= (5,0), columnspan= 1)
     name_text = Entry(load)
     name_text.grid(row = 1, column = 1, columnspan=1)
     weight_label = Label(load, text="Enter weight: ")
     weight_label.grid(row = 2, column=0, padx = (0,0))
     weight_text = Entry(load)
     weight_text.grid(row=2,column=1, padx = (0,0))
     load_another_container_button = Button(load, text="Add container", command = lambda: load_another_contaiener_button_click(name_text.get(), weight_text.get()))
     load_another_container_button.grid(row=3, column = 0, padx = (0, 10), pady = (10,0))
     
     
#JOB SUBMIT BUTTON WILL AUTOMATICALLY FIND THE FASTEST WAY TO DO THE JOB
def job_submit_click():
     select_txt_file_button.config(state=DISABLED)
     containers_selected = []
     if jobs_click.get() == "Unload":
          cells = bay.getCells()
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
     elif jobs_click.get() == "Load":
          #open load window
          open_new_load_window()
          return 
     elif jobs_click.get() == "Balance Ship":
          cells = bay.getCells()
          loop = True
          containers_selected = []
          balanced = False
          closest_to_deficit_left = [0,0,0,0]
          closest_to_deficit_right = [0,0,0,0]
          nodes = {}
          temp_nodes = {}
          key_pos = 0
          left_flag = 0
          right_flag = 0
          while loop:
               left_weight = calculate_side_weight(0,8,0,6,cells)
               right_weight = calculate_side_weight(0,8,6,12,cells)
               if left_weight == 0 and right_weight == 0:
                    balanced = True
                    break;
               
               balance_mass = int(math.ceil((left_weight + right_weight) / 2))

               if check_if_balance(left_weight, right_weight, balance_mass): #if return True, then ship is balanced
                    balanced = True
                    break
               deficit = abs(balance_mass - left_weight) if left_weight < right_weight else abs(balance_mass - right_weight)
               
               left_side_bay = divide_bay(cells, 0, 8, 0, 6)
               right_side_bay = divide_bay(cells, 0, 8, 6, 12)

               if left_weight > right_weight :
                    possible_to_move_list = possible_containers_to_move(left_side_bay, deficit)
                    if len(possible_to_move_list) == 0:
                         #find the closest number to deficit:
                         closest_to_deficit_left = find_closest_weight_to_deficit(left_side_bay, deficit)
                         #if repeated container movement, ship cannot be balanced
                         if left_flag == 1 and right_flag == 1:
                              nodes = {}
                              break
                         containers_selected.append(closest_to_deficit_left)
                         left_flag = 1
                    else:
                         containers_selected.append(possible_to_move_list[0])         
               else:
                    possible_to_move_list = possible_containers_to_move(right_side_bay, deficit)
                    if len(possible_to_move_list) == 0:
                         #find the closest number to deficit:
                         closest_to_deficit_right = find_closest_weight_to_deficit(right_side_bay, deficit)
                         #if repeated container movement, ship cannot be balanced
                         if left_flag == 1 and right_flag == 1:
                              nodes = {}
                              break
                         containers_selected.append(closest_to_deficit_right)
                         right_flag = 1

                    else:
                         containers_selected.append(possible_to_move_list)        
               temp_nodes = search_for_balance(cells, containers_selected, key_pos)
               if temp_nodes == None:
                    nodes = {}
                    break
               key_pos += len(list(temp_nodes.keys()))
               cells = temp_nodes[key_pos-1]
               nodes.update(temp_nodes)
               containers_selected = []
          nodes_keys = list(nodes.keys())
          if len(nodes_keys) == 0:
               messagebox.showinfo(title=None, message="Ship Cannot be Balanced!")
               jobs_drop_menu.config(state='normal')
               job_submit_button.config(state='normal')
               select_txt_file_button.config(state=NORMAL)
               bay.restart()
               return
          bay.setContainersNodes(nodes)
          bay.setContainersNodesKeys(nodes_keys)
          next_move_button.config(state = "normal")
          return


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
          bay.restart()


select_txt_file_button = Button(root, text="Select Manifest", padx=8, pady=12, command=select_txt_file_click)
select_txt_file_button.place(x=width_root-int(width_root/6), y=height_root-int(height_root/5))



jobs_drop_menu = OptionMenu(root, jobs_click, *jobs)
jobs_drop_menu.config(state="disabled")
jobs_drop_menu.place(x=width_root-int(width_root/6), y=200)

job_submit_button = Button(root, text="Submit", command=job_submit_click)
job_submit_button.place(x=width_root-int(width_root/6), y=240)

next_move_button = Button(root, text="Next Move", command=next_move_click)
next_move_button.config(state="disabled")
next_move_button.place(x=int(width_root/2), y=height_root - 200)
root.mainloop()