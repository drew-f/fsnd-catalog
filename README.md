# Book Catalog

## About
This is a python application written using Flask and SQLAlchemy that stores
details of books in various categories. It was created as Project 3 of the
Udacity Full Stack Web Development Nanodegree program.

## Requirements
- Python 2.7.x
- flask
- SQLAlchemy

## Usage
- Clone the vagrant virtual machine from:
https://github.com/udacity/fullstack-nanodegree-vm
- Unzip project3.zip into the vagrant folder
- Set up the database by running the dbsetup.py file:
```python dbsetup.py```
- If desired, import sample data (taken from Amazon.com) by running
sample_data_import.py:
```python sample_data_import.py```
- Run the application:
```python app.py```
- Access the application on http://localhost:5000

## Marker Notes
- Any logged in user can change the name of a category, add a new category,
add books, and delete an empty category
- Individual books can only be edited or deleted by the user that created them
