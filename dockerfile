# Python 3.8 image
FROM python:3.8

# Create app -folder
RUN mkdir /app

# Copy everything to the app folder
COPY . /app

# Define working directory
WORKDIR /app

# Delete the virtual env
RUN rm -rf immo_env

# Install dependnecies
RUN pip install -r requirements.txt

# Run the app
CMD python app.py