from customtkinter import*
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("800x600")
        self.title("Voting System")
        self.config(bg='white')
        self.attributes('-fullscreen', True)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True, fill=tk.BOTH)

        self.home_tab = ctk.CTkFrame(self.notebook)
        self.admin_tab = ctk.CTkFrame(self.notebook)

        self.notebook.add(self.home_tab, text="HOME")
        self.notebook.add(self.admin_tab, text="ADMIN")

        self.category = 1
        self.categories = ["~SRC PRESIDENT~","~JCR PRESIDENT~","~ACSES PRESIDENT~"]

        # Updated candidates with corresponding images and bios
        self.candidates = {
            1: [("Mr.ARTHUR AIKINS", "\n20yrs\nLv.300\nBSc.BSc.MINING ENG.", "aikins.jpg"),
                ("Mr.ASHONG SPENCER", "\n15yrs\nLv.100\nBSc.COMPUTER SCIENCE", "spencer.jpg"),
                ("Mr.BAAH BERNARD", "\n23yrs\nLv.400\nBSc.MECHANICAL ENG.", "bernard.jpg")],
            2: [("Ms.DARDEY PRISCILA", "\n20yrs\nLv.300\nBSc.DATA ANALYTICS", "priscy.jpg"),
                ("Mr.DANQUA EMANUEL", "\n18yrs\nLv.200\nBSc.PETROLEUM ENG.", "emma.jpg"),
                ("Ms.SIEBER ALICE", "\n19yrs\nLv.100\nBSc.MATHEMATICS", "alice.jpg")],
            3: [("Mr.ONANA ANDRE", "\n25yrs\nLv.-300\nBSc.COMPUTER SCIENCE", "maguire.jpg"),
                ("Mr.MAGUIRE HARRY", "\n22yrs\nLv.100\nBSc.COMPUTER SCIENCE", "antony.jpg"),
                ("Mr.ASARE ANTONY", "\n19yrs\nLv.-200\nBSc.COMPUTER SCIENCE", "onana.jpg")]
        }
        self.votes = {candidate[0]: 0 for category in self.candidates.values() for candidate in category}

        self.create_home_login_tab()
        self.create_admin_tab()

    def create_home_login_tab(self):
        self.home_login_frame = ctk.CTkFrame(self.home_tab, fg_color='white')
        self.home_login_frame.pack(pady=10, expand=True, fill=tk.BOTH)
        
        # Welcome label
        CTkLabel(self.home_login_frame, text="WELCOME TO THE UNIVERSITY OF MINES AND TECHNOLOGY(UMaT) ELECTIONS, 2024",
        font=('Courier New', 39,'bold'),
        text_color='darkgreen',
        wraplength=1300,
        anchor='w',
        justify='center').pack(padx=50, pady=(30, 10))

        # UMaT logo
        logo = CTkImage(light_image=Image.open("images/umatlogo.jpg"), size=(327, 275))
        CTkLabel(self.home_login_frame, image=logo).pack(pady=20)

        # Username Entry
        self.username = CTkEntry(self.home_login_frame,placeholder_text='USERNAME',font=('Courier New', 30, 'bold'),corner_radius=10,width=300,height=50)
        self.username.pack(pady=10)

        # Password Entry
        self.password = CTkEntry(self.home_login_frame, placeholder_text='PASSWORD',show="•",font=('Courier New', 30, 'bold'),corner_radius=10,width=300,height=50)
        self.password.pack(pady=10)

        # Login Button
        login_button = CTkButton(self.home_login_frame, text="LOGIN", command=self.home_login,fg_color="darkgreen",hover_color='green',text_color="white",font=('Courier New', 30, 'bold'),corner_radius=9,width=300)
        login_button.pack(pady=13)

    def home_login(self):
        if self.username.get() == "user" and self.password.get() == "password":
            self.home_login_frame.destroy()
            self.create_home_tab()
        else:
            messagebox.showerror("LOGIN FAILED!!!", "Incorrect username or password")

    def create_admin_tab(self):
        self.admin_login_frame = CTkFrame(self.admin_tab, fg_color='white')
        self.admin_login_frame.pack(pady=10, expand=True, fill=tk.BOTH)

        # Welcome label
        CTkLabel(self.admin_login_frame, text="ADMIN'S PORTAL",
        font=('Courier New', 50,'bold'),
        text_color='darkgreen',
        wraplength=1300,
        anchor='w',
        justify='center').pack(padx=50, pady=(30, 10))

        # Password Entry
        password_label = ctk.CTkLabel(self.admin_login_frame, text="PASSWORD:", font=('Courier New', 30, 'bold'))
        password_label.place(relx=0.44,rely=0.4)
        self.adminpass = CTkEntry(self.admin_login_frame, placeholder_text='PASSWORD',show="•",font=('Courier New', 30, 'bold'),corner_radius=10,width=300,height=50)
        self.adminpass.place(relx=0.39,rely=0.45)

        # Login Button
        login_button = CTkButton(self.admin_login_frame, text="LOGIN", command=self.admin_login,fg_color="darkgreen",hover_color='green',text_color="white",font=('Courier New', 30, 'bold'),corner_radius=9,width=300)
        login_button.place(relx=0.39,rely=0.55)

    def admin_login(self):
        if self.adminpass.get() == "admin":
            self.admin_login_frame.destroy()
            self.admin_dashboard()
        else:
            messagebox.showerror("ACCESS DENIED!!!", "Incorrect password")

    def create_home_tab(self):
        self.home_tab_frame = ctk.CTkFrame(self.home_tab, fg_color='white')
        self.home_tab_frame.pack(pady=10, expand=True, fill=tk.BOTH)

        self.update_category_display()

    def update_category_display(self):
        for widget in self.home_tab_frame.winfo_children():
            widget.destroy()

        self.radio_button_var = tk.IntVar() 
        self.votes_cast = False

        category_name = self.categories[self.category - 1]
        lab1 = ctk.CTkLabel(self.home_tab_frame, text=category_name,font=('Courier New', 60,'bold'),text_color='darkgreen')
        lab1.pack(pady=20)

        self.candidate_frames = []

        for i, (candidate_name, bio_text, image_file) in enumerate(self.candidates[self.category]):

            frame = ctk.CTkFrame(self.home_tab_frame, width=350, height=350, fg_color='white')
            frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
            self.candidate_frames.append(frame)

            image_path = f"images/{image_file}"
            photo = CTkImage(light_image=Image.open(image_path), size=(360, 335))
            CTkLabel(frame, image=photo).place(relx=0.5, rely=0.26, anchor='center')

            # Radio buttons
            rb = ctk.CTkRadioButton(frame, text="", variable=self.radio_button_var,value=i+1,fg_color='darkgreen',border_width_checked=11,radiobutton_width=40,radiobutton_height=40)
            rb.place(relx=0.5,rely=0.81)

            # Bio Textbox
            bio_textbox = ctk.CTkTextbox(frame, width=300, height=150,font=('Courier New', 20, 'bold'),fg_color='white',text_color='grey')
            bio_textbox.insert('1.0', bio_text)
            bio_textbox.configure(state='disabled')
            bio_textbox.place(relx=0.25,rely=0.51)

            candidate_label = ctk.CTkLabel(frame, text=candidate_name, font=('Courier New', 30,'bold'),text_color='darkgreen')
            candidate_label.place(relx=0.21,rely=0.73)

        cast_vote_button = ctk.CTkButton(self.home_tab_frame, text="VOTE", command=self.cast_vote, font=('Courier New', 30,'bold'), corner_radius=9, width=300, hover_color='green',fg_color='darkgreen')
        cast_vote_button.place(relx=0.4,rely=0.93)

    def cast_vote(self):
        if not self.votes_cast:
            vote = self.radio_button_var.get()
            if vote > 0:
                candidate = self.candidates[self.category][vote-1][0]
                self.votes[candidate] += 1
                self.votes_cast = True

                if self.category == 3:
                    self.thank_you_message()
                else:
                    self.next_category()
            else:
                messagebox.showwarning("No Selection", "Please select a candidate before casting your vote.")

    def next_category(self):
        if self.category < 3:
            self.category += 1
            self.update_category_display()

    def thank_you_message(self):
        messagebox.showinfo("SUCCESSFUL!", "Your votes have been submitted succesfully.\nThank you!")

    def admin_dashboard(self):
        self.admin_dashboard_frame = ctk.CTkFrame(self.admin_tab, fg_color='white')
        self.admin_dashboard_frame.pack(pady=10, expand=True, fill=tk.BOTH)

        self.create_table()
        self.create_barchart()

        logout_button = ctk.CTkButton(self.admin_dashboard_frame, text="Log Out", command=self.logout, fg_color="darkgreen", hover_color='green', text_color="white", font=('Courier New', 20,'bold'),width=150)
        logout_button.place(relx=0.88,rely=0.95)

    def create_table(self):
        conn = sqlite3.connect("votes44.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS votes (candidate TEXT, votes INTEGER)")
        c.execute("DELETE FROM votes")
        for candidate, vote in self.votes.items():
            c.execute("INSERT INTO votes VALUES (?, ?)", (candidate, vote))
        conn.commit()
        conn.close()

        table_frame = ctk.CTkFrame(self.admin_dashboard_frame, fg_color='white')
        table_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        table = ttk.Treeview(table_frame, columns=("Candidate", "Votes"), show="headings")
        table.pack(pady=10, fill=tk.BOTH, expand=True)

        table.heading("Candidate", text="CANDIDATES")
        table.heading("Votes", text="VOTES")

        for candidate, vote in self.votes.items():
            table.insert("", "end", values=(candidate, vote))

    def create_barchart(self):
        fig, ax = plt.subplots(figsize=(17.2, 4))  # Increased width to 14 and height to 8
        
        ax.bar(self.votes.keys(), self.votes.values(), color='darkgreen', width=0.02)
        ax.set_xlabel('CANDIDATES')
        ax.set_ylabel('NUMBER OF VOTES')
        ax.set_title('VOTES FOR EACH CANDIDATE')


        canvas = FigureCanvasTkAgg(fig, master=self.admin_dashboard_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(relx=0.492, rely=0.66, anchor='center')


    def logout(self):
        self.admin_dashboard_frame.destroy()
        self.create_admin_tab()

if __name__ == "__main__":
    app = App()
    app.mainloop()
