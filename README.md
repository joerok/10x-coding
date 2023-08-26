# 10x Genomics Platform Engineering Technical Coding Prompt

##  Awesome Multi-Container Weather Almanac service (AMCWA)

## Requirements 
 - docker
 - git
 - make tools

### Installation
    # docker compose up --build server -d
    # docker compose up --build test

### Under the Hood

The AMCWA service uses python's Flask web framework to serve API requests.

The test suite is ran by pytest using basic python unittests.

#### Development timeline

Overall the process for creating this application took just under two hours.  

Should the first part of the project been to build out the architecture or build the application?  In this case I chose to build the application.  

_Choosing the API web framework_

At first I thought to use web2py's web framework because it was attractively simple.  However, after installing the module, I discovered it has base requirements of SQLAlchemy, which is just a huge application to install for such a little application.

I dismissed Django, because I would not consider Django a lightweight web framework.

I considered just writing a socket listener, as I would not think this application would require any threading or even forking.  But I doubted that was what 10x was looking for.

So, I went with the tried and true Flask which requires only a couple environment variables to setup, and is very lightweight in the module installation requirements.

_The Coding Exercise_

The coding exercise was simple enough.  Open a file and spit out some JSON based off URL parameters.  Not much to worry about.  I did not worry about security, maintainability, or scalability.  The end code is short (35 lines), and I believe, fairly readable.

The application initialization and single endpoint function are contained in the same file `controller.py`

Running by hand:


```
    $ flask --app controller.py  run
     * Serving Flask app 'controller.py'
     * Debug mode: off
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on http://127.0.0.1:5000
    Press CTRL+C to quit
```
And executing in a separate terminal:

```
    $ curl http://127.0.0.1:5000/query?limit=1
    {"data":[{"date":"2012-01-01","precipitation":"0.0","temp_max":"12.8","temp_min":"5.0","weather":"drizzle","wind":"4.7"}]}
```

Flask Logging:

```
127.0.0.1 - - [25/Aug/2023 16:30:51] "GET /query?limit=1 HTTP/1.1" 200 -
```

Now, I have not added my various typos or debugging.  But suffice to say I didn't write the 35 lines without an error.

Which brings us too ...

_Testing_

Since I was writing the code in Python, unittesting with pytest is my current favorite.

So after coming up with the unit test cases:

```
$ pytest test_unit.py
======================================================================================= test session starts platform linux -- Python 3.10.12, pytest-7.4.0, pluggy-1.2.0
rootdir: /home/joe/projects/10x-coding
collected 5 items                                                                                                                                                                                 

test_unit.py ..... [100%]

======================================================================================== 5 passed in 0.07s 
```
_Docker_

The first part of the bonus part of the project was to create a Dockerfile with access to the container from outside.  Now, I am ashamed to admit, but this caused me some problems.  I could not access my flask application!

After some fun reading online, I discovered that I should force debug mode because I am not actually using a webserver such as nginx or apache.  So, that was just a couple docker `ENV` commands in the `Dockfile`

```
$ docker-compose up --build server -d
[+] Running 1/1
 ✔ Container 10x-weather-app  Recreated                                                                                                                                                      10.4s 
Attaching to 10x-weather-app
10x-weather-app  |  * Serving Flask app 'controller.py'
10x-weather-app  |  * Debug mode: on
10x-weather-app  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
10x-weather-app  |  * Running on http://10x-weather-app:8234
10x-weather-app  | Press CTRL+C to quit
10x-weather-app  |  * Restarting with stat
10x-weather-app  |  * Debugger is active!
10x-weather-app  |  * Debugger PIN: 517-082-042
```

and a quick call to the container:
```
$ curl http://127.0.0.1:8234/query?limit=1
{
  "data": [
    {
      "date": "2012-01-01",
      "precipitation": "0.0",
      "temp_max": "12.8",
      "temp_min": "5.0",
      "weather": "drizzle",
      "wind": "4.7"
    }
  ]
}
```

**BONUS 2**

I am just about to complete the project, and all I have to do is.... create a new container to run tests.  This in itself is pretty easy, just rebuild the last image and give it a new name.  But in my experience this is not what you do!  I decided to use a multistage Dockerfile.  

The `base` stage is mostly to say that the container should have python.

The `test` stage is only what is necessary for running tests.  Turns out this was just two files, a `requirements.tests.txt` to install pytest and requests modules, and the `test_integration.py`.  The test suite is a shameless ripoff from the earlier created `test_unit.py`.  Again, not something you would do in production, as integration tests are meant to determine if the pieces work together, not if the pieces' business logic is correct.

The `app` stage is everything needed to run the application server.

I did run into a problem getting the containers to talk to each other.  But that was resolved in the compose file.

```
$ docker-compose up --build test
[+] Building 1.8s (11/11) FINISHED
...
[+] Running 1/0
 ✔ Container 10x-weather-test  Created                                                                                                                                                        0.0s 
Attaching to 10x-weather-test
10x-weather-test  | ============================= test session starts ==============================
10x-weather-test  | platform linux -- Python 3.10.12, pytest-7.4.0, pluggy-1.2.0 -- /usr/local/bin/python
10x-weather-test  | cachedir: .pytest_cache
10x-weather-test  | rootdir: /app
10x-weather-test  | collecting ... 
10x-weather-test  | collected 5 items
...
10x-weather-test  | ============================== 5 passed in 0.13s ===============================
10x-weather-test exited with code 0
```
