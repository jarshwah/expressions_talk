# Expressions

Examples used in my talk.

## Getting Started

The examples within are designed to show the differences between Django 1.7 and Django 1.8. 
It's necessary to leverage virtualenv to easily switch between the examples. These are roughly 
the steps I used to get up and running (on OSX). This can *only* be run on Python 3, and preferably
with Python 3.4.

We'll be using homebrew, pip3 (which comes with python3), virtualenv, and virtualenvwrapper.

```
git git@github.com:jarshwah/expressions_talk.git
cd expressions_talk
brew install python3 pyenv
pip3 install virtualenv virtualenvwrapper  # unless you already have both installed
pyenv install 3.4.3
mkvirtualenv -p `pyenv which python` exp1.7
mkvirtualenv -p `pyenv which python` exp1.8
workon exp1.7
pip install -r requirements/1.7.txt
deactivate
workon exp1.8
pip install -r requirements/1.8.txt
cd expressions
./manage.py migrate
```

You're now ready to run some of the examples.

## Running examples:

```
workon exp1.8
cd expressions_talk/expressions/
./manage.py shell_plus
>>> from cdr.examples import *
>>> qs = conditional_annotation()
>>> print(qs.query)
# prints the query..
>>> for agent in qs:
...    print("{}\t{}\t{}".format(agent.name, agent.count_2014, agent.count_2015))

```
