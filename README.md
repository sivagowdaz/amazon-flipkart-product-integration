# Amazon-Flipkart Integration

### This is a web application that integrates amazon and Flipkart, when a user searches for a particular product it displays all the searchappropriate results from amazon and Flipkart in two columns with all product details. Performs automatic login activities and product selection activities. Automation bots are created with an Object-Oriented approach

## Prerequisites

1. python must be installed

## Project Setup

1. Install all the dependencies listed in the requirements.txt file(It is recommended to install dependencies inside the virtual environment, instead of installing globally.)
2. Make migrations by running bellow commands

```
python manage.py migrate
python manage.py makemigrations
```

3. Run bellow command to run the server

```
python manage.py runserver
```

## Note

### chrome webdriver is included in the repository path adpmini\adpmini\bot\scrapping\chromedriver.exe

### change the driver path according to your system path at C:\Users\shivaprasad\Desktop\needed\adpmini\adpmini\bot\scrapping\constants.py
