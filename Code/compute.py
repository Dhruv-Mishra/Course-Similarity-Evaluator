# import necessary libraries
import pandas as pd
import os
import glob
import openpyxl
import warnings
import re
import tensorflow_hub as hub
import difflib
import numpy as np
import math
from sklearn.metrics.pairwise import linear_kernel
import pickle

warnings.simplefilter(action='ignore', category=UserWarning)

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

class Course_Loader:
    course_names = {}
    course_codes = {}
    names_list = []
    codes_list = []
    df = -1
    newEntries = False
    cosine_sim = -1
    indices = -1

    def __init__(self):
        data = ['Course Name','Course Code','Course Description']
        self.df = pd.DataFrame(columns = data)
        self.course_codes = {}
        self.course_names = {}
        self.names_list = []
        self.codes_list = []
        self.newEntries = False

    def addCourse(self, f):
        newCourse = Course(f)
        self.course_names[newCourse.name] = newCourse
        self.course_codes[newCourse.code] = newCourse
        new_df = pd.DataFrame({"Course Name":[newCourse.name],"Course Code":[newCourse.code], "Course Description":[newCourse.description]})
        self.df = self.df.append(new_df,ignore_index=True)
        self.newEntries = True # Keeps track of if new entries were added after calculating the similarity check 

    def findbyCode(self,code, exact = False):
        ans = []
        if(not exact):
            code = "".join(code.lower().split())
            out = difflib.get_close_matches(code, self.codes_list, cutoff= 0.0000001, n = 10)
            for i in out:
                ans.append(self.course_codes[i])
        if(code in self.course_codes.keys()):
            ans.append(self.course_codes[code])
        return ans
    
    def findbyName(self,name, exact = False):
        ans = []
        if(not exact):
            name = "".join(name.lower().split())
            out = difflib.get_close_matches(name, self.names_list, cutoff= 0.0000001, n = 10)
            for i in out:
                ans.append(self.course_names[i])
        if(name in self.course_names.keys()):
            ans.append(self.course_names[name])
        return ans

    def initialize_recommender(self):
        if(self.newEntries):
            self.newEntries = False
            self.df = self.df.dropna()
            self.df = self.df.drop_duplicates(subset='Course Name', keep='first')
            self.df = self.df.reset_index(drop=True)
            self.names_list = self.df['Course Name'].unique()
            self.codes_list = self.df['Course Code'].unique()
            encodings = embed(self.df['Course Description'])
            matrix = np.vstack(encodings)
            cosine_sim = linear_kernel(matrix, matrix)
            indices = pd.Series(self.df.index, index=self.df['Course Name'])
            self.cosine_sim = cosine_sim
            self.indices = indices

    def get_recommendations(self, title):
        idx = self.indices[title]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        return sim_scores
    
    def combine_recommendations(self,titles):
        out = []
        self.initialize_recommender()
        for i in range(len(self.df)):
            out.append([i,0])
        for org_title in titles:            #### Names may or may not be present in the dataset, finds the closest title matching in the dataset
            title = difflib.get_close_matches(org_title, self.names_list, cutoff= 0.0000001, n = 1)[0]  #Searching the closest match in the dataset 
            cur_out = self.get_recommendations(title)
            for score in range(len(cur_out)):
                out[score][1] += cur_out[score][1]
        final_score = sorted(out, key=lambda x: x[1], reverse=True)
        df_indices = [i[0] for i in final_score][1:10]
        result = self.df.iloc[df_indices]
        return result
                     
class Course:
    course_name_list = set([])
    file_name = ""
    code = ""
    description = ""
    embedding = []
    similarity_matrix = []
    file_ptr = ""
    name = ""

    def __init__(self, file_pointer):
        self.file_name = str(f)
        self.file_ptr = file_pointer
        self.description = self.find_description()
        self.code = self.find_code()
        self.name = self.find_name()
        if(self.description != -1):
            self.embedding = self.compute_embedding()

    def find_description(self):
        workbook = openpyxl.load_workbook(self.file_ptr)
        worksheet = workbook.active
        description_row = -1
        description_col = -1
        for coll in range(1,6):
            for roww in range(1,20):
                if("description" in "".join(re.sub(r'[^\w\s]','', re.sub(r'\d+','',str(worksheet.cell(row=roww, column=coll).value).lower())).split())):
                    description_row = roww
                    description_col = coll
                    return str(worksheet.cell(row=roww, column=coll+1).value)
        return "-1"
    
    def find_code(self):
        f = self.file_ptr
        workbook = openpyxl.load_workbook(f)
        worksheet = workbook.active
        for coll in range(1,4):
            for roww in range(1,5):
                cell_val = "".join("".join(str(worksheet.cell(row=roww, column=coll).value).lower().strip().split()).split("-"))
                if('code' in cell_val):
                    cell_val = " ".join("".join(str(worksheet.cell(row=roww, column=coll+1).value).lower().strip().split()).split("-"))
                    return cell_val
        #If not found in the sheet, find in file_name 
        file_name = str(f).split("\\")[-1]
        file_name = file_name.split("/")[-1]
        file_name = file_name.split(".")
        if(len(file_name) >= 2):
            file_name = file_name[-2]
        file_name = "".join(file_name.lower().split())
        return file_name 
    
    def find_name(self):
        f = self.file_ptr
        workbook = openpyxl.load_workbook(f)
        worksheet = workbook.active
        for coll in range(1,4):
            for roww in range(1,5):
                cell_val = "".join("".join(str(worksheet.cell(row=roww, column=coll).value).lower().strip().split()).split("-"))
                if('name' in cell_val):
                    cell_val = " ".join("".join(str(worksheet.cell(row=roww, column=coll+1).value).lower().strip().split()).split("-"))
                    return cell_val
        #If not found in the sheet, find in file_name 
        file_name = str(f).split("\\")[-1]
        file_name = file_name.split("/")[-1]
        file_name = file_name.split(".")
        if(len(file_name) >= 2):
            file_name = file_name[-2]
        file_name = "".join(file_name.lower().split())
        return file_name

    def compute_embedding(self):
        return embed([self.description])
   
path = os.getcwd()
path = str(path) + "\\Data\\"
csv_files = glob.glob(os.path.join(path, "*.xlsx"))

c = Course_Loader()

for f in csv_files:
    c.addCourse(f)

