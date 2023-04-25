from Course_Loader import *
import os
import pickle
import glob 

try:                                              #Loading Course_Loader object if it exists
    with open("Course_Loader_Save", "rb") as f:
        c = pickle.load(f)
except:                                           #Creating a new object if it doesn't exist and saving it on the disk

    path = os.getcwd() # Getting the current directory to access the data files
    path = str(path) + "\\Data\\" # Data must be stored inside the Data folder located in the current directory 

    csv_files = glob.glob(os.path.join(path, "*.xlsx")) # Get names of all csv files
    
    c = Course_Loader()

    for f in csv_files:  #Adding files to the course loader object 
        c.addCourse(f)

    with open("Course_Loader_Save", "wb") as f:   #Saving the new object on the disk 
        pickle.dump(c,f)

query = ["machine learning"]
c.combine_recommendations(query)    #Making a query