
# SFT

Secure File Transfer application that can be used by different members within a network to share files efficiently and securely.

## Initial setup
- Make sure Python is installed in the system and then install all the dependencies for the project mentioned in "requirements.txt" file by typing the following command - 

```shell
pip install -r requirements.txt
```

- Make a ".env" file which contains the environment variables such as MONGO_URI and others.
NOTE: Don't forget to use the MONGO_URI in order to connect to database.
- Create two directories "received/" and "uploads/" in the root directory of the app, and they will be used by the app to save the files.

## How to run ?

Now, once all the dependecies are installed in the system, navigate to the project directory and run the project using following command in the terminal -

```shell
python index.py
```
The app will run on the local server at the address "localhost:5000". Open this link in any web browser and it's ready to use.