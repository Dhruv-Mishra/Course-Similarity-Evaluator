# Course-Similarity-Evaluator
A tool which helps both students and teachers to identify the overlapping courses within the course directory to avoid course redundacy within an instituition.<br>
![image](https://user-images.githubusercontent.com/88452809/234382877-f9b42e39-d151-4f75-a059-f1798c2e56ff.png)
## About
A tool which helps both students and teachers to identify the overlapping courses within the course directory to avoid offering redundant courses. It allows its users to search within their insituition's course directory simply by entering the name. To make things even simpler, the user does not even have to write the full name. Even short forms like intro(for introduction), b/w (for between) etc. are accepted.
To add to this, there is also an option of finding courses similar to a set of courses if the user wishes for the same. 

## Features
#### Course Similarity Matching 
The core component of the system is to allow the user to find the courses similar to their selected course in the course directory. For this, the user may search by name of the course.  The system will then suggest the courses which are likely to be similar to the course that the user input.

#### Multi Course Similarity
Extending this core functionality to multiple courses, we decided to implement the similarity matching on a set of courses as well. For this, we take the take the similarity metric of all the courses in the dataset with respect to each of the input courses. Then, for each course in the dataset, we take the sum of the similarity metric obtained with respect to each input. The courses which have the highest resulting sum are the ones we suggest.

#### Dataset Specific Spell Correction
We have added the functionality of correcting wrong spellings for the user. This spell correct, however, is not generic and is specific to our dataset. This ensures that our input is not corrected to a generic english sentence, which cannot be found in our dataset.

#### Inbuilt Data Scrapper Support (.xlsx and .csv)
We have implemented a preprocessor which takes in the input as a file pointer object and extracts the data from the specified file. For this, we used python's Openpyxl to read excel files cell by cell, and identify the cells that contain possibly useful information. We then preprocess this information and neatly pack it into a Course object, which can further be used for various purposes.

#### Automatic Similarity Updation Upon New Additions
To avoid unnecessary computation, and to make the system faster, we have implemented event specific updation. This means that the system will work with each new added course, but it will not compute the similarity metrics until a function using these metrics is called upon. 

## Interface
*This is a low fidelity prototype of the interface, the high fidelity prototype and an actual working interface are in the works
![image](https://user-images.githubusercontent.com/88452809/234382099-503bd13f-cf36-474c-a22d-c6051f1c4e23.png)
![image](https://user-images.githubusercontent.com/88452809/234382292-c74c4dad-9670-48bd-8aa4-be86365d4290.png)
![image](https://user-images.githubusercontent.com/88452809/234382359-d0e49561-e653-42c3-87d0-60a92feaf95c.png)
## How To Use
### Prerequisites
##### For running this code, you need Python 3 (preferably >= 3.7.9 ) installed on your system.
##### You must have the the following dependencies installed:
&nbsp;&nbsp;&nbsp;&nbsp; - `Pandas`<br>
&nbsp;&nbsp;&nbsp;&nbsp; - `Numpy`<br>
&nbsp;&nbsp;&nbsp;&nbsp; - `Tensorflow`<br>
&nbsp;&nbsp;&nbsp;&nbsp; - `Tensorflow Hub`<br>
&nbsp;&nbsp;&nbsp;&nbsp; - `Sklearn`<br>
&nbsp;&nbsp;&nbsp;&nbsp; - `Difflib`<br>
&nbsp;&nbsp;&nbsp;&nbsp; - `Pickle`<br>
&nbsp;&nbsp;&nbsp;&nbsp; - `Openpyxl`<br>

Ensure that you have atleast <span style="color:red">**50 MB**</span> of free space on your system.

### Using the System
To start, you need to initialize a <span style="color:blue"> **Course_Loader** </span> object. This is where all the data will be stored, processed and similarity will be calculated. It can be initialized in the following way:

    c = Course_Loader()

Once the object is loaded, you now have to add all the xlsx files containing the information about the courses. To add a new course, you simply have to call the <span style="color:orange">**addCourse** </span> function of your <span style="color:blue">**Course_Loader** </span> object. For this you need to retrive the directory of the .xlsx files containing your data. 
In our case, the files are located in the Data folder in the same directory as our python file. 
    
	path = os.getcwd()
	path = str(path) + "\\Data\\"
	csv_files = glob.glob(os.path.join(path, "*.xlsx"))    #Retrieving the directory of the data
	
	for f in csv_files:
    	c.addCourse(f)    #Adding each course using the addCourse function

Now that all the courses have been added, you can use the system. Note that you may add a new course at any given time and the system will update itself to include this in the results.
Now, to make a query, you have to call the <span style="color:orange"> **combine_recommendations** </span> function of your <span style="color:blue"> **Course_Loader** </span> object. The input to this function will be a list of strings, here each string denotes the course that you wish to input (see the examples for more clarity).

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
