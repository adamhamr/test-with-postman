# test-with-postman
A project that contains several bugs. A beginner tester can make use of it to test out the project and report the bugs.

## Step-by-Step Guide: How to Test the REST API Using Postman (Beginner-Friendly)

### 1. Install Python

Go to the official Python website: [](https://www.python.org/downloads/)

Download Python installer.

Run the installer and:

-	Check the box: "Add Python to PATH"
-	Click "Customize installation"
-	Ensure the following options are selected: pip, venv, and "Install for all users"

Finish the installation

### 2. Open the Project Folder

Open a terminal (Command Prompt or PowerShell) and run:
```
cd rest-api-test
```

This enters a new folder for your project.

### 3. Create a Virtual Environment

A virtual environment allows you to isolate the dependencies for this project:

`python -m venv venv`

To activate it:

- 	On Windows:
`venv\Scripts\activate`
- 	On macOS/Linux:
`source venv/bin/activate`

You should now see something like `(venv)` at the beginning of your terminal prompt.

### 4. Install Project Dependencies

Install the required Python packages:

`pip install fastapi uvicorn transformers`

### 5. Check the API Code

Make sure, there is main.py file inside the rest-api-test folder.

### 6. Run the API Server

Start the server by running:

`uvicorn main:app –reload`

What this command does:

- 	Starts the FastAPI application (main:app)
- 	Enables automatic reloading (--reload) when you make changes to the code

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

If you see both lines, especially `Application startup complete`, the server is running correctly.

### 7. Install Postman

Go to [](https://www.postman.com/downloads/)

Download and install the latest version for your operating system.

### 8. Open Postman after installation.

Send a Request Using Postman

Open Postman

Click 'New' > 'HTTP Request'

In the request window:

- Set the method to POST
- Set the URL to: http://127.0.0.1:8000/suggest
- Go to the Body tab, select raw, and set the format to JSON
- Paste this into the body:

```
{
  "name": "Gabriella",
  "age": 30,
  "favorite_color": "red"
}
```

Click “Send”

You should receive a JSON response similar to:

```
{
  "suggestion": "Hi Gabriella! Hope you're balancing work and fun! Also, red is a beautiful color!",
  "token_count": 18
}

```

### 9. Check the Log File

While the server is running, logs are written to a file named suggestion_api.log.

To view the logs:

`notepad suggestion_api.log`

Look for details such as incoming requests, responses, and any intentional or unexpected errors.

### 10. Stop the Server

When you're done, go back to the terminal running Uvicorn and press:

`CTRL + C`

This will stop the server.
