import tkinter as tk
from tkinter import messagebox, font, ttk
import re
import hashlib
import requests

def check_pwned_password(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1password[:5]
    suffix = sha1password[5:]
    url = 'https://api.pwnedpasswords.com/range/' + prefix
    response = requests.get(url)
    
    if response.status_code != 200:
        raise RuntimeError('Error fetching "Have I Been Pwned" data: {}'.format(response.status_code))
    
    suffixes = (line.split(':') for line in response.text.splitlines())
    for hash_suffix, count in suffixes:
        if hash_suffix == suffix:
            return True, count
    return False, 0

# Function to calculate the password strength
def check_password_strength(password):
    score = 0
    length = len(password)

    # Increase score based on length
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1

    # Check for presence of numbers, uppercase, lowercase, and special characters
    if re.search(r"\d", password): # Numbers
        score += 1
    if re.search(r"[A-Z]", password): # Uppercase
        score += 1
    if re.search(r"[a-z]", password): # Lowercase
        score += 1
    if re.search(r"[!@#$%^&*()-_=+[]\{}|;:',.<>?/~`]", password): # Special characters
        score += 1
    
    # Additional complexity checks
    if re.search(r"(.)\1{2,}", password): # Deduct points for triple repeat characters
        score -= 1
    if re.search(r"(0123|1234|2345|3456|4567|5678|6789|7890)", password): # Sequential numbers
        score -= 1
    if re.search(r"(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mnop|nopq|opqr|pqrs|qrst|rstu|stuv|tuvw|uvwx|vwxy|wxyz)", password.lower()): # Sequential letters
        score -= 1

    if check_pwned_password(password):
        score = 0
    else:
        print('This password has not appeared in a known breach.')

    # Ensure score is between 0 and 5
    score = max(score, 0)
    score = min(score, 5)

    return score

# Function to provide a rating and display a message box
def rate_password():
    password = password_entry.get()
    score = check_password_strength(password)
    compromised, count = check_pwned_password(password)

    reasons = []
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

    if reasons:
        reasons_str = "\n".join(reasons)
        messagebox.showwarning("Password Strength Rating",
                               f"Your password is: {rating}.\n\nIssues:\n{reasons_str}")
    else:
        messagebox.showinfo("Password Strength Rating", f"Your password is: {rating}.")

# Create the main window
root = tk.Tk()
root.title("Password Strength Checker")

# Set a theme for ttk
style = ttk.Style()
style.theme_use('default')  # Using the default theme as a base

# Define colors for the dark theme
dark_background = "#2D2D2D"
light_text = "#E0E0E0"
accent_color = "#009688"  # Teal color for the accent
input_bg = "#4E4E4E"
button_bg = "#4E4E4E"
button_fg = "#E0E0E0"
button_active_bg = "#00796B"

# Customize the style for the label, entry and button
style.configure('TLabel', background=dark_background, foreground=light_text, font=('Arial', 11))
style.configure('TEntry', fieldbackground=input_bg, foreground=light_text, borderwidth=1, font=('Arial', 11))
style.configure('TButton', background=button_bg, foreground=button_fg, font=('Arial', 11), borderwidth=1)
style.map('TButton',
          background=[('active', button_active_bg)],
          foreground=[('active', light_text)])

# Change the default background color of the root window and all frames
root.configure(background=dark_background)
style.configure('TFrame', background=dark_background)

# Set the window size and center it
window_width = 500
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Create a main frame for padding
main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.pack(expand=True, fill=tk.BOTH)

# Create a frame for the input section
input_frame = ttk.Frame(main_frame, padding="10 10 10 10")
input_frame.pack(pady=20, expand=True, fill=tk.BOTH)

# Create the label and entry for the password
password_label = ttk.Label(input_frame, text="Enter your password:")
password_label.pack(side=tk.LEFT, padx=10)
password_entry = ttk.Entry(input_frame, show="*", width=30)
password_entry.pack(side=tk.RIGHT, padx=10)

# Create a frame for the button
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=10, expand=True)

# Function to change the cursor to a pointer
def on_enter(event):
    check_button.configure(cursor="hand2")

# Function to change the cursor back to arrow
def on_leave(event):
    check_button.configure(cursor="")

# Create the check button
check_button = tk.Button(button_frame, text="Check Strength", command=rate_password, font=('Arial', 11))
check_button.pack(side=tk.LEFT, padx=10)

# Bind the enter and leave events to the check button
check_button.bind("<Enter>", on_enter)
check_button.bind("<Leave>", on_leave)

# Start the main loop
root.mainloop()
