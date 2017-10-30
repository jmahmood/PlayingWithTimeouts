A way to test GUnicorn timeout behavior.

To run, type in `bash start.sh`.  It is assumed that the version of python you are running has the appropriate libraries already installed. (`pip install -r requirements.txt`)

This starts a foreground and background version of the server.

The servers themselves have commands that return 1, 10, 20 and 30 second requests.  

The experiment starts a gunicorn server that is attached to a basic tornado application.  


The urls you are interested are all GET urls.

```
(local url)/1 # 1 second wait time 
(local url)/10 # 10 second wait time
(local url)/20 # 20 second wait time
(local url)/30 # 30 second wait time
```