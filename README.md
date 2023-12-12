# Onlyfiles

This project consists in a shared repository web application with admin and user roles on which only the admins can upload files but everyone authenticated into the repository can download them. 

We use Django as our Web Development Framework, Firebase as our Data Cloud and PostgresSQL as our Database.


## Requirements

The code requires Django libraries and other Python libraries. To install the necessary requirements, use pip with the requirements.txt file. It is strongly recommended to use a virtual environment like venv when installing Python dependencies.

### Python3
`pip install -r requirements.txt`

## Configuration

1. Run the application with the Usage command and create a super user: `python3 manage.py createsuperuser`
2. To make OAuth2.0 using Google as a provider work you should access the admin panel at https://localhost/shoronpo, log in, and create a Social Application record by providing your Google OAuth credentials for the project.
3. Create a .env file containing all the Firebase configuration details.

## Usage

Execute the following command to run a HTTPS development server, given a web certificate :

`python3 manage.py runserver_plus --cert-file webserver.crt.pem --key-file webserver.key.pem localhost:8000`

## Credits

### Contributors

* Marc Alba Cerveró
* Miquel Taberner Mir
* Oriol Miranda Garrido
