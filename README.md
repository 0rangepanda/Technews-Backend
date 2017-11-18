Note:
  If install any new packages
  -> In folder data, run: pip freeze > requirements.txt

To set up project:
  create python virtual environment:
    virtualenv project
    source bin/activate
  get source code from githab:
    git clone https://github.com/0rangepanda/Technews-Backend.git
  Install python packages:
    pip install -r requirements.txt
  Run server:
    python server.py

Replacebale files:
  in data folder:
    stopword - the stop word list file, which will be used by rake
    techlist - the tech word list file, which will be used to filter the result of mapreduce job
    My ProjectXXX.json - authentification file for google big query project
