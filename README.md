
## Contents

- [About](#about)
- [Run application](#run_application)
- [Usage](#usage)
- [Run application using Docker](#run_application_using_docker)
- [Run tests](#run_tests)


## About

Dr.Office is a MVC Flask appliaction, which helps doctor to store info about patient's visit.

## Run application

1. From root folder create virtual environment (if you run the app for the first time)

```
python -m venv venv
```

2. Run virtual environment

```
cd .\venv\Scripts\
.\Activate.ps1
```

3. Install dependencies (if you run the app for the first time)

```
pip install -r requirements.txt
```

4. Create **.env** file.
Copy the content from **.env.example** into the **.env** file

5. Run the application

```
flask --app app run
```

NOTE: to make sure that html renders well, check ***.css*** and ***.js*** line endings, it should be **LF** instead of **CRLF**

## Usage

Copy and paste the link to browser.

```
http://localhost:5000/login
```
Register your user and you will be redirected on the main page

## Run application using Docker

From root folder execute **docker-compose up -d** (***.env*** file should be already created).

## Run tests
<ins>Run unit tests:</ins> execute ***coverage run -m --source=. pytest --ignore=tests/e2e***<br />
<ins>See test's report in console:</ins> execute ***coverage report***<br />
<ins>See test's report in browser:</ins> execute ***coverage html***. Then go to ***htmlcov*** folder and open ***index.html*** in browser.

<ins>Run e2e tests:</ins> execute **docker-compose up -d** (it will start up the ***dr.office-e2e*** container)<br />
If you haven't install Playwright drivers yet, then execute **playwright install**<br />
Execute **pytest tests/e2e**, it will launch the e2e tests through the ***dr.office-e2e*** container
