# Software Setup

## Python Setup

1.  Install Python 3 and virtual environment tools
```bash
sudo apt install python3 python3-venv
```

2.  Make a new virtual environment
```bash
python3 -m venv path/to/my/venv
```

3.  Enter the virtual environment
```bash
source path/to/venv/bin/activate
```

4.  Install pip requirements
```bash
# from project root
pip install -r requirements.txt
```

5.  Run the test program
```bash
python3 server/testserver.py

>  Bottle v0.12.16 server starting up (using WSGIRefServer())...
>  Listening on http://localhost:8080/
>  Hit Ctrl-C to quit.
>
```
