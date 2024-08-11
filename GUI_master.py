import tkinter as tk
from PIL import Image , ImageTk  
 

##############################################+=============================================================
python_executable = r"C:\Path\To\Your\Python\python.exe"
 
root = tk.Tk()
#root.configure(background="seashell2")
#root.geometry("1300x700")
import sqlite3
my_conn = sqlite3.connect('face.db')

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title(" Image and Video metadata Using AI and Image Processing ")


#++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
image2 =Image.open('H.jpg')
image2 =image2.resize((w,h), Image.NEAREST)

background_image=ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0) #, relwidth=1, relheight=1)



  #################################################################################################################
def reg():
    print("Image Metadata")
    from subprocess import call
    call(["python", "image_Metadata3.py"]) 



def Log():
    print("Video Metadata")
    from subprocess import call
    call(["python", "final.py"]) 
    
    
    
def sem():
    print("Youtube Metadata")
    from subprocess import call
    call(["python", "video_Metadata3.py"]) 




def window():
    root.destroy()


button1 = tk.Button(root, text="Image Metadata", command=reg,width=20, height=1, font=('times', 15, ' bold '),bg="brown",fg="white")
button1.place(x=400, y=410)

button2 = tk.Button(root, text="Video Metadata", command=Log,width=20, height=1, font=('times', 15, ' bold '),bg="green",fg="white")
button2.place(x=750, y=410)


button2 = tk.Button(root, text="Youtube Metadata", command=sem,width=20, height=1, font=('times', 15, ' bold '),bg="green",fg="white")
button2.place(x=70, y=410)

  # Adjusted x-coordinate for left placement


#
#button5 = tk.Button(frame_alpr, text="button5", command=window,width=20, height=1, font=('times', 15, ' bold '),bg="yellow4",fg="white")
#button5.place(x=10, y=280)


exit = tk.Button(root, text="Exit", command=window, width=20, height=1, font=('times', 15, ' bold '),bg="red",fg="white")
exit.place(x=1090, y=410)



root.mainloop()