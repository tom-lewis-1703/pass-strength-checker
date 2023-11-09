import tkinter as tk
from tkinter import messagebox, font, ttk
import re
import hashlib
import requests

# Function to check if a password has been compromised using the HIBP API
def check_pwned_password(password):
    # Hash the password using SHA-1
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    # Take only the first 5 characters of the hash
    prefix = sha1password[:5]
    # The rest of the hash
    suffix = sha1password[5:]
    # Form the URL to only send the first 5 characters of the hash
    url = 'https://api.pwnedpasswords.com/range/' + prefix
    # Make the request to the HIBP API
    response = requests.get(url)
    
    # Raise an error if the response from HIBP API is not successful
    if response.status_code != 200:
        raise RuntimeError('Error fetching "Have I Been Pwned" data: {}'.format(response.status_code))
    
    # Check if the suffix of our hash is in the response
    suffixes = (line.split(':') for line in response.text.splitlines())
    for hash_suffix, count in suffixes:
        if hash_suffix == suffix:
            return True, count
    return False, 0

# Function to calculate the password strength
def check_password_strength(password):
    score = 0
    length = len(password)

    # Increase score based on password length
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1

    # Increase score based on presence of different types of characters
    if re.search(r"\d", password): # Numbers
        score += 1
    if re.search(r"[A-Z]", password): # Uppercase letters
        score += 1
    if re.search(r"[a-z]", password): # Lowercase letters
        score += 1
    if re.search(r"[!@#$%^&*()-_=+[\]{}|;:',.<>?/~`]", password): # Special characters
        score += 1
    
    # Deduct points for patterns that reduce password strength
    if re.search(r"(.)\1{2,}", password): # Triple repeat characters
        score -= 1
    if re.search(r"(0123|1234|2345|3456|4567|5678|6789|7890)", password): # Sequential numbers
        score -= 1
    if re.search(r"(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mnop|nopq|opqr|pqrs|qrst|rstu|stuv|tuvw|uvwx|vwxy|wxyz)", password.lower()): # Sequential letters
        score -= 1

    # Check if the password has been compromised and set score to 0 if it has
    if check_pwned_password(password):
        score = 0

    # Ensure the score is within the range 0-5
    score = max(score, 0)
    score = min(score, 5)

    return score

# Function to provide a rating and display a message box
def rate_password():
    # Get the password from the entry widget
    password = password_entry.get()
    # Calculate the password strength
    score = check_password_strength(password)
    # Check if the password is compromised
    compromised, count = check_pwned_password(password)

    # List to hold reasons why the password might be weak
    reasons = []
    # Add reasons based on the missing criteria for a strong password
    if len(password) < 8:
        reasons.append("Password is too short (less than 8 characters).")
    if not any(char.isdigit() for char in password):
        reasons.append("Password does not contain any numbers.")
    if not any(char.isupper() for char in password):
        reasons.append("Password does not contain any uppercase letters.")
    if not any(char.islower() for char in password):
        reasons.append("Password does not contain any lowercase letters.")
    if not any(char in '!@#$%^&*()-_=+[]{}|;:,.<>?/~' for char in password):
        reasons.append("Password does not contain any special characters.")
    if compromised:
        reasons.append(f"This password has been compromised and seen {count} times in data breaches.")
    
    # Determine the rating based on the score
    rating = ""
    if score <= 1:
        rating = "Very Weak"
    elif score == 2:
        rating = "Weak"
    elif score == 3:
        rating = "Medium"
    elif score == 4:
        rating = "Strong"
    elif score == 5:
        rating = "Very Strong"

    # Display the appropriate message box with the rating and reasons
    if reasons:
        reasons_str = "\n".join(reasons)
        messagebox.showwarning("Password Strength Rating",
                               f"Your password is: {rating}.\n\nIssues:\n{reasons_str}")
    else:
        messagebox.showinfo("Password Strength Rating", f"Your password is: {rating}.")

# Set up the main window and its appearance
root = tk.Tk()
root.title("Password Strength Checker")

# Configure the style for the ttk widgets
style = ttk.Style()
style.theme_use('default')  # Base the custom style on the default theme

# Define and apply custom colors and font styles for the dark theme
dark_background = "#2D2D2D"
light_text = "#E0E0E0"
accent_color = "#009688"  # Teal as an accent color
input_bg = "#4E4E4E"
button_bg = "#4E4E4E"
button_fg = "#E0E0E0"
button_active_bg = "#00796B"

# Configure ttk widgets to use the custom styles defined above
style.configure('TLabel', background=dark_background, foreground=light_text, font=('Arial', 11))
style.configure('TEntry', fieldbackground=input_bg, foreground=light_text, borderwidth=1, font=('Arial', 11))
style.configure('TButton', background=button_bg, foreground=button_fg, font=('Arial', 11), borderwidth=1)
style.map('TButton',
          background=[('active', button_active_bg)],
          foreground=[('active', light_text)])

# Set the background color of the main window and all frames to match the dark theme
root.configure(background=dark_background)
style.configure('TFrame', background=dark_background)

# Position the window in the center of the screen with a predefined size
window_width = 500
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Create and configure the main frame for the layout
main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.pack(expand=True, fill=tk.BOTH)

# Create and configure the frame for the input section
input_frame = ttk.Frame(main_frame, padding="10 10 10 10")
input_frame.pack(pady=20, expand=True, fill=tk.BOTH)

# Create and configure the label and entry for the password input
password_label = ttk.Label(input_frame, text="Enter your password:")
password_label.pack(side=tk.LEFT, padx=10)
password_entry = ttk.Entry(input_frame, show="*", width=30)
password_entry.pack(side=tk.RIGHT, padx=10)

# Create and configure the frame for the button
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=10, expand=True)

# Event handlers to change the cursor on button hover
def on_enter(event):
    check_button.configure(cursor="hand2")  # Change to pointer cursor when mouse enters

def on_leave(event):
    check_button.configure(cursor="")  # Change back to default cursor when mouse leaves

# Create and configure the button to check password strength
check_button = tk.Button(button_frame, text="Check Strength", command=rate_password, font=('Arial', 11))
check_button.pack(side=tk.LEFT, padx=10)

# Bind hover events to the check button for cursor style change
check_button.bind("<Enter>", on_enter)
check_button.bind("<Leave>", on_leave)

# Start the main loop of the GUI
root.mainloop()
