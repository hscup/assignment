# Rush hour

## Installation

Use python 3.6.1 or greater, because it is much friendlier and additionally runs faster.
The best way to install pygame is with the pip tool (which is what python uses to install packages)

It's recommend to run the program in virtual environment

### Create virtual environment
#### Windows

```bash
    virtualenv --python=python3.6 venv
    venv\Scripts\activate
    pip install -r requirements.txt

    # Run it
    python rushhour_gui.py game0.txt
```

#### Mac, Linux

```bash
    virtualenv --python=python3.6 venv
    source venv/bin/activate
    pip install -r requirements.txt

    # Run it
    python rushhour_gui.py game0.txt
```