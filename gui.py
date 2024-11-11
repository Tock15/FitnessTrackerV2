import customtkinter as ctk
import pickle

class MainPage(ctk.CTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.geometry("1000x600")
        self.title("Exercise Tracker")
        self.grid_columnconfigure(0, weight=1)
        self.title_label = ctk.CTkLabel(self, text="Fitness Tracker", font=("Arial", 36))
        self.title_label.grid(row=0, column=0, pady=100)

        self.bmi_button = ctk.CTkButton(self, text="BMI Calculator")
        self.bmi_button.grid(row=1, column=0, pady=10)

        self.tracker_button = ctk.CTkButton(self, text="Tracker",command=self.open_tracker)
        self.tracker_button.grid(row=2, column=0, pady=10)

        self.stats_button = ctk.CTkButton(self, text="Stats")
        self.stats_button.grid(row=3, column=0, pady=10)

        self.toplevel_window = None


        self.mainloop()
    def open_tracker(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = TrackerWindow(self) 
            self.toplevel_window.grab_set()  
        else:
            self.toplevel_window.focus() 
        
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