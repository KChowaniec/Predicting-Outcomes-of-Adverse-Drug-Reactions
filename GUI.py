"""
File: GUI.py
Project: Predicting Outcomes of Adverse Drug Reactions
Author: Kathy Chowaniec
File Description:
This script generates the Graphical User Interface used in predicting outcomes
given the entered input. The PredictOutcome.py script is used by this script
to get the predicted outcome(s).
"""
#use Tkinter to build GUI
from Tkinter import * 
from GUIPredictOutcome import getPrediction #method to return predicted outcome(s)
class AppGUI:
    def __init__(self):
        window = Tk() # Create a window
        window.title("FAERS Predict Outcome") # Set a title
        window.geometry("450x400") #set window size
        self.window = window
        # Add a frame to the window
        frame1 = Frame(window) 
        frame1.pack()  
        
        #gender radiobuttons
        gender = "Gender: "
        gender_label = Label(frame1, text = gender)
        self.gender = IntVar() #store selected radiobutton
        #male radiobutton
        male_btn = Radiobutton(frame1, text = "Male", 
            variable = self.gender, value = 0) 
        #female radiobutton
        female_btn = Radiobutton(frame1, text = "Female", 
            variable = self.gender, value = 1)
        #place labels and buttons on frame
        gender_label.grid(row=1,column=1)
        male_btn.grid(row=1,column=2, padx=2, pady=2)
        female_btn.grid(row=1,column=3, padx=2, pady=2)
        
        frame2 = Frame(window) # Create and add a frame to window
        frame2.pack()
        
        #age
        age = "Age:"
        age_label = Label(frame2, text = age)
        self.age = IntVar() #store entered age
        age_entry = Entry(frame2, textvariable = self.age)
        #place label and input box on frame
        age_label.grid(row=1,column=1,padx=2,pady=2)
        age_entry.grid(row=1,column=2,padx=2,pady=2)
        
        #`age unit drop-down list
        lst1 = ['DEC', 'DY', 'HR', 'MON', 'WK', 'YR']
        self.ageunit = StringVar() #store selection from list
        #add list to frame
        drop = OptionMenu(frame2,self.ageunit,*lst1)
        drop.grid(row = 1, column = 3,padx=2,pady=2)
     
        
        #weight
        frame3 = Frame(window) # Create and add a frame to window
        frame3.pack()
        weight = "Weight "
        weight_label = Label(frame3, text = weight)
        self.weight = IntVar() #store entered weight
        weight_entry = Entry(frame3, textvariable = self.weight)
        #store text and input box on frame
        weight_label.grid(row=1,column=1)
        weight_entry.grid(row=1,column=2)
        
        #weight unit drop-down list
        lst1 = ['KG', 'LBS']
        self.wghtunit = StringVar() #store selected option
        #add list to frame
        drop = OptionMenu(frame3,self.wghtunit,*lst1)
        drop.grid(row=1,column=3,padx=2,pady=2)
        
        frame4 = Frame(window) # Create and add a frame to window
        frame4.pack()          
        
        #country
        country = "Country of occurrence:"
        country_label = Label(frame4, text = country)
        self.country = StringVar() #store entered country
        country_entry = Entry(frame4, textvariable = self.country)
        #store text and input box on frame
        country_label.grid(row=1,column=1)
        country_entry.grid(row=1,column=2,padx=10,pady=10)
        
        #drug name
        frame5=Frame(window)
        frame5.pack()
        drug= "Primary Suspect Drug:"
        drug_label = Label(frame5, text = drug)
        self.drug = StringVar() #store entered drug name
        drug_entry = Entry(frame5, textvariable = self.drug)
        #add text and input box to frame
        drug_label.grid(row=1,column=1)
        drug_entry.grid(row=1,column=2,padx=10,pady=10)
                
        #reason
        frame6 = Frame(window)
        frame6.pack()
        reason="Reason for taking drug:"
        reason_label = Label(frame6, text=reason)
        self.reason = StringVar() #store entered reason for taking a drug
        reason_entry=Entry(frame6, textvariable=self.reason)
        #add text and input box to frame
        reason_label.grid(row=1,column=1)
        reason_entry.grid(row=1,column=2,padx=10,pady=10)
        
        
        frame7 = Frame(window) # Create and add a frame to window
        frame7.pack()          
        
        #reaction 
        effects = "Reaction:"
        effects_label = Label(frame7, text = effects)
        self.effects = StringVar() #store entered reaction
        effects_entry = Entry(frame7, textvariable = self.effects)
        #Predict Outcome button
        btn = Button(frame7, text = "Predict Outcome", command = self.predict)
        #add text, input box and button to frame        
        effects_label.grid(row=1,column=1)
        effects_entry.grid(row=1,column=2,padx=10,pady=20)
        btn.grid(row=2,column=2,padx=10,pady=10)
        self.label = None
        
        window.mainloop() # Create an event loop    
    
    #function to get outcomes from entered input and display
    def predict(self):
        if self.label is not None:
            self.label.destroy() #clear label
        gender_value = self.gender.get()
        info = []
        if gender_value == 0: #determine what gender was selected
            gender = 'M'
        else:
            gender = 'F'
        #store all entered information
        info = [self.age.get(), self.ageunit.get(), gender, self.weight.get(), self.wghtunit.get(), self.country.get(), self.drug.get(), self.reason.get(), self.effects.get()]
        prediction = getPrediction(info) #call method in PredictOutcome.py
        results = []
        #determine predicted outcome from result
        for predict in prediction:
            if prediction[predict] == 'yes':
                if predict == "CA":
                    result = "Congenial Anomaly"
                elif predict == "DS":
                    result = "Disability"
                elif predict == "DE":
                    result = "Death"
                elif predict == "HO":
                    result = "Hospitalization"
                elif predict == "LT":
                    result = "Life-Threatening"
                elif predict == "OT":
                    result = "Other Serious"
                elif predict == "RI":
                    result = "Requires Intervention"
                results.append(result)
        
        frame8 = Frame(self.window) # Create and add a frame to window
        frame8.pack()     
        text = 'Predicted Outcome(s): \n'
        for result in results:
            text = text + result + '  '
        if len(results) == 0:
            text = text + "No outcome could be predicted"
        #add results to frame
        self.label = Label(frame8, text = text)
        self.label.grid(row=1,column=1)

AppGUI() # Create GUI