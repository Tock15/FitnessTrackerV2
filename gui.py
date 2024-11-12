import customtkinter as ctk
import pickle

class MainPage(ctk.CTk):
    def __init__(self,*args,**kwargs):
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

        ############### Traacker Frame ################

        self.trackerFrame = ctk.CTkFrame(self)
        self.trackerFrame.grid_columnconfigure(0, weight=1)
        self.trackerFrame.pack_forget()  # Initially hide the tracker frame
        # Title for Tracker Frame
        self.tracker_title_label = ctk.CTkLabel(self.trackerFrame, text="Workout Log", font=("Arial", 36))
        self.tracker_title_label.grid(row=0, column=0, pady=20)
        # Back Button
        self.back_button = ctk.CTkButton(self.trackerFrame, text="Back", command=self.show_main)
        self.back_button.grid(row=1, column=0, sticky="w", padx=20, pady=10)
        # Log New Workout Button
        self.log_new_workout_button = ctk.CTkButton(self.trackerFrame, text="Log New Workout", command=self.open_tracker)
        self.log_new_workout_button.grid(row=1, column=0, sticky="e", padx=20, pady=10)


        self.mainloop()
    def open_tracker(self):
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

        self.label = ctk.CTkLabel(self, text="Workout Log", font=("Arial", 24), pady=10)
        self.label.grid(row=0, column=0, columnspan=2)

        # Date picker (placeholder)
        self.date_label = ctk.CTkLabel(self, text="Date:")
        self.date_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.date_entry = ctk.CTkEntry(self, placeholder_text="Select Date")
        self.date_entry.grid(row=1, column=1, padx=10, pady=5)

        # Exercise selection
        self.exercise_label = ctk.CTkLabel(self, text="Exercise:")
        self.exercise_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        
        # Dropdown for saved exercises
        self.exercise_dropdown = ctk.CTkComboBox(self, values=["Bench Press", "Squat", "Deadlift"])  # Add exercise options here
        self.exercise_dropdown.grid(row=2, column=1, padx=10, pady=5)

        # Entry for new exercise
        self.new_exercise_entry = ctk.CTkEntry(self, placeholder_text="Or enter new")
        self.new_exercise_entry.grid(row=3, column=1, padx=10, pady=5)

        # Weight, Sets, Reps inputs
        self.weight_label = ctk.CTkLabel(self, text="Weight (kg):")
        self.weight_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.weight_entry = ctk.CTkEntry(self)
        self.weight_entry.grid(row=4, column=1, padx=10, pady=5)

        self.sets_label = ctk.CTkLabel(self, text="Sets:")
        self.sets_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.sets_entry = ctk.CTkEntry(self)
        self.sets_entry.grid(row=5, column=1, padx=10, pady=5)

        self.reps_label = ctk.CTkLabel(self, text="Reps:")
        self.reps_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.reps_entry = ctk.CTkEntry(self)
        self.reps_entry.grid(row=6, column=1, padx=10, pady=5)

        # Log and History buttons
        self.log_button = ctk.CTkButton(self, text="Log", command=self.log_workout)
        self.log_button.grid(row=7, column=0, pady=10)

        self.history_button = ctk.CTkButton(self, text="Workout History", command=self.view_history)
        self.history_button.grid(row=7, column=1, pady=10)

    def log_workout(self):
        # Placeholder function for logging the workout
        print("Workout logged!")

    def view_history(self):
        # Placeholder function for viewing workout history
        print("View workout history")
MainPage()