## ARP scanner

### Install requirement

#### Install nmap on Linux
Make sure you have nmap installed
```bash
sudo apt install nmap
```

#### Install python 2.7 and required packages

It's recommended to create virtual environment

```bash
virtual --python=python2.7 venv
source venv/bin/activate

pip install python-arptable
pip install python-nmap
```

### Usage
- Please make sure to run this script with root
- If you run with virtual environment, please use the absolute path to the python (the path to the executable python in the virtual environment )

sudo <path-to-virtual_env-python> scanner.py [options]

Example:
sudo /home/myusername/miniconda3/envs/py2/bin/python scanner.py