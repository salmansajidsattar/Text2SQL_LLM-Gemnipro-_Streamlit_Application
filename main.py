import streamlit as st
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()
## Configure Genai Key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name MOVIE and has the following columns 
    - Name, Revenue, Year, Universe
    
    For example,
    Example 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM MOVIE ;
    
    Example 2 - Tell me all the movies in Marvel Universe?, 
    the SQL command will be something like this SELECT * FROM MOVIE 
    where Universe="Marvel"; 
    
    also the sql code should not have ``` 
    in beginning or end and sql word in output

    """
]

## Function to retrieve query from the database
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows
    
## Function To Load Google Gemini Model and provide queries as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Streamlit App
st.set_page_config(page_title="English questions to SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

# The content of the Submit button
submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"movie.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)