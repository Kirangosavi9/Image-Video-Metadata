import subprocess
import json
import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image, ImageTk

BACKGROUND_IMAGE_PATH = r"D:\image-metadata-extractor-master\reg1.jpg"


def get_exiftool_path():
    return os.path.join("C:", "exiftool", "exiftool.exe")



def extract_video_metadata(video_filepath):
    exiftool_path = get_exiftool_path()

    # Example: Extract all metadata using exiftool
    exiftool_command = [
        exiftool_path,
        "-json",
        video_filepath
    ]

    try:
        result = subprocess.run(exiftool_command, capture_output=True, text=True, check=True)
        metadata_json = result.stdout.strip()
        metadata = json.loads(metadata_json)

        # Access and print all metadata attributes
        for tag in metadata[0]:
            print(f"{tag}: {metadata[0][tag]}")
        return metadata[0]  # Return the metadata dictionary
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None


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


def format_video_metadata(video_metadata):
    """Formats video metadata into a readable string."""
    formatted_data = "Video Metadata:\n"
    for key, value in video_metadata.items():
        if key == 'Resolution':
            formatted_data += f"{key}: {value[0]}x{value[1]}\n"
        else:
            formatted_data += f"{key}: {value}\n"

    # Check if 'Model' key is present in the metadata
    if 'Model' in video_metadata:
        formatted_data += f"Camera Model: {video_metadata['Model']}\n"

    return formatted_data


def display_metadata(file_path, metadata_text):
    """Displays file properties in a GUI window."""
    root = tk.Tk()
    root.geometry("800x600")  # Adjust the window size
    root.state('zoomed')  # Maximize the window

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
    text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20, font=("Courier", 12), fg="black",
                                            bg="#90ee90")
    text_widget.insert(tk.INSERT, metadata_text)
    text_widget.pack(padx=10, pady=10)

    # Add exit button at the bottom with black color
    exit_button = tk.Button(frame, text="Exit", command=lambda: exit_application(root),
                            font=("Courier", 12, "bold"), fg="#90ee90", bg="black", height=2, width=10)
    exit_button.place(relx=0.5, rely=0.95, anchor="center")

    # Run the GUI main loop
    root.mainloop()


def exit_application(root):
    """Exits the application and returns to the main window."""
    root.destroy()


def select_video(root):
    """Opens a file dialog to select a video file."""
    root.withdraw()  # Hide the main window temporarily
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Video",
                                           filetypes=(("Video files", "*.mp4;*.avi"), ("All files", "*.*")))
    root.deiconify()  # Show the main window back

    if file_path:
        video_metadata = extract_video_metadata(file_path)
        if video_metadata:
            metadata_text = format_video_metadata(video_metadata)
            display_metadata(file_path, metadata_text)


if __name__ == "__main__":
    # Add a button to select a video
    root = tk.Tk()
    root.title("Video Metadata Viewer")

    # Set the background color to white
    root.configure(bg="white")

    select_button = tk.Button(root, text="Select Video", command=lambda: select_video(root), font=("Courier", 20),
                              fg="#90ee90", bg="black")
    select_button.pack(pady=300, padx=10)  # Adjust pady and padx to increase the height and width

    root.mainloop()
