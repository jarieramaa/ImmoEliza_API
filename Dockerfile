#DOCKER FILE CREATION

# Linux python 3.8
FROM python:3.8

# Create a folder that the root of the system called "app"
RUN mkdir /app

#Copy all the files frm the current folder
COPY . /app

# Define the working directory
WORKDIR /app

# Delete the virual env
RUN rm -rf venv

#Install depencies
RUN pip install -r requirements.txt

#Run the app
CMD python app.py