AI MODULES FOR REALLIST & KARUTHU.AI
DOCUMENTATION

Github Link :  https://github.com/azar011/AI_MODULES.git

1. Voice Recognition :-

Purpose :-
This document defines the hardware infrastructure requirements for deploying a Voice Assistant system that converts Native speech into English text using the Faster-Whisper Large-v3 model. The solution is intended for enterprise environments requiring high transcription accuracy, scalability, reliability, and support for concurrent users.


Solution Overview :-
The voice assistant captures native language audio from users, processes the audio using the Faster-Whisper Large-v3 model, and returns English text output through backend APIs.

API Endpoints :-
1.  /translate  -  It gets the user audio file and returns the task id for each user  [POST]
2.  /status/{task_id} – It gives the Output of recognized Text in the audio  [GET]


How to run :-
1. Open folder in vs code 
2. Open backend folder in Terminal
3. cmd - python -m venv venv
4. cmd - venv/Scripts/activate 
5. cmd - pip install -r requirements.txt
6. python run.py
7. Open another terminal run cmd - celery -A app.tasks worker --pool=threads --
    concurrency=2 --loglevel=info

{ => Ensure that python , pip and redis server have been installed in your system }

Curl Code : curl --location --request POST 'https://seducing-boss-retrial.ngrok-free.dev/'
Field Name : file
2. CAPA Recommendation :-
Purpose :-
The system uses semantic search with embeddings and a vector database to retrieve the most relevant historical CAPA records based on user issues. It is designed for enterprise environments requiring high search accuracy, low response time, scalability, reliability, and support for concurrent users.
Solution Overview :-
The CAPA Recommendation System receives an issue description from the user, converts the text into embeddings using a Sentence Transformer model, searches similar historical CAPA records stored in Qdrant Vector Database, and returns the most relevant Corrective Actions, Root Causes, and Preventive Actions through backend APIs.
API Endpoints :-
1. /generate/capa - Gets the data from the user and returns the task_id . [POST] 
2. /status/{task_id}  - Returns the most relevant CAPA recommendations based on
                                    semantic similarity. [GET]
3. /save-capa  - If user Writes the new capa it will stored in the vector database. [POST] 
How to Run :-
    1. Ensure that Qdrant installed locally. 
    2. Ensure that redis have been installed and running.
    3. Open CAPA recommendation folder in vs code.
    4. Open backend folder in terminal 
    5. cmd -  python -m venv venv
    6. cmd - venv/Scripts/activate 
    7. cmd - pip install -r requirements.txt
    8. Add CAPA historical data in ‘ capa_backend/app/data.escalations.json ‘
    9. Change the Open ai API key in .env file .
    10.  python run.py
    11. Open another terminal run cmd - celery -A app.tasks worker --pool=threads --     
       concurrency=2 --loglevel=info

{ => Ensure that python , pip , redis server , Qdrant have been installed in your system }

3. Escalation Count Prediction :-
 Purpose :-
This document defines the software infrastructure requirements for deploying an Escalation Count Prediction system that predicts the expected number of escalations using historical escalation data. 
Solution Overview :-
The Escalation Count Prediction System receives the hierarchy details (Building, Floor, Department, or Zone) from the user, retrieves the historical escalation records from the database, analyzes previous escalation trends, predicts the expected escalation count, and returns the prediction through backend APIs.
API Endpoints :-
    1. /predict - Gets the hierarchy details from the user and returns the predicted escalation count. [GET] 
    2. /buildings - Returns the available building list. [GET] 
    3. /floors - Returns the available floors based on the selected building. [GET] 
    4. /departments - Returns the available departments based on the selected building and floor. [GET] 
    5. /zones - Returns the available zones based on the selected building, floor, and department. [GET] 
How to Run :-
    1. Ensure that MySQL has been installed locally and running.
    2. Create a new database named escalation_ml_db. Import the SQL file escalations_ml.sql into the escalation_ml_db database. 
    3. Open the Escalation Count Prediction folder in VS Code. 
    4. Open the backend folder in Terminal. 
    5. cmd - python -m venv venv 
    6. cmd - venv/Scripts/activate 
    7. cmd - pip install -r requirements.txt 
    8. Import the historical escalation database into MySQL. 
    9. Update the MySQL database credentials in the configuration file. 
    10. cmd - python run.py                                                                                       
       {Ensure that Python, pip, and MySQL Server have been installed in your system.} 
4. DPR Analysis :-
Purpose :-
This document defines the software infrastructure requirements for deploying a DPR (Daily Performance Report) Analytics Dashboard that provides real-time insights into Unit, Department, and Checklist performance. The solution is intended for enterprise environments requiring accurate analytics, dashboard visualization, scalability, reliability, and support for concurrent users.
Solution Overview :-
The DPR Analytics Dashboard retrieves Daily Performance Report data from the MySQL database, analyzes Unit, Department, and Checklist performance, calculates completion and lapsed statistics, predicts future performance trends using Machine Learning, and returns the analytics through backend APIs.
API Endpoints :-
    1. /dashboard/main - Returns the overall DPR dashboard summary including KPIs and analytics. [GET] 
    2. /unit/list - Returns all available Units. [GET] 
    3. /unit/dashboard/{unit_name} - Returns dashboard analytics for the selected Unit. [GET] 
    4. /department/list - Returns all available Departments. [GET] 
    5. /department/dashboard/{department_name} - Returns dashboard analytics for the selected Department. [GET] 
    6. /checklist/list - Returns all available Checklists. [GET] 
    7. /checklist/dashboard/{checklist_name} - Returns dashboard analytics for the selected Checklist. [GET] 
    8. /predict/{entity_type}/{entity_name} - Returns Machine Learning-based trend prediction for Unit, Department, or Checklist. [GET] 




How to Run :-
    1. Ensure that MySQL has been installed locally. 
    2. Ensure that the MySQL server is running. 
    3. Create a database named dpr_trend_analysis. 
    4. Import the SQL file dpr_data.sql into the dpr_trend_analysis database. 
    5. Update the MySQL database credentials in the configuration file. 
    6. Open the DPR Analysis folder in VS Code. 
    7. Open the backend folder in Terminal. 
    8. cmd - python -m venv venv 
    9. cmd - venv/Scripts/activate 
    10. cmd - pip install -r requirements.txt 
    11. cmd - python run.py 
    12. Open the application or access the API endpoints. 
    13. Open the frontend files[dpr_frontend,dpr_frontend-prediction] → index.html in chrome/edge
       
{ => Ensure that Python, pip, and MySQL Server have been installed in your system. }











5. Sentiment analysis :-
Purpose :-
The Sentiment Analysis system that classifies patient feedback into Positive, Negative, or Neutral sentiments using a fine-tuned Transformer model. The solution is intended for enterprise environments requiring high classification accuracy, scalability, reliability, and support for concurrent users.
Solution Overview :-
The Sentiment Analysis System receives patient feedback from the user, preprocesses the text, classifies the sentiment using a fine-tuned Transformer model, and returns the sentiment prediction through backend APIs. The system also supports batch prediction for analyzing multiple feedbacks in a single request.
API Endpoints :-
    1. /sentiment/predict - Gets a feedback sentence from the user and returns the predicted sentiment. [POST] 
    2. /sentiment/predict-batch - Gets multiple feedback sentences and returns the predicted sentiment for each feedback. [POST] 
    3. /sentiment/health - Returns the health status of the Sentiment Analysis service. [GET] 
