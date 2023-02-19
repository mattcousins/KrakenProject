## Name: Matt Cousins

### How to load up the project:

* Ensure you have Python 3.10+
* Download the tarball file
* cd into KrakenProject
* Install virtualenv with `pip install virtualenv`
* Create an environment `virtualenv venv`
* Activate the environment `source venv/bin/activate`
* Install requirements `pip install pandas`
* Run migrations for database `python manage.py makemigrations`, `python manage.py migrate`
* Create a superuser `python manage.py createsuperuser` for access
* Start the server `python manage.py runserver`
* Run tests with `python manage.py test`
* To exit, run `deactivate`

### How to import and view the data

* Run `python manage.py import_file --file_location` (swapping '--file_location' for the actual location)
* With the serving running, heading to /admin
* Log in
* View the 'Register readings' data.

### Areas for my improvement (with more time):

* Determine what the first and last rows of the file are and process accordingly
* Add further tests
* More validation on the file upload. Highlight problematic rows and alert the user.
* When importing the file, looping over all lines and stumbling across a 26 row isn't very maintainable. It is quite
  fast though for lots of data, I think. Think about a better solution.
* Make datetimes timezone aware

### Structure:

* As there could be outputs per reading (day and night I'm guessing), the actual reading was a separate model with a
  foreign key.
* I built the importer as a Class, which is easier to structure, follow along with and maintain. 