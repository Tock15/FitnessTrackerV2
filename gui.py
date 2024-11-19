import customtkinter as ctk
from tkcalendar import DateEntry
import pickle
from exercise import Weightlifting, Tracker #,Cardio
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os
import datetime
import matplotlib.dates as mdates


ctk.set_default_color_theme("theme.json")
ctk.set_appearance_mode("light")
class MainPage(ctk.CTk):
    def __init__(self,*args,**kwargs):
        self.tracker=None
        self.data = []
        if not os.path.exists("data.pkl"):
            with open("data.pkl", "wb") as f:
                pickle.dump(self.data, f)
                f.close()
        else:
            with open("data.pkl", "rb") as f:
                self.data = pickle.load(f)
                f.close()
        super().__init__(*args,**kwargs)
        self.geometry("1000x600")
        self.title("Exercise Tracker")
        self.from_date = None
        self.to_date= None
        

        ############### Main Frame ################

        self.mainFrame = ctk.CTkFrame(self)
        self.mainFrame.pack(fill="both", expand=True)
        self.mainFrame.grid_columnconfigure(0, weight=1)
        # Title
        self.title_label = ctk.CTkLabel(self.mainFrame, text="Fitness Tracker", font=("Arial", 36))
        self.title_label.grid(row=0, column=0, pady=100)
        # BMI Button
        self.bmi_button = ctk.CTkButton(self.mainFrame, text="BMI Calculator",command=self.show_bmi)
        self.bmi_button.grid(row=1, column=0, pady=10)
        # Tracker Button
        self.tracker_button = ctk.CTkButton(self.mainFrame, text="Tracker",command=self.show_tracker)
        self.tracker_button.grid(row=2, column=0, pady=10)
        # Stats Button
        self.stats_button = ctk.CTkButton(self.mainFrame, text="Stats",command=self.show_stats)
        self.stats_button.grid(row=3, column=0, pady=10)

        self.toplevel_window = None ## use this later for top level window

        ############### Tracker Frame ################

        self.trackerFrame = ctk.CTkFrame(self)
        self.trackerFrame.grid_columnconfigure(0, weight=1)
        self.trackerFrame.grid_rowconfigure(2, weight=1) 
        self.trackerFrame.pack_forget() 
        # Title for Tracker Frame
        self.tracker_title_label = ctk.CTkLabel(self.trackerFrame, text="Workout Log", font=("Arial", 36))
        self.tracker_title_label.grid(row=0, column=0, pady=20)
        # Back Button
        self.back_button = ctk.CTkButton(self.trackerFrame, text="Back", command=self.show_main)
        self.back_button.grid(row=1, column=0, sticky="w", padx=20, pady=10)
        # Log New Workout Button
        self.log_new_workout_button = ctk.CTkButton(self.trackerFrame, text="Log New Workout", command=self.open_new_workout)
        self.log_new_workout_button.grid(row=1, column=0, sticky="e", padx=20, pady=10)
        # Exercise Log Table
        self.log_table_frame = ctk.CTkScrollableFrame(self.trackerFrame, fg_color="lightgrey")
        self.log_table_frame.grid(row=2, column=0, pady=20, padx=20, sticky="nsew")
        # Ensure the log_table_frame expands
        self.log_table_frame.grid_columnconfigure(1, weight=1)  
        self.update_log_table()

        ################## BMI Frame ##################

        self.bmi_frame = ctk.CTkFrame(self)
        self.bmi_frame.grid_columnconfigure(0, weight=1)
        self.bmi_frame.pack_forget()
        # Title for BMI Frame
        self.bmi_title_label = ctk.CTkLabel(self.bmi_frame, text="BMI Calculator", font=("Arial", 36))
        self.bmi_title_label.grid(row=0, column=0,columnspan=2, pady=20)
        # Back Button
        self.bmi_back_button = ctk.CTkButton(self.bmi_frame, text="Back", command=self.show_main)
        self.bmi_back_button.grid(row=1, column=0, sticky="w", padx=150, pady=(20,50))
        # Height Entry
        self.height_label = ctk.CTkLabel(self.bmi_frame, text="Height (cm):")
        self.height_label.grid(row=2, column=0, padx=(200,20), pady=10, sticky="w")
        self.height_entry = ctk.CTkEntry(self.bmi_frame)
        self.height_entry.grid(row=2, column=1, padx=(20,200), pady=10,sticky= "e")
        # Weight Entry
        self.weight_label = ctk.CTkLabel(self.bmi_frame, text="Weight (kg):")
        self.weight_label.grid(row=3, column=0, padx=(200,20), pady=10, sticky="w")
        self.weight_entry = ctk.CTkEntry(self.bmi_frame)
        self.weight_entry.grid(row=3, column=1, padx=(20,200), pady=10,sticky= "e")
        # Calculate Button
        self.calculate_button = ctk.CTkButton(self.bmi_frame, text="Calculate", command=self.calculate_bmi)
        self.calculate_button.grid(row=4, column=0, columnspan=2, pady=20)
        # Result Label
        self.result_label = ctk.CTkLabel(self.bmi_frame, text="", font=("Arial", 24))
        self.result_label.grid(row=5, column=0, columnspan=2, pady=20)

        ############### Stats Frame ################
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.grid_columnconfigure(0, weight=1)
        self.stats_frame.pack_forget()
        self.selected_exercise = None
        # Title for Stats Frame
        self.stats_title_label = ctk.CTkLabel(self.stats_frame, text="Stats", font=("Arial", 36))
        self.stats_title_label.grid(row=0, column=0, columnspan=2, pady=20)
        # Back Button
        self.stats_back_button = ctk.CTkButton(self.stats_frame, text="Back", command=self.show_main)
        self.stats_back_button.grid(row=1, column=0, sticky="w", padx=20, pady=10)
        # Select exercise button
        self.select_exercise_button = ctk.CTkButton(self.stats_frame, text="Select Exercise", command=self.select_exercise)
        self.select_exercise_button.grid(row=1, column=1, padx=20, pady=10)
        # Frame for graph
        self.graph_frame = ctk.CTkFrame(self.stats_frame,fg_color="lightgrey")
        self.graph_frame.grid(row=5, column=0, columnspan=2, pady=20,sticky="ns")
        self.plot_button = ctk.CTkButton(self.stats_frame, text="Plot Graph", command=self.plot_graph)
        self.plot_button.grid(row=6, column=0, columnspan=2, pady=10)
        # Selected Exercise Label
        self.selected_exercise_label = ctk.CTkLabel(self.stats_frame, text=f"Selected Exercise: {self.selected_exercise}", font=("Arial", 14))
        self.selected_exercise_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.mainloop()
    def select_exercise(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ctk.CTkToplevel(self)
            self.toplevel_window.geometry("400x300")
            self.toplevel_window.title("Select Exercise")
            self.toplevel_window.columnconfigure(0, weight=1)
            self.toplevel_window.grab_set()
            if os.path.exists("comboboxlist.pkl"): 
                with open("comboboxlist.pkl", "rb") as f:
                    self.ex_list = pickle.load(f)
                    f.close()
            else:
                self.ex_list = []

            self.exercise_label = ctk.CTkLabel(self.toplevel_window, text="Select Exercise:", font=("Arial", 14))
            self.exercise_label.grid(row=0, column=0, padx=10, pady=5)
            
            self.exercise_listbox = ctk.CTkComboBox(self.toplevel_window, values=self.ex_list, state="readonly")
            self.exercise_listbox.grid(row=0, column=1, padx=10, pady=10)
            
            self.from_date_label = ctk.CTkLabel(self.toplevel_window, text="From Date:")
            self.from_date_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
            self.from_date_entry = DateEntry(self.toplevel_window, width=20, font=("Arial,13"), date_pattern="DD/MM/YYYY", background='E0E6E9', foreground='white', borderwidth=2)
            self.from_date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

            self.to_date_label = ctk.CTkLabel(self.toplevel_window, text="To Date:")
            self.to_date_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
            self.to_date_entry = DateEntry(self.toplevel_window, width=20, font=("Arial,13"), date_pattern="DD/MM/YYYY", background='E0E6E9', foreground='white', borderwidth=2)
            self.to_date_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

            self.confirm_button = ctk.CTkButton(self.toplevel_window, text="Confirm", command=self.confirm_selection)
            self.confirm_button.grid(row=3, column=0, padx=10, pady=10,columnspan = 2)
        else:
            self.toplevel_window.focus()

    def confirm_selection(self):
        self.selected_exercise = self.exercise_listbox.get()
        self.selected_exercise_label.configure(text=f"Selected Exercise: {self.selected_exercise}\nFrom: {self.from_date_entry.get()}\nTo: {self.to_date_entry.get()}")
        self.from_date = self.from_date_entry.get()
        self.to_date = self.to_date_entry.get()
        self.toplevel_window.destroy()
    def calculate_bmi(self):
        try:
            height = float(self.height_entry.get()) / 100  # Convert cm to meters
            weight = float(self.weight_entry.get())
            if height <= 0 or weight <= 0:
                raise ValueError("Height and weight must be positive numbers.")
            bmi = weight / (height ** 2)
            self.result_label.configure(text=f"Your BMI is: {bmi:.2f}")
        except ValueError:
            self.result_label.configure(text="Please enter valid positive numbers.")


    def update_log_table(self):
        for widget in self.log_table_frame.winfo_children():
            widget.destroy()
        if len(self.data) > 0:
            for i, tracker in enumerate(self.data):
                date_label = ctk.CTkLabel(self.log_table_frame, text=tracker.date, font=("Arial", 14),text_color="black")
                date_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

                name_label = ctk.CTkLabel(self.log_table_frame, text=tracker.name, font=("Arial", 14), text_color="black")
                name_label.grid(row=i, column=1, padx=10, pady=5, sticky="ew") 

                view_button = ctk.CTkButton(self.log_table_frame, text="View", command=lambda t=tracker: self.view_workout(t))
                view_button.grid(row=i, column=2, padx=10, pady=5, sticky="e")
                delete_button = ctk.CTkButton(self.log_table_frame, text="Delete", command=lambda t=tracker: self.delete_workout(t))
                delete_button.grid(row=i, column=3, padx=10, pady=5, sticky="ew")
        self.log_table_frame.update_idletasks()

    def delete_workout(self, tracker):
        self.data.remove(tracker)
        self.update_log_table()
        with open("data.pkl", "wb") as f:
            pickle.dump(self.data, f)
            f.close()
    def view_workout(self, tracker):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ctk.CTkToplevel(self)
            self.toplevel_window.geometry("400x300")
            self.toplevel_window.title(tracker.name)
            self.toplevel_window.grab_set()  

            for i, exercise in enumerate(tracker.exercises):
                exercise_label = ctk.CTkLabel(self.toplevel_window, text=f"{exercise.name}: {exercise.weight}kg: {exercise.sets} sets x {exercise.reps} reps", font=("Arial", 14))
                exercise_label.pack(pady=5)
        else:
            self.toplevel_window.focus()
    def clear_bmi(self):
        self.height_entry.delete(0, 'end')
        self.weight_entry.delete(0, 'end')
        self.result_label.configure(text="")
    def open_new_workout(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = TrackerWindow(self) 
            self.toplevel_window.grab_set()  
        else:
            self.toplevel_window.focus() 
    def show_tracker(self):
        self.mainFrame.pack_forget()
        self.bmi_frame.pack_forget()
        self.trackerFrame.pack(fill="both", expand=True)
    def show_main(self):
        self.trackerFrame.pack_forget()
        self.bmi_frame.pack_forget()
        self.stats_frame.pack_forget()
        self.clear_bmi()
        self.mainFrame.pack(fill="both", expand=True)
    def show_bmi(self):
        self.mainFrame.pack_forget()
        self.trackerFrame.pack_forget()
        self.bmi_frame.pack(fill="both", expand=True)
    def show_stats(self):
        self.mainFrame.pack_forget()
        self.trackerFrame.pack_forget()
        self.bmi_frame.pack_forget()
        self.stats_frame.pack(fill="both", expand=True)
    def plot_graph(self):
        if not self.selected_exercise:
            self.error_label = ctk.CTkLabel(self.stats_frame, text="No exercise selected", text_color="red", font=("Arial", 14))
            self.error_label.grid(row=7, column=0, columnspan=2, pady=10)
            self.after(2000, self.error_label.destroy)
            return

        from_date = datetime.datetime.strptime(self.from_date, "%d/%m/%Y")
        to_date = datetime.datetime.strptime(self.to_date, "%d/%m/%Y")

        dates = []
        intensities = []

        for tracker in self.data:
            for exercise in tracker.exercises:
                if exercise.name == self.selected_exercise:
                    exercise_date = datetime.datetime.strptime(exercise.date, "%d/%m/%Y")
                    if from_date <= exercise_date <= to_date:
                        dates.append(exercise_date)
                        intensities.append(exercise.get_intensity())

        if dates and intensities:
            fig, ax = plt.subplots(figsize=(10, 6)) 
            ax.plot(dates, intensities, marker='o')
            ax.set_title(f"Intensity of {self.selected_exercise} Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("Intensity")
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))

            for widget in self.graph_frame.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            plt.close(fig)
        
class TrackerWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x400")

        ############ Name and Date Frame ############

        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(fill="both", expand=True)
        self.info_frame.grid_columnconfigure(0, weight=1)
        
        # Title Label
        self.title_label = ctk.CTkLabel(self.info_frame, text="Workout Logger", font=("Arial", 24))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Workout Name
        self.workout_name_label = ctk.CTkLabel(self.info_frame, text="Workout Name:")
        self.workout_name_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.workout_name_entry = ctk.CTkEntry(self.info_frame)
        self.workout_name_entry.grid(row=1, column=1, padx=10, pady=5)
        # Date picker
        self.date_label = ctk.CTkLabel(self.info_frame, text="Date:")
        self.date_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.date_entry = DateEntry(self.info_frame, width=20, font=("Arial,13"),date_pattern="DD/MM/YYYY", background='E0E6E9', foreground='white', borderwidth=2)
        self.date_entry.grid(row=2, column=1, padx=10, pady=5)
        # Next button 
        self.next_button = ctk.CTkButton(self.info_frame, text="Next", command=self.show_logger_frame)
        self.next_button.grid(row=3, column=0, columnspan=2, pady=10)

        ########### Logging Frame ############
        self.logger_frame = ctk.CTkFrame(self)
        self.logger_frame.pack_forget()
        self.logger_frame.grid_columnconfigure(0, weight=1)
        self.ex_list = []
        # Title Label
        self.label = ctk.CTkLabel(self.logger_frame, text="", font=("Arial", 24), pady=10)
        self.label.grid(row=0, column=0, columnspan=2)
        # Exercise selection
        self.exercise_label = ctk.CTkLabel(self.logger_frame, text="Exercise:")
        self.exercise_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        # Dropdown for saved exercises
        if not os.path.exists("comboboxlist.pkl"):
            with open("comboboxlist.pkl", "wb") as f:
                self.ex_list = ["None"]
                pickle.dump(self.ex_list, f)
                f.close()
        else:
            with open("comboboxlist.pkl", "rb") as f:
                self.ex_list = pickle.load(f)
                f.close()
        
        self.exercise_dropdown = ctk.CTkComboBox(self.logger_frame, values=self.ex_list, state="readonly")
        self.exercise_dropdown.set(self.ex_list[0])
        self.exercise_dropdown.grid(row=1, column=1, padx=10, pady=5)
        # Entry for new exercise
        self.new_exercise_entry = ctk.CTkEntry(self.logger_frame, placeholder_text="Or enter new")
        self.new_exercise_entry.grid(row=2, column=1, padx=10, pady=5)
        # Weight, Sets, Reps inputs
        self.weight_label = ctk.CTkLabel(self.logger_frame, text="Weight (kg):")
        self.weight_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.weight_entry = ctk.CTkEntry(self.logger_frame)
        self.weight_entry.grid(row=3, column=1, padx=10, pady=5)
        self.sets_label = ctk.CTkLabel(self.logger_frame, text="Sets:")
        self.sets_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.sets_entry = ctk.CTkEntry(self.logger_frame)
        self.sets_entry.grid(row=4, column=1, padx=10, pady=5)
        self.reps_label = ctk.CTkLabel(self.logger_frame, text="Reps:")
        self.reps_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.reps_entry = ctk.CTkEntry(self.logger_frame)
        self.reps_entry.grid(row=5, column=1, padx=10, pady=5)
        # Log and Finish buttons
        self.log_button = ctk.CTkButton(self.logger_frame, text="Log", command=self.log_workout)
        self.log_button.grid(row=6, column=0, pady=10)
        self.finish_button = ctk.CTkButton(self.logger_frame, text="Complete", command=self.finish_logging)
        self.finish_button.grid(row=6, column=1, pady=10)

    def log_workout(self): #TODO Don't allow user to use combo box and new entry at the same time
        date = self.date_entry.get()
        if self.new_exercise_entry.get() == "" and self.exercise_dropdown.get() == "None":
            self.confirmation_label = ctk.CTkLabel(self.logger_frame, text="Please select or enter an exercise.", text_color="red")
            self.confirmation_label.grid(row=7, column=0, columnspan=2, pady=10)
            self.after(2000, self.confirmation_label.destroy)
            return
        if self.new_exercise_entry.get() != "" and self.exercise_dropdown.get() != "None":
            self.confirmation_label = ctk.CTkLabel(self.logger_frame, text="Please use only one exercise input method.", text_color="red")
            self.confirmation_label.grid(row=7, column=0, columnspan=2, pady=10)
            self.after(2000, self.confirmation_label.destroy)
            return
        exercise = self.exercise_dropdown.get() if self.new_exercise_entry.get() == "" else self.new_exercise_entry.get()
        if   self.new_exercise_entry.get() != "" and self.new_exercise_entry.get() not in list(self.exercise_dropdown.cget("values")):
            new_exercise = self.new_exercise_entry.get()
            current_values = list(self.exercise_dropdown.cget("values"))
            current_values.append(new_exercise)
            with open("comboboxlist.pkl", "wb") as f:
                pickle.dump(current_values, f)
                f.close()
            self.exercise_dropdown.configure(values=current_values)
        try:
            weight = float(self.weight_entry.get())
            sets = int(self.sets_entry.get())
            reps = int(self.reps_entry.get())
            
            if weight <= 0 or sets <= 0 or reps <= 0:
                raise ValueError("Weight, sets, and reps must be positive numbers.")
        except ValueError:
            self.confirmation_label = ctk.CTkLabel(self.logger_frame, text="Please enter valid positive numbers.", text_color="red")
            self.confirmation_label.grid(row=7, column=0, columnspan=2, pady=10)
            self.after(2000, self.confirmation_label.destroy)
            return

        self.exercise_dropdown.set('None')
        self.new_exercise_entry.delete(0, 'end')
        self.weight_entry.delete(0, 'end')
        self.sets_entry.delete(0, 'end')
        self.reps_entry.delete(0, 'end')

        temp = Weightlifting(date, exercise, weight, sets, reps)
        self.master.tracker.add_exercise(temp)
        self.confirmation_label = ctk.CTkLabel(self.logger_frame, text="Logged successfully!", text_color="green")
        self.confirmation_label.grid(row=7, column=0, columnspan=2, pady=10)
        self.after(2000, self.confirmation_label.destroy)

    def show_logger_frame(self):
        try:
            name = self.workout_name_entry.get()
            if name == "":
                raise ValueError("Workout name cannot be empty.")
        except ValueError as e:
            self.confirmation_label = ctk.CTkLabel(self.info_frame, text=str(e), text_color="red")
            self.confirmation_label.grid(row=4, column=0, columnspan=2, pady=10)
            self.after(2000, self.confirmation_label.destroy)
            return
        date = self.date_entry.get()
        self.label.configure(text=name)
        self.master.tracker = Tracker(name, date)  # IMPORTANT - create a new tracker object here
        self.info_frame.pack_forget()
        self.logger_frame.pack(fill="both", expand=True)
    def finish_logging(self):
        self.master.data.append(self.master.tracker)
        self.master.tracker = None
        with open("data.pkl", "wb") as f:
            pickle.dump(self.master.data, f)
            f.close()
        self.master.update_log_table()
        self.destroy()
MainPage()