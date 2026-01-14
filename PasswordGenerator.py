from tkinter import *
from tkinter.ttk import *
from ttkthemes import ThemedTk
import random
import time


root = ThemedTk(theme="ubuntu")
root.title("PasswordGenerator_Billy_MPA")
root.geometry("510x260")
root.resizable(False, False)

lower = "abcdefghijklmnopqrstuvwxyz"
upper = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
strong = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"

password_var = StringVar()
encrypted_var = StringVar()
key_var = IntVar(value=0)
power = IntVar(value=2)
save_var = IntVar(value=0)


def save_to_txt():
    if encrypted_var.get() == "" or key_var.get() == 0:
        return
    with open("encrypted_data.txt", "a", encoding="utf-8") as f:
        f.write(encrypted_var.get() + "\n")
        f.write("KEY: " + str(key_var.get()) + "\n")
        f.write("-" * 30 + "\n")

def get_time_key():
    now = time.localtime()
    return (now.tm_hour * 3600 + now.tm_min * 60 + now.tm_sec) * 23

def gen():
    length = int(combo.get())
    pool = lower if power.get() == 1 else upper if power.get() == 2 else strong

    password = "".join(random.choice(pool) for _ in range(length))
    password_var.set(password)
    encrypted_var.set("")
    key_var.set(0)

def encrypt():
    text = password_var.get()
    key = get_time_key()
    encrypted = ""

    for c in text:
        if c in strong:
            encrypted += strong[(strong.index(c) + key) % len(strong)]
        else:
            encrypted += c

    encrypted_var.set(encrypted)
    key_var.set(key)
    if save_var.get():
        save_to_txt()

def decrypt():
    text = encrypted_var.get()
    key = key_var.get()
    if key == 0:
        return

    decrypted = ""
    for c in text:
        if c in strong:
            decrypted += strong[(strong.index(c) - key) % len(strong)]
        else:
            decrypted += c

    password_var.set(decrypted)

def copy_var(v):
    root.clipboard_clear()
    root.clipboard_append(v.get())


Label(root, text="Password").grid(row=0, column=0, padx=5, pady=5)
Entry(root, textvariable=password_var, width=25).grid(row=0, column=1)
Button(root, text="Copy", command=lambda: copy_var(password_var)).grid(row=0, column=2)

Label(root, text="Encrypted").grid(row=1, column=0)
Entry(root, textvariable=encrypted_var, width=25).grid(row=1, column=1)
Button(root, text="Copy", command=lambda: copy_var(encrypted_var)).grid(row=1, column=2)

Label(root, text="Length").grid(row=2, column=0)
combo = Combobox(root, values=(10, 12, 14, 16, 18, 20), width=22)
combo.current(1)
combo.grid(row=2, column=1)

Label(root, text="Power").grid(row=3, column=0)

power_frame = Frame(root)
power_frame.grid(row=3, column=1, sticky=W)

Radiobutton(power_frame, text="Low", value=1, variable=power).pack(side=LEFT, padx=5)
Radiobutton(power_frame, text="Medium", value=2, variable=power).pack(side=LEFT, padx=5)
Radiobutton(power_frame, text="Strong", value=3, variable=power).pack(side=LEFT, padx=5)

Button(root, text="Generate", command=gen).grid(row=4, column=0, pady=8)
Button(root, text="Encrypt", command=encrypt).grid(row=4, column=1)
Button(root, text="Decrypt", command=decrypt).grid(row=4, column=2)

Label(root, text="Key").grid(row=5, column=0)
Entry(root, textvariable=key_var, width=25).grid(row=5, column=1)
Button(root, text="Copy", command=lambda: copy_var(key_var)).grid(row=5, column=2)

Checkbutton(root, text="Save to file", variable=save_var).grid(row=6, column=1)

root.mainloop()
