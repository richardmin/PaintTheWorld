Note: to work on the Python server, you should run the following commands to set
up your virtual environments.
This ensures compatability of code.

For \*NIX Systems:
```bash
$ pyvenv venv
$ . venv/bin/activate
$ pip install -r requirements.txt  # install python dependencies inside venv
```

To launch the server, make sure you're in your virtual environment and run:
```bash
$ ./launch.sh
```

If you've installed a new python package inside your virtual environment, you
should update the requirements file:
```bash
$ pip freeze > requirements.txt
```

To return to the real world, run:
```bash
$ deactivate
```
