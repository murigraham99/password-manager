from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_numbers + password_symbols

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    website.lower()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Empty field", message="You have left an empty field")
    else:
        ok = messagebox.askokcancel(title=website,
                                    message=f"The data you have entered for {website} is:\n email: {email} \n password: {password} \n Is this correct?")

        if ok:
            try:
                with open("file.json", "r") as file:
                    # reading old data:
                    data = json.load(file)
            except FileNotFoundError:
                with open("file.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                # updating old data with new data
                data.update(new_data)
                with open("file.json", "w") as file:

                    # saving updated data
                    json.dump(data, file, indent=4)

            finally:
                website_entry.delete(0, "end")
                password_entry.delete(0, "end")


# ---------------------------- SEARCH PASSWORD IN JSON FILE ------------------------------- #


def search():
    website = website_entry.get()
    website.lower()
    try:
        with open("file.json", "r") as file:
            data = json.load(file)


    except FileNotFoundError:
        messagebox.showerror(title="Error", message="Data not found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            print(f"pressed {password} \n {email}")

            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showerror(title="Not found", message="There are no details found for the website")


# ---------------------------- UI SETUP -------------------------------

screen = Tk()
screen.title("Password Manager")
screen.config(pady=50, padx=50)
canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="MURI.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# text fields:
website_txt = Label(text="Website:")
website_txt.grid(column=0, row=1)

email_txt = Label(text="Email/User:")
email_txt.grid(column=0, row=2)

password_txt = Label(text="Password:")
password_txt.grid(column=0, row=3)

# entry fields:
website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(column=1, row=1)

email_entry = Entry(width=38)
email_entry.insert(0, "robertomuresan1999@gmail.com")
email_entry.grid(column=1, row=2, columnspan=2)

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# buttons:
password_button = Button(text="Generate Password", command=gen_password)
password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", command=search, width=13)
search_button.grid(column=2, row=1)

screen.mainloop()
