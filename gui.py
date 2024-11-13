import customtkinter as ctk
from tkcalendar import DateEntry
import pickle
from exercise import Weightlifting, Cardio, Tracker


ctk.set_default_color_theme("theme.json")
class MainPage(ctk.CTk):
    def __init__(self,*args,**kwargs):
        self.tracker = Tracker()
        super().__init__(*args,**kwargs)
        self.geometry("1000x600")
        self.title("Exercise Tracker")

        ############### Main Frame ################

        self.mainFrame = ctk.CTkFrame(self)
        self.mainFrame.pack(fill="both", expand=True)
        self.mainFrame.grid_columnconfigure(0, weight=1)
        # Title
        self.title_label = ctk.CTkLabel(self.mainFrame, text="Fitness Tracker", font=("Arial", 36))
        self.title_label.grid(row=0, column=0, pady=100)
        # BMI Button
        self.bmi_button = ctk.CTkButton(self.mainFrame, text="BMI Calculator")
        self.bmi_button.grid(row=1, column=0, pady=10)
        # Tracker Button
        self.tracker_button = ctk.CTkButton(self.mainFrame, text="Tracker",command=self.show_tracker)
        self.tracker_button.grid(row=2, column=0, pady=10)
        # Stats Button
        self.stats_button = ctk.CTkButton(self.mainFrame, text="Stats")
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
        self.log_table_frame.grid_columnconfigure(0, weight=1)
        # Add content to log_table_frame
        self.log_table = ctk.CTkLabel(self.log_table_frame, text="No logs yet", font=("Arial", 14), text_color="grey")
        self.log_table.grid(row=0, column=0, pady=10)

        self.mainloop()
    def open_new_workout(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = TrackerWindow(self) 
            self.toplevel_window.grab_set()  
        else:
            self.toplevel_window.focus() 
    def show_tracker(self):
        self.mainFrame.pack_forget()
        self.trackerFrame.pack(fill="both", expand=True)
    def show_main(self):
        self.trackerFrame.pack_forget()
        self.mainFrame.pack(fill="both", expand=True)
        
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
        self.date_entry = DateEntry(self.info_frame, width=20, font=("Arial,13"), background='E0E6E9', foreground='white', borderwidth=2)
        self.date_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Next button to proceed to logging frame
        self.next_button = ctk.CTkButton(self.info_frame, text="Next", command=self.show_logger_frame)
        self.next_button.grid(row=3, column=0, columnspan=2, pady=10)

        ########### Logging Frame ############
        self.logger_frame = ctk.CTkFrame(self)
        self.logger_frame.pack_forget()
        self.logger_frame.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self.logger_frame, text="", font=("Arial", 24), pady=10)
        self.label.grid(row=0, column=0, columnspan=2)

        # Exercise selection
        self.exercise_label = ctk.CTkLabel(self.logger_frame, text="Exercise:")
        self.exercise_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        # Dropdown for saved exercises
        self.exercise_dropdown = ctk.CTkComboBox(self.logger_frame, values=["Bench Press"], state="readonly")  # Add exercise options here
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
        # Log and History buttons
        self.log_button = ctk.CTkButton(self.logger_frame, text="Log", command=self.log_workout)
        self.log_button.grid(row=6, column=0, pady=10)
        self.history_button = ctk.CTkButton(self.logger_frame, text="Workout History", command=self.view_history)
        self.history_button.grid(row=6, column=1, pady=10)

    def log_workout(self):
        # Collect data from entries
        date = self.date_entry.get()
        exercise = self.exercise_dropdown.get() if self.new_exercise_entry.get() == "" else self.new_exercise_entry.get()
        weight = self.weight_entry.get()
        sets = self.sets_entry.get()
        reps = self.reps_entry.get()

        # Add new exercise to dropdown if it's not empty and not already in the list
        if self.new_exercise_entry.get() != "" and self.new_exercise_entry.get() not in self.exercise_dropdown.cget("values"):
            new_exercise = self.new_exercise_entry.get()
            current_values = list(self.exercise_dropdown.cget("values"))
            current_values.append(new_exercise)
            self.exercise_dropdown.configure(values=current_values)

        self.exercise_dropdown.set('')
        self.new_exercise_entry.delete(0, 'end')
        self.weight_entry.delete(0, 'end')
        self.sets_entry.delete(0, 'end')
        self.reps_entry.delete(0, 'end')

        temp = Weightlifting(date, exercise, weight, sets, reps)
        self.master.tracker.add_exercise(temp)
        print(self.master.tracker.logDict) # TODO remove this later when done testing

        # Save the workout data to a file (append mode)
        # with open("workout_log.pkl", "ab") as f:
        #     pickle.dump(workout_data, f)
    def show_logger_frame(self):
        name = self.workout_name_entry.get()
        self.label.configure(text=name)
        self.info_frame.pack_forget()
        self.logger_frame.pack(fill="both", expand=True)
    def view_history(self):
        # Placeholder function for viewing workout history
        print("View workout history")
MainPage()