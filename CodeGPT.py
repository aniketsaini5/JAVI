import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import google.generativeai as genai
import os
import webbrowser
import subprocess
from datetime import datetime
import requests
import pywhatkit as kit
import pyttsx3


# Example contact list as a dictionary
contact_list = {
    "ajay": "+917027288903",
    "vikram": "+918950899252",
    "goutam":"+918295840276",
    "sahil":"+91056100259",
}    


# Set your API keys
os.environ["API_KEY"] = "AIzaSyBoLYxNErACSEfILLt06CjpszYkAnEr_6o"
WEATHER_API_KEY = "3582913f081af70564f5d6932d35d496"

# Configure the Generative AI model
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Optional: Select the first voice (you might need to experiment)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change index if necessary
engine.setProperty('rate', 155)  # Speed of speech
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

def generate_content(prompt):
    response = model.generate_content(prompt)
    return response.text

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            entry.delete(0, tk.END)
            entry.insert(0, text)
            process_query()
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Sorry, I could nopipt understand the audio.")
        except sr.RequestError:
            messagebox.showerror("Error", "Sorry, the API is not available.")

def process_query():
    # Clear the existing response before processing the new query
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.config(state=tk.DISABLED)
    
    query = entry.get()
    if query:
        if 'open' in query.lower():
            open_windows_app(query)
        elif 'play music' in query.lower()  or 'play song'in query.lower():
            play_music_on_youtube(query)
        elif 'time' in query.lower() or 'what is time' in query.lower() or 'time please' in query.lower() or 'time is ' in query.lower():
            show_time()
        elif 'weather in' in query.lower():
            get_weather(query)
        elif 'write a code' in query.lower()  or  'write code' in query.lower() or  'give code' in query.lower(): 
            try:
                response = generate_content(query)
                display_response_code(response)
                engine.say("Your code is here")
                engine.runAndWait()  
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        elif 'who are you' in query.lower():   
            response = "I am Javi"
            display_response_code(response)
            engine.say(response)
            engine.runAndWait()
        elif 'Hello JAVI' in query.lower():   
            response = "Hello , how can i help you"
            display_response_code(response)
            engine.say(response)
            engine.runAndWait()
                    
        elif 'how are you feeling' in query.lower()  or 'how are you' in query.lower() or 'how r u' in query.lower():
            response = "I am Good 😊,What about you?"
            display_response_code(response)
            engine.say(response)
            engine.runAndWait() 
                    
        
        # Check for sending message command
        elif 'send message' in query.lower():
            try:
                # Example queries:
                # 1. "send message to +1234567890 Hello there!"
                # 2. "send message to John Hello there!"

                parts = query.lower().split('to ', 1)  # Split into two parts: before and after 'to'

                if len(parts) > 1:
                    contact_info = parts[1].split(' ', 1)  # Split into contact (number/name) and message
                    if len(contact_info) == 2:
                        contact = contact_info[0].strip()  # Extract contact (number or name)
                        message = contact_info[1].strip()  # Extract the message

                        # Check if contact is in the contact list
                        if contact in contact_list:
                            phone_number = contact_list[contact]
                            kit.sendwhatmsg_instantly(phone_number, message)
                            display_response(f"Message sent to {contact} ({phone_number}): {message}")
                        elif contact.startswith('+') and contact[1:].isdigit():
                            # If contact is a valid phone number
                            kit.sendwhatmsg_instantly(contact, message)
                            display_response(f"Message sent to {contact}: {message}")
                        else:
                            display_response(
                                f"Contact '{contact}' not found in your contact list. "

                            )
                    else:
                        display_response("Could not understand the message format. Please provide it in the format: 'send message to [number/name] [your message]'")
                else:
                    display_response("Could not find 'to' in the message. Please provide it in the format: 'send message to [number/name] [your message]'")
            except Exception as e:
                display_response(f"Failed to send message: {str(e)}")

 

        elif 'my contacts' in query.lower() or 'my contact list' in query.lower():
            display_response(f"Your contacts are: {contact_list}")   
        
        else:
            try:
                response = generate_content(query)
                display_response(response)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")



# Function to add a contact to the contact list
def add_contact(name, number):
    contact_list[name.lower()] = number
    return f"Contact '{name}' added successfully with number {number}."


def display_response_code(response):
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    
    # Configure text formatting tags specifically for code
    result_text.tag_configure('code', font=('Courier', 12, 'normal'), foreground='black')
    result_text.tag_configure('bold_code', font=('Courier', 12, 'bold'))
    
    # Split the response into lines for better formatting
    lines = response.split('\n')
    for line in lines:
        if line.startswith('**') and line.endswith('**'):  # Bold code lines
            result_text.insert(tk.END, line[2:-2] + '\n', 'bold_code')
        else:  # Regular code lines
            result_text.insert(tk.END, line + '\n', 'code')
    
    result_text.config(state=tk.DISABLED)

def open_windows_app(query):
    apps = {
        'notepad': r'C:\Windows\System32\notepad.exe',
        'calculator': r'C:\Windows\System32\calc.exe',
        'word': r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
        'excel': r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE',
        'powerpoint': r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE',
        'outlook': r'C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE',
        'onenote': r'C:\Program Files\Microsoft Office\root\Office16\ONENOTE.EXE',
        'access': r'C:\Program Files\Microsoft Office\root\Office16\MSACCESS.EXE',
        'publisher': r'C:\Program Files\Microsoft Office\root\Office16\MSPUB.EXE',
        'edge': r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        'brave': r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
        'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        'youtube': 'https://www.youtube.com',
        'whatsapp': 'https://web.whatsapp.com',
        'instagram': 'https://www.instagram.com',
        'twitter': 'https://twitter.com',
        'linkedin': 'https://www.linkedin.com',
        'erp': 'https://geetauniversity.com/',
        'leetcode': 'https://leetcode.com/',                    
        'gfg': 'https://www.geeksforgeeks.org/',
        'github': 'https://github.com/login',
        'chatgpt': 'https://chatgpt.com/'
    }

    query_lower = query.lower()
    for app in apps:
        if app in query_lower:
            try:
                if 'http' in apps[app]:  # Check if it's a URL
                    webbrowser.open(apps[app])
                else:
                    subprocess.Popen(apps[app])
                display_response(f"Opening {app.capitalize()}")
                return
            except FileNotFoundError:
                display_response(f"Could not open {app.capitalize()}. Is it installed?")
                return
    
    display_response("Sorry, I couldn't find the app you requested.")
def show_time():
    now = datetime.now()
    current_time = now.strftime("%I:%M:%S %p")
    display_response(f"The current time is {current_time}")
    
def get_youtube_video_url(query):
    api_key = 'AIzaSyCTQb2KRaoih-nNX8WqCBZRCLO08DPLdAY'
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query.replace(' ', '+')}&key={api_key}&type=video&maxResults=1"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()
        if data['items']:
            video_id = data['items'][0]['id']['videoId']
            return f"https://www.youtube.com/watch?v={video_id}"
        else:
            return None
    except Exception as e:
        print(f"Error fetching YouTube video URL: {str(e)}")
        return None

def play_music_on_youtube(query):
    search_query = query.replace('play music', '').strip()
    if search_query:
        try:
            video_url = get_youtube_video_url(search_query)
            if video_url:
                webbrowser.open(video_url)
                display_response(f"Opening '{search_query}' on YouTube. Please click 'Play' if the video doesn't start automatically.")
            else:
                display_response("No video found for your query.")
        except Exception as e:
            display_response(f"Error: {str(e)}")
    else:
        display_response("Please specify a song to play.")
def get_weather(query):
    city_name = query.lower().replace('weather in', '').strip()
    if city_name:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('cod') == 404:
                display_response("City not found. Please enter a valid city name.")
            else:
                weather_climate = data['weather'][0]['main']
                weather_description = data['weather'][0]['description']
                temperature = round(data['main']['temp'])
                pressure = data['main']['pressure']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                visibility = data.get('visibility', 'Not available')  # Some APIs might not provide visibility
                
                weather_info = (
                    f"The weather in {city_name.capitalize()} is currently {weather_climate} ({weather_description}).\n"
                    f"Temperature: {temperature}°C\n"
                    f"Pressure: {pressure} hPa\n"
                    f"Humidity: {humidity}%\n"
                    f"Wind Speed: {wind_speed} m/s\n"
                    f"Visibility: {visibility} meters"
                )
                display_response(weather_info)
        else:
            display_response("Sorry, I couldn't fetch the weather information.")
    else:
        display_response("Please specify a city to get the weather information.")


def display_response(response):
    # Enable the text widget for updating
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)

    # Define text formatting tags
    result_text.tag_configure('bold', font=('Arial', 12, 'bold'))
    result_text.tag_configure('regular', font=('Arial', 12))
    
    # Replace markdown-like syntax with `**` for easier processing
    response = response.replace('###', '**')
    response = response.replace('##', '**')

    # Split response by '**' to find bold segments
    parts = response.split('**')
    for i, part in enumerate(parts):
        if i % 2 == 1:  # Odd segments are bold
            result_text.insert(tk.END, part, 'bold')
        else:  # Even segments are regular
            result_text.insert(tk.END, part, 'regular')
    
    # Disable the text widget after updating
    result_text.config(state=tk.DISABLED)

    # Split the response into paragraphs
    paragraphs = response.split('\n\n')
    
    # Determine if the assistant should speak or not
    if len(paragraphs) > 0:
        # Get the first paragraph and count words
        first_paragraph = paragraphs[0]
        word_count = len(first_paragraph.split())
        
        if word_count <= 100:
            engine.say(first_paragraph)  # Make the assistant speak the first paragraph
        else:
            engine.say("Your result is here")  # Inform the user that the result is available
    else:
        engine.say("Your result is here")  # Handle cases with no paragraphs

    # Execute the speech
    engine.runAndWait()
    
    


def copy_text():
    try:
        # Copy text to clipboard
        root.clipboard_clear()  # Clear the clipboard
        root.clipboard_append(result_text.get(1.0, tk.END))  # Append the text
        root.update()  # Update the clipboard
        messagebox.showinfo("Info", "Text copied to clipboard!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy text: {str(e)}")

# GUI Setup
root = tk.Tk()
root.title("JAVI Voice Assistant")
root.config(bg="cyan2")

logo = r"C:\python programes\CodeGPT\javi.ico"
try:
    root.iconbitmap(logo)
except tk.TclError as e:
    print(f"Error setting icon: {e}")

# Function to adjust GUI to full screen
def adjust_gui():
    width = root.winfo_screenwidth() - 10
    height = root.winfo_screenheight() - 10
    root.geometry(f"{width}x{height}")
    root.attributes('-fullscreen', False)


# Entry for user input
tk.Label(root, text="JAVI",  bg="cyan2" , fg="red",font=('Castellar', 40,'bold')).pack(pady=10, padx=10, side=tk.TOP)

entry = tk.Entry(root, font=('Aptos Display', 20), fg="purple1",bg='Lightcyan2', bd=4, relief='sunken', width=80)
entry.place(x=180, y=120)

# Bind Enter key to the entry widget
def on_enter_key(event):
    process_query()

entry.bind('<Return>', on_enter_key)

# Button to trigger speech recognition
mic_button = tk.Button(root, text="🎙️", activeforeground="red", activebackground='cyan2' ,fg="Dark Green", bg='cyan2',command=recognize_speech, relief="flat", font=('Arial', 19))
mic_button.place(x=1950, y=100)  # Adjust x and y as needed

# Text widget to display results
result_text = tk.Text(root, wrap=tk.WORD, bd=4,bg='whitesmoke',fg='orangered', height=40, width=120, font=('Aptos', 17), state=tk.DISABLED)
result_text.place(x=180, y=250, width=1750, height=900)  # Adjust x, y, width, and height as needed

# Scrollbar for the result text widget
scrollbar = tk.Scrollbar(root, command=result_text.yview)
scrollbar.place(x=1910, y=250, height=900)  # Adjust x and y as needed
result_text['yscrollcommand'] = scrollbar.set

# Create Copy button
copy_button = tk.Button(root, text="Copy",  activeforeground="white",activebackground="green", fg='black',bg='white', font=('Verdana', 10), relief='sunken', command=copy_text)
copy_button.place(x=1836, y=209)  # Adjust x and y as needed

# Set the GUI to full screen
root.after(100, adjust_gui)

# Start the GUI event loop
root.mainloop()
