import tkinter as tk
from tkinter import messagebox
import bcrypt

# Track login status
logged_in_user = None

# Track failed login attempts
failed_attempts = {}
locked_users = set()


# -------------------- REGISTER --------------------
def register():
    username = username_entry.get().strip()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showwarning(
            "Warning",
            "Please enter username and password."
        )
        return

    # Password requirements
    if len(password) < 8:
        messagebox.showerror(
            "Registration Failed",
            "Password must contain at least 8 characters."
        )
        return

    if not any(char.isupper() for char in password):
        messagebox.showerror(
            "Registration Failed",
            "Password must contain at least one uppercase letter."
        )
        return

    if not any(char.islower() for char in password):
        messagebox.showerror(
            "Registration Failed",
            "Password must contain at least one lowercase letter."
        )
        return

    if not any(char.isdigit() for char in password):
        messagebox.showerror(
            "Registration Failed",
            "Password must contain at least one number."
        )
        return

    if not any(not char.isalnum() for char in password):
        messagebox.showerror(
            "Registration Failed",
            "Password must contain at least one special character."
        )
        return

    # Check duplicate username
    try:
        with open("users.txt", "r") as file:
            users = file.readlines()

        for user in users:
            stored_username, stored_hash = user.strip().split("|", 1)

            if stored_username == username:
                messagebox.showerror(
                    "Registration Failed",
                    "Username already exists."
                )
                return

    except FileNotFoundError:
        pass

    # Hash password using bcrypt
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    # Store username and hash
    with open("users.txt", "a") as file:
        file.write(
            username + "|" + hashed_password.decode("utf-8") + "\n"
        )

    messagebox.showinfo(
        "Registration Successful",
        "Account created successfully!"
    )

    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


# -------------------- LOGIN --------------------
def login():
    global logged_in_user

    username = username_entry.get().strip()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showwarning(
            "Warning",
            "Please enter username and password."
        )
        return

    # Check if account is locked
    if username in locked_users:
        messagebox.showerror(
            "Account Locked",
            "This account has been locked after 3 failed login attempts."
        )
        return

    try:
        with open("users.txt", "r") as file:
            users = file.readlines()

        for user in users:
            stored_username, stored_hash = user.strip().split("|", 1)

            if stored_username == username:

                if bcrypt.checkpw(
                    password.encode("utf-8"),
                    stored_hash.encode("utf-8")
                ):
                    # Successful login
                    logged_in_user = username
                    failed_attempts[username] = 0

                    status_label.config(
                        text=f"● Logged in as {username}"
                    )

                    messagebox.showinfo(
                        "Login Successful",
                        "Authentication successful!"
                    )
                    return

                else:
                    # Increase failed attempts
                    failed_attempts[username] = (
                        failed_attempts.get(username, 0) + 1
                    )

                    attempts = failed_attempts[username]

                    if attempts >= 3:
                        locked_users.add(username)

                        messagebox.showerror(
                            "Account Locked",
                            "3 failed login attempts detected.\n"
                            "This account is now locked."
                        )
                    else:
                        remaining = 3 - attempts

                        messagebox.showerror(
                            "Login Failed",
                            f"Invalid password.\n"
                            f"Attempts remaining: {remaining}"
                        )

                    return

        messagebox.showerror(
            "Login Failed",
            "Username not found."
        )

    except FileNotFoundError:
        messagebox.showerror(
            "Error",
            "No registered users found.\nPlease register first."
        )


# -------------------- LOGOUT --------------------
def logout():
    global logged_in_user

    if logged_in_user is None:
        messagebox.showwarning(
            "Logout",
            "No user is currently logged in."
        )
        return

    logged_in_user = None

    status_label.config(
        text="● Logged out"
    )

    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    messagebox.showinfo(
        "Logout",
        "You have been logged out successfully."
    )


# -------------------- MAIN WINDOW --------------------
root = tk.Tk()
root.title("Secure Login System")
root.geometry("500x520")
root.resizable(False, False)

# Main background
root.configure(bg="#f4f6f8")

# -------------------- HEADER --------------------
header = tk.Frame(
    root,
    bg="#1f2937",
    height=110
)
header.pack(fill="x")

title_label = tk.Label(
    header,
    text="🔐 Secure Login System",
    font=("Arial", 22, "bold"),
    bg="#1f2937",
    fg="white"
)
title_label.pack(pady=(20, 5))

subtitle_label = tk.Label(
    header,
    text="Secure Authentication using bcrypt",
    font=("Arial", 10),
    bg="#1f2937",
    fg="white"
)
subtitle_label.pack()


# -------------------- LOGIN CARD --------------------
card = tk.Frame(
    root,
    bg="white",
    padx=35,
    pady=25
)
card.pack(padx=35, pady=30, fill="both", expand=True)

# Username
username_label = tk.Label(
    card,
    text="Username",
    font=("Arial", 11, "bold"),
    bg="white"
)
username_label.pack(anchor="w")

username_entry = tk.Entry(
    card,
    width=35,
    font=("Arial", 11)
)
username_entry.pack(pady=(5, 15), ipady=6)

# Password
password_label = tk.Label(
    card,
    text="Password",
    font=("Arial", 11, "bold"),
    bg="white"
)
password_label.pack(anchor="w")

password_entry = tk.Entry(
    card,
    width=35,
    font=("Arial", 11),
    show="*"
)
password_entry.pack(pady=(5, 20), ipady=6)


# -------------------- BUTTONS --------------------
register_button = tk.Button(
    card,
    text="Register",
    width=18,
    font=("Arial", 10, "bold"),
    command=register
)
register_button.pack(pady=5)

login_button = tk.Button(
    card,
    text="Login",
    width=18,
    font=("Arial", 10, "bold"),
    command=login
)
login_button.pack(pady=5)

logout_button = tk.Button(
    card,
    text="Logout",
    width=18,
    font=("Arial", 10, "bold"),
    command=logout
)
logout_button.pack(pady=5)


# -------------------- STATUS --------------------
status_label = tk.Label(
    card,
    text="● Not logged in",
    font=("Arial", 10, "bold"),
    bg="white"
)
status_label.pack(pady=(15, 5))


# Security information
security_label = tk.Label(
    card,
    text="🔒 Passwords are securely stored using bcrypt hashing",
    font=("Arial", 9),
    bg="white"
)
security_label.pack(pady=5)


# -------------------- RUN --------------------
root.mainloop()