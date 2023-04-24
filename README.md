# Course-Similarity-Evaluator
A tool which helps both students and teachers to identify the overlapping courses within the course directory to avoid offering redundant courses.

## About

## Features
##### Course Similarity Matching 
##### Multi Course Similarity 
##### Dataset Specific Spell Correction
##### Inbuilt Data Scrapper Support (.xlsx and .csv)
##### Automatic Similarity Updation Upon New Additions

## Working
##### Preprocessing 
##### Spell Correction 
##### Similarity Metric 
##### Query Processing 

## How To Use
### Prerequisites
#####For running this code, you need Python 3 (preferably >= 3.7.9 ) installed on your system.
#####You must have the the following dependencies installed:
&nbsp;&nbsp;&nbsp;&nbsp; - `Pandas`<br>
&nbsp;&nbsp;&nbsp;&nbsp; - `Numpy`<br>
&nbsp;&nbsp;&nbsp;&nbsp; - `Tensorflow`<br>
&nbsp;&nbsp;&nbsp;&nbsp; - `Tensorflow Hub`<br>
&nbsp;&nbsp;&nbsp;&nbsp; - `Sklearn`<br>
&nbsp;&nbsp;&nbsp;&nbsp; - `Difflib`<br>
&nbsp;&nbsp;&nbsp;&nbsp; - `Pickle`<br>
&nbsp;&nbsp;&nbsp;&nbsp; - `Openpyxl`<br>

Ensure that you have atleast <span style="color:red">**50 MB **</span> of free space on your system.

### Using the System
To start, you need to initialize a <span style="color:blue"> ** Course_Loader ** </span> object. This is where all the data will be stored, processed and similarity will be calculated. It can be initialized in the following way:

    c = Course_Loader()

Once the object is loaded, you now have to add all the xlsx files containing the information about the courses. To add a new course, you simply have to call the <span style="color:orange">** addCourse ** </span> function of your <span style="color:blue">** Course_Loader ** </span> object. For this you need to retrive the directory of the .xlsx files containing your data. 
In our case, the files are located in the Data folder in the same directory as our python file. 
    
	path = os.getcwd()
	path = str(path) + "\\Data\\"
	csv_files = glob.glob(os.path.join(path, "*.xlsx"))    #Retrieving the directory of the data
	
	for f in csv_files:
    	c.addCourse(f)    #Adding each course using the addCourse function

Now that all the courses have been added, you can use the system. Note that you may add a new course at any given time and the system will update itself to include this in the results.
Now, to make a query, you have to call the <span style="color:orange"> ** combine_recommendations ** </span> function of your <span style="color:blue"> ** Course_Loader ** </span> object. The input to this function will be a list of strings, here each string denotes the course that you wish to input (see the examples for more clarity).

It would look something like this:

	query = ["Course-1","Course-2","Course-3", ...] #The courses which you wish to search
	c.combine_recommendations(query)

Upon running this, you would get the desired output in the form of a pandas dataframe. The output would contain the top 10 courses similar to your entered courses, in the ranked order with first being the most similar.
## Example Queries
### Single Input Query
**Input Query:**<br>
![image](https://user-images.githubusercontent.com/88545875/234037833-6a198565-85fd-4c9b-b219-92682d1aa160.png)

**Output Generated:**<br>
![image](https://user-images.githubusercontent.com/88545875/234036656-e42b9efa-4334-4dc3-9f35-2e0fdcc11f1e.png)

### Multi Input Query
**Input Query:**<br>
![image](https://user-images.githubusercontent.com/88545875/234040855-262b5270-2ac5-4098-ae25-68799a700a8a.png)

**Output Generated:**<br>
![image](https://user-images.githubusercontent.com/88545875/234041051-552809a2-9bcf-49de-be21-33bb1b2a8183.png)

## Issues
None so far. More extensive testing needed on a larger dataset.
