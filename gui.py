import customtkinter as ctk
from tkcalendar import DateEntry
import pickle
from exercise import Weightlifting, Cardio, Tracker


ctk.set_default_color_theme("theme.json")
class MainPage(ctk.CTk):
    def __init__(self,*args,**kwargs):
        self.tracker=None
        self.data = []
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
        self.log_table_frame.grid_columnconfigure(1, weight=1)  # Ensure the name_label is centered
        self.mainloop()
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
        self.log_table_frame.update_idletasks()

    def view_workout(self, tracker):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ctk.CTkToplevel(self)
            self.toplevel_window.geometry("400x300")
            self.toplevel_window.title(tracker.name)
            self.toplevel_window.grab_set()  

            for i, exercise in enumerate(tracker.exercises):
                exercise_label = ctk.CTkLabel(self.toplevel_window, text=f"{exercise.name}: {exercise.sets} sets x {exercise.reps} reps", font=("Arial", 14))
                exercise_label.pack(pady=5)
        else:
            self.toplevel_window.focus()
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
        self.exercise_dropdown = ctk.CTkComboBox(self.logger_frame, values=["Bench Press"], state="readonly")
        self.exercise_dropdown.set("Select exercise")  ## TODO Error handle when user does not select an exercise
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

    def log_workout(self):
        # Collect data from entries
        date = self.date_entry.get()
        exercise = self.exercise_dropdown.get() if self.new_exercise_entry.get() == "" else self.new_exercise_entry.get()
        weight = self.weight_entry.get()
        sets = self.sets_entry.get()
        reps = self.reps_entry.get()

        # Add new exercise to dropdown if it's not empty and not already in the list
        if self.new_exercise_entry.get() != "" and self.new_exercise_entry.get() not in list(self.exercise_dropdown.cget("values")):
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
        date = self.date_entry.get()
        self.label.configure(text=name)
        self.master.tracker = Tracker(name, date)  # Assign to self.master.tracker
        self.info_frame.pack_forget()
        self.logger_frame.pack(fill="both", expand=True)
    def finish_logging(self):
        self.master.data.append(self.master.tracker)
        self.master.tracker = None
        print("Length: ", len(self.master.data))
        self.master.update_log_table()
        self.destroy()
        print("Finish")
MainPage()