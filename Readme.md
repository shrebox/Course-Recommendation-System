# Course Recommendation System

Detailed report available at: https://www.overleaf.com/read/fwmrcwxwpkck

A system that will help in a personalized recommendation of courses for an upcoming semester based on the performance of previous semesters.

#### For running individual models

1. User Based: ```$ python user.py```	
2. Item Based: ```$ python item.py```
3. Warp MF: ```$ python hmf_warp_log.py```
4. Logistic MF: ```$ python hmf_warp_log.py```
5. Auto encoders: ```$ python auto_enc.py```

It will return top 5 recommended courses and their grades. Also it will return top 5 courses that are compared with ground truth.

#### For running the web app locally on your system do
1. node main.js 
2. Go to the browser and browse http://localhost:3000/
3. Enter the student ID and Semester for which you want top 5 courses alongwith their the grades.

matrix_creation.py is used to import the data into different models. Used as an import file.

Packages need to be installed: LightFM, sklearn, theano, pandas, numpy, scipy, npm (express, body-parser and ejs modules for nodejs).