How to Run :-
    1. Open the Sentiment Analysis folder in VS Code. 
    2. Open the backend folder in Terminal. 
    3. cmd - python -m venv venv 
    4. cmd - venv/Scripts/activate 
    5. cmd - pip install -r requirements.txt 
    6. Train the sentiment model using:    
           [can extend the backend/training/sentiment_dataset.csv if needed ]
        	cmd - python backend/training/train.py 
    7. After the model is successfully trained, run   :  cmd -  python run.py
    8. Access the API endpoints through the FastAPI server. 
    9. Open frontend folder → index.html in chrome/edge
{ => Ensure that Python and pip have been installed in your system. }
6.Department & Division Recommendation :-

Purpose :-
The Department & Division Recommendation system that recommends the most appropriate Department and Division for a given checklist question using semantic search with embeddings and a vector database. The solution is intended for enterprise environments requiring high recommendation accuracy, low response time, scalability, reliability, and support for concurrent users instead of manual selection.
Solution Overview :-
The Department & Division Recommendation System receives a checklist question from the user, converts the text into embeddings using a Sentence Transformer model, searches similar questions stored in the Qdrant Vector Database, and returns the most relevant Department and Division through backend APIs. The system also allows administrators to add, update, delete, and manage questions, which are synchronized between MySQL and the vector database.
API Endpoints :-
    1. /questions/predict - Gets a checklist question from the user and returns the recommended Department and Division based on semantic similarity. [POST] 
    2. /questions/add - Adds a new question along with its Department and Division. The data is stored in MySQL and indexed in the Qdrant Vector Database. [POST] 
    3. /questions - Returns all stored questions with their corresponding Department and Division. [GET] 
    4. /questions/{question_id} - Returns the details of a specific question. [GET] 
    5. /questions/{question_id} - Updates an existing question, Department, and Division in both MySQL and Qdrant. [PUT] 
    6. /questions/{question_id} - Deletes a question from MySQL and the Qdrant Vector Database. [DELETE] 
    7. /health - Returns the health status of the application, MySQL database, Qdrant Vector Database, and embedding model. [GET] 


How to Run :-
    1. Ensure that MySQL has been installed locally .
    2. Create a database named department_prediction. 
    3. Add  data in backend/Importing_data/question_DD_data.csv [ clear all & add historical data ]
    4. Ensure that Qdrant has been installed locally and is running. 
    5. Open the Department & Division Recommendation folder in VS Code. 
    6. Open the backend folder in Terminal. 
    7. cmd - python -m venv venv 
    8. cmd - venv/Scripts/activate 
    9. cmd - pip install -r requirements.txt 
    10.  cmd – python -m Importing_data.import_to_mysql
    11. Update the MySQL database credentials in the .env file. 
    12. Update the Qdrant configuration in the .env file if required. 
    13. Run the data import scripts to populate MySQL and Qdrant (if the database is empty). 
    14. cmd - python run.py 
{ => Ensure that Python, pip, MySQL Server, and Qdrant have been installed in your system. }








Complete Zip File Link : https://drive.google.com/drive/folders/1mAXJIM728ESXBhc4OE2tL0VePOadK0If?usp=sharing




Local Installation of Qdrant :-

Link :    https://github.com/qdrant/qdrant/releases?utm_source=chatgpt.com 
download : qdrant-x86_64-pc-windows-msvc.zip [for windows] 
download : qdrant_1.xx.x-1_amd64.deb [for ubuntu]
    1. For Ubuntu :-
        1. sudo dpkg -i qdrant_1.15.5-1_amd64.deb
        2. sudo apt --fix-broken install [ only if dependencies missing]
        3. start : sudo systemctl start qdrant
        4. enable it on boot : sudo systemctl enable qdrant
    2. For Windows :-
        1. open the downloaded file folder in cmd  [/qdrant_service]
        2. qdrant.exe

To see web-ui
    1. Open the qdrant_service folder in vs code
    2. open ‘qdrant_service/qdrant-web-ui-frontend’ folder in Terminal
    3. cmd – npm install 
    4. cmd – npm start
    5. Open : http://localhost:5173/
{ =>   It is to see the locally installed qdrant vector db Web – ui   }


===============================================================
