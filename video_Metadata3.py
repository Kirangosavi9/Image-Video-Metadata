import tkinter as tk
from tkinter import ttk, scrolledtext
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
from PIL import Image, ImageTk
from PIL import Image

# Replace 'YOUR_API_KEY' with your actual YouTube Data API key
API_KEY = 'AIzaSyCJf1CyQuxlVtjvbYym66rCB-p40tLK0Ws'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def format_video_metadata(metadata):
    formatted_data = "Video Metadata:\n"
    for key, value in metadata.items():
        formatted_data += f"{key}: {value}\n"
    return formatted_data

def get_youtube_video_data(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    request = youtube.videos().list(part='snippet,statistics', id=video_id)
    response = request.execute()
    return response['items'][0] if response['items'] else None

def extract_video_id(youtube_url):
    query = urlparse(youtube_url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None

def display_metadata_in_window(youtube_url, output_text):
    video_id = extract_video_id(youtube_url)
    if video_id:
        youtube_video_data = get_youtube_video_data(video_id)
        if youtube_video_data:
            metadata = {
                "YouTube Video Title": youtube_video_data['snippet']['title'],
                "YouTube Channel": youtube_video_data['snippet']['channelTitle'],
                "Upload Date": youtube_video_data['snippet']['publishedAt'],
                "View Count": youtube_video_data['statistics']['viewCount'],
                "Like Count": youtube_video_data['statistics']['likeCount'],
                "Dislike Count": youtube_video_data['statistics'].get('dislikeCount', "N/A"),
                "Comment Count": youtube_video_data['statistics'].get('commentCount', "N/A"),
                "Description": youtube_video_data['snippet'].get('description', "N/A")
            }
            metadata_text = format_video_metadata(metadata)
            output_text.insert(tk.END, metadata_text)
            output_text.insert(tk.END, "\n")  # Add a newline for better readability
        else:
            output_text.insert(tk.END, "Error: Could not fetch video data from YouTube.\n")
    else:
        output_text.insert(tk.END, "Error: Invalid YouTube URL.\n")

def select_video():
    """Allows the user to input a YouTube URL to display video metadata."""
    youtube_url = input_url.get()
    if youtube_url:
        output_text.delete(1.0, tk.END)  # Clear previous output
        display_metadata_in_window(youtube_url, output_text)

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    root.title("Video Metadata Viewer")
    root.configure(bg='#1b1b1b')  # Set background color to black

    style = ttk.Style()
    style.configure("TButton", font=("Courier", 12, "bold"))

    w, h = 1600, 900  # Set the desired width and height

    image2 = Image.open('D.jpg')
    image2 = image2.resize((w, h), Image.NEAREST)

    background_image = ImageTk.PhotoImage(image2)

    background_label = tk.Label(root, image=background_image)

    background_label.image = background_image

    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create and pack the input field
    input_url_label = tk.Label(root, text="Enter a YouTube URL:", bg='#1b1b1b', fg='white', font=('Arial', 15))
    input_url_label.pack(pady=10)
    input_url = tk.Entry(root, bg='white', fg='black', font=('Arial', 15))  # Set font size to 12
    input_url.pack(pady=10)
    # Create a style and configure the font for the TButton style
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 13))
    # Create the scrolled text widget to display metadata
    output_text = scrolledtext.ScrolledText(root, width=100, height=30, bg='white', fg='black')  # Set background color to green and text color to black
    output_text.pack(pady=20)

    # Create and pack the button to display metadata
    select_button = ttk.Button(root, text="Display Metadata", command=select_video, style='TButton', width=20)
    select_button.pack(pady=200, ipady=40)
    select_button.place(x=75, y=570)  # Run the Tkinter event loop

    # Set x and y coordinates to move the button to a specific position
    select_button.place(relx=0.2, rely=0.1)

    exit_button = ttk.Button(root, text="Exit", command=root.destroy, style='TButton', width=20)
    exit_button.place(relx=0.66, rely=0.05, anchor="ne")  # Adjust relx and rely for the desired position
    exit_button.place(x=75, y=600)  # Run the Tkinter event loop
    root.mainloop()
