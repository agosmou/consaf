# [Con]struction [Saf]ety
This is a construction safety tooling web app aimed at remote monitoring for your construction site

## Screenshots
![image](https://github.com/agosmou/consaf/assets/73868258/6e4c3d9d-a938-4d9a-bdfb-d611cad6b9b0)
The above image shows the output from the webapp.

![image](https://github.com/agosmou/consaf/assets/73868258/3a8bc89d-3117-4f43-b37f-84fe61ed1e5a)
The above image shows the randomly generated stock photo that was analyzed with the object detection model

![image](https://github.com/agosmou/consaf/assets/73868258/330838cb-f93b-4fc4-8e8a-f63203dc017b)
The above image shows the location for the returned coordinates which matches the value for the `"location"` key

![image](https://github.com/agosmou/consaf/assets/73868258/643e35b7-ef2c-485e-bb36-56d8c993cd5c)
The above image shows the weather for the given location which matches the values for `"apparent_temperature_max"` and `apparent_temperature_min`

## The Future of [Con][Saf]
[ConSaf 1.0.0 - Major Release]'
Real time site monitoring via camera on-site
- Inputs 
    - constant live video from camera with wifi service to use IP for weather information
- Outputs
    - safety object detection
    - real time weather monitoring 

[ConSaf 0.1.0 - MVP - alpha]
static site to provide insights based on user inputs
- Inputs
    - Image URL
    - User inputted location

- Outputs
    - object detection
    - weather information



## Tech Stack

Frontend  
- HTML, CSS, JS
- Bootstrap 5

Backend and significant pythong packages  
- Flask
- yolov5
- gunicorn as production webserver on Linux

Database
- 

Deployment
- 
- 


## API

### Set up the API
shortcut to set up from the server directory  
*Note that we will use Python 3.10 because we will be using yolov5*  
`$ py -3.10 -m venv .venv && source .venv/Scripts/activate && pip install -r requirements.txt`

<em>If you need to download python 10 then follow the link below and download the file. MAs you go through the Python 3.10 download wizard, ake sure you check the box that adds python to the PATH variable</em>  

[download here](https://www.python.org/ftp/python/3.10.11/) and select this executable file:   

`python-3.10.11-amd64.exe` 05-Apr-2023 01:09 29037240


<strong>Ensure you select the correct python interprettor</strong><br>
Open up the VSCode command pallete  
 `CTRL + shift + P` and type in the search bar "Select Python Interprettor" -> "Select Path" and copy the path from :
```
backend/              
├── api/
│   ├── .venv/       
│     ├── Scripts/   
│        ├── python.exe # copy the path to this  
```

### Run the server in development environment from the api directory
`$ flask --app main run --debug`


### Run the server using Docker
First, open up docker desktop on your machine and run these commands from the server directory

<strong>build the image</strong><br>
`$ docker build -t image_consaf_api . # note the trailing "."`

<strong>spin up the container</strong><br>
`$ docker run -d --name consaf_api_container -p 80:80 image_consaf_api`

Your directory should look this, so all your calls should be from the server directory and NOT the api directory
`myName@LAPTOP MINGW64 /myMachinePath/consaf/backend`
```markdown
.
├── api
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt

```
Your dockerfile should look like this:
```dockerfile
FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./api /code/api

CMD ["gunicorn", "api.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]

```

If you make changes to the code, you'll have to recreate the image and spin back up. 

To simply start and stop the existing container,  
`$ docker start consaf_api_container`  
`$ docker stop consaf_api_container`

## Client


## Computer Vision

the object detection model uses yolov5 - [model source](https://huggingface.co/keremberke/yolov5s-construction-safety)
[dataset](https://huggingface.co/datasets/keremberke/construction-safety-object-detection)

## Testing
For testing, make sure you create a new virtual environment and install the requirements_test.txt file

run `pytest tests` from the "backend" directory  
`myName@LAPTOP MINGW64 /myMachinePath/consaf/backend $ pytest tests`

## Debugging

### API Start Up
If you get an error regarding the import of packages when trying to run your API:
- first, make sure you're using absolute paths for importing your packages

- If the errors look like this:
`ModuleNotFoundError: No module named 'api'`  
or  
`ImportError: attempted relative import with no known parent package`  

You will need to edit the `PYTHONPATH` variable. You can do this two different ways (I recommend the 1st as this is what I did and it worked for me). Make sure you have your virtualenvironment (.venv) running:   
1. You'll be adding a file to the `.venv` directory. Navigate to the folder shown below and add a file called `consaf.pth`    
```
server/
├─ .venv/
│  ├─ Lib/
│  │  ├─ site-packages/
│  │     ├─ consaf.pth
```
In this file, add this to it:`C:\yourComputerPath\consaf\backend`  
Done!

2. run this command: `export PYTHONPATH=$PYTHONPATH:/path/to/your/project`



## TO-DO - 0.0.1
FrontEnd
- [ ] Set up Home page with Login
- [ ] guest login dashboard for demos

Backend
- [X] set up unit tests
- [X] Set up computer vision model endpoint
- [X] Add weather third party API
- [X] Add Unsplash random image generator third party API
- [X] Add reverse GEoCode from Unsplash image third party API
- [ ] Add cache strategy for location inputs when users search for weather updates
- [ ] Add rate limiting
- [ ] Set up JWT authentication
- [ ] Set Up Oauth for sign ups/login and sender for SMTP email communication but only if a user has been authenticated and has a valid JWT
- [ ] add OpenAI to report back on PPE and weather findings
- [ ] add postgreSQL db to save users along with their queried images and chatGPT responses

DevOps
- [ ] purchase domain on AWS (SSL/TLS)
- [ ] Containerize server with Docker
- [ ] deploy server using docker on AWS EC2 and db on RDS. S3 bucket to host static files



## TO-DO - 0.0.2
Features
- [ ] add functionality to upload an image and have it display on the browser


FrontEnd
- [ ] TypeScript
- [ ] Sign Up with google OAuth

Backend
- [ ] use sender for SMTP email verification
- [ ] cloudflare turnstile/recaptchav3 middleware for account creation
- [ ] sign up with google

DevOps
- [ ] fully automate deployments via github actions from commits
- [ ] Load Test with Grafana K6
- [ ] Error logging with Sentry SDK

## Third Party API's
- [Geocode Maps](https://geocode.maps.co/#:~:text=This%20geocoding%20API%20is%20provided,uses%20the%20Google%20Maps%20API.) for finding locations from coordinates

- [Open-Meteo](https://open-meteo.com/en/docs) for weather data from coordinates

- [Unsplash](https://unsplash.com/documentation)


## Testing
Navigate to the `backend/api directory`. From here, start up a new virtual environmnet for testing and install all the testing dependencies. Then run `pytest tests`

