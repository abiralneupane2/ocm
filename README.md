# ocm


# Check if python is installed.
$ python -V

# Install python if not found.

# Install virtual environment.
$ pip install virtualenv

# Create virtual environment
$ python -m venv /path-to-new-virtualenvironment

# Activate virtual environment
$ /path-to-new-virtualenvironment/environment/Scripts/activate

# Install necessary python packages
$ pip install django django-extensions django-crispy-forms xhtml2pdf django-online-users

<------One time setup upto here--------->

# To start application

# Activate virtual environment
$ /path-to-new-virtualenvironment/environment/Scripts/activate

# cd into project folder
$ ./manage.py runserver


