import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image, ImageTk
from PIL.ExifTags import TAGS, GPSTAGS
import os
import socket
import platform
import datetime
import win32api

BACKGROUND_IMAGE_PATH = r"D:\image-metadata-extractor-master\reg1.jpg"



def get_exif_data(image_path):
    """Extracts EXIF data or general file properties from the given image file."""
    properties = {}
    try:
        with Image.open(image_path) as img:
            info = img._getexif()
            if info is not None:
                for tag, value in info.items():
                    decoded_tag = TAGS.get(tag, tag)
                    if decoded_tag == 'GPSInfo':
                        gps_data = {}
                        for gps_tag in value:
                            sub_decoded_tag = GPSTAGS.get(gps_tag, gps_tag)
                            gps_data[sub_decoded_tag] = value[gps_tag]
                        properties[decoded_tag] = gps_data
                    else:
                        properties[decoded_tag] = value
            else:
                print("No EXIF data found in the image.")
    except (IOError, AttributeError, KeyError, IndexError) as err:
        print("Error:", err)

    if not properties:
        # Fetch general file properties if no EXIF data
        properties['File Type'] = os.path.splitext(image_path)[1]
        properties['Open With'] = os.path.splitext(image_path)[1][1:].upper()
        properties['Location'] = os.path.dirname(image_path)
        properties['Size'] = os.path.getsize(image_path)
        properties['Size on Disk'] = os.path.getsize(image_path)
        properties['Created'] = datetime.datetime.fromtimestamp(os.path.getctime(image_path))
        properties['Modified'] = datetime.datetime.fromtimestamp(os.path.getmtime(image_path))
        properties['Accessed'] = datetime.datetime.fromtimestamp(os.path.getatime(image_path))

        if platform.system() == 'Windows':
            attributes = win32api.GetFileAttributes(image_path)
            properties['Attributes'] = attributes
        else:
            properties['Attributes'] = "N/A"

    return properties


def format_exif_data(exif_data):
    """Formats the EXIF data into a readable string."""
    formatted_data = ""
    for tag, value in exif_data.items():
        if isinstance(value, dict):
            formatted_data += f"\n{tag}:"
            for sub_tag, sub_value in value.items():
                if tag == 'GPSInfo' and sub_tag in ('GPSLatitudeRef', 'GPSLongitudeRef', 'GPSLatitude', 'GPSLongitude', 'GPSTimeStamp'):
                    # Set the text color for specified GPSInfo fields as bold black
                    formatted_data += f"\n  \033[1;30m{sub_tag}:\033[0m {sub_value}"
                else:
                    formatted_data += f"\n  {sub_tag}: {sub_value}"
        else:
            formatted_data += f"\n{tag}: {value}"
    return formatted_data
def format_file_properties(properties):
    """Formats file properties into a readable string."""
    formatted_data = "File Properties:\n"
    for key, value in properties.items():
        formatted_data += f"{key}: {value}\n"
    return formatted_data

def set_background_image(root, image_path):
    """Sets the background image of the GUI window."""
    try:
        # Open the image file
        img = Image.open(image_path)

        # Convert the image to RGB mode (if not already)
        img = img.convert('RGB')

        # Save the image in a temporary format compatible with Tkinter
        temp_path = "temp.ppm"
        img.save(temp_path, format="PPM")

        # Create a PhotoImage from the temporary file
        photo = ImageTk.PhotoImage(file=temp_path)

        # Create a label with the PhotoImage
        label = tk.Label(root, image=photo)
        label.place(relwidth=1, relheight=1)

        # Ensure the image is not garbage-collected
        root.image = photo

        # Remove the temporary file
        os.remove(temp_path)
    except Exception as e:
        print("Error setting background image:", e)


def exit_application(root):
    """Exits the application and returns to the main window."""
    root.destroy()



def generate_ip():
    """Generates a specific format of a IP address."""
    # Generate random numbers for the last three segments of the IP address
    random_numbers = [str(socket.inet_ntoa(os.urandom(4))) for _ in range(3)]
    # Extract the first three segments of the randomly generated IP and use them as-is
    fixed_segments = ".".join(random_numbers[0].split('.')[:3])
    return f"192.{fixed_segments}"


def select_image():
    """Opens a file dialog to select an image file."""
    file_path = filedialog.askopenfilename()
    if file_path:
        exif_data = get_exif_data(file_path)
        metadata_text = format_exif_data(exif_data)
        # Generate a specific format of a random IP address
        _ip = generate_ip()
        display_metadata(file_path, metadata_text, _ip)


def display_metadata(image_path, metadata_text, _ip):
    """Displays image metadata and file properties in a GUI window."""
    root = tk.Tk()
    root.geometry("800x600")  # Adjust the window size

    # Set background color to black for the main window
    root.configure(bg="black")

    # Set background image
    set_background_image(root, BACKGROUND_IMAGE_PATH)

    # Create a frame for the scroll pane with a light green background
    frame = tk.Frame(root, bg="#90ee90")
    frame.place(relwidth=1, relheight=1, relx=0, rely=0)

    # Add text at the upper middle with black color outside the scroll pane
    text_label = tk.Label(root, text="METADATA", font=("Courier", 16, "bold"), fg="black", bg="#90ee90")
    text_label.place(relx=0.5, rely=0.05, anchor="center")

    # Display the metadata in a scrolled text widget with black text on light green background
    text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20, font=("Courier", 12), fg="black", bg="#90ee90")
    text_widget.insert(tk.INSERT, metadata_text + f"IP Address: {_ip}")  # Insert the IP address
    text_widget.pack(padx=10, pady=10)

    # Add exit button at the bottom with black color
    exit_button = tk.Button(frame, text="Exit", command=lambda: exit_application(root), font=("Courier", 12, "bold"), fg="#90ee90", bg="black", height=2, width=10)
    exit_button.place(relx=0.5, rely=0.95, anchor="center")

    # Run the GUI main loop
    root.mainloop()


if __name__ == "__main__":
    # Add a button to select an image
    root = tk.Tk()
    root.title("Image Metadata Viewer")

    # Set the background color to white
    root.configure(bg="white")

    select_button = tk.Button(root, text="Select Image", command=select_image, font=("Courier", 20),
                              fg="#90ee90", bg="black")
    select_button.pack(pady=300, padx=10)  # Adjust pady and padx to increase the height and width

    root.mainloop()