# CilantroAudit
Capstone Team C Summer/Fall 2019
---
## Overview

This project will be an electronic auditing system which should simplify the process of creating audits, filling them out and tracking the data they provide in order to better analyze trends and safety risks.

## License

*This project is licensed under the MIT license. Please view LICENSE for more details.*
Copyright (c) 2019 Sean Lesch

## Contributors

(Summer/Fall 2019) - Team C
- Aaron
- Bader Alshaya
- Bradley
- Erik
- Kegan
- Josiah
- Sean
- Steven

### How to Contribute

This project will be developed using a feature-branch strategy.
1. Create a new branch. Good convention to have the name describe the feature being implemented.
2. Fully implement that feature with necessary tests.
3. Ensure there are no bugs that can break the master branch/release build.
4. Merge into master using a pull request.

## Installation / Setup

- Register for the JetBrains Student Pack (use your PSU email)
  - https://www.jetbrains.com/shop/eform/students
- Install the IDE (Professional Version) for development environment (click the right one for your platform)
  - https://www.jetbrains.com/pycharm/download
  - Make sure to go to `licenses` and login with your student pack account

### Quick Dev-Environment Setup
1. Create New Project in Pycharm.
2. In Pycharm's Terminal: 
  - 'git clone' this repo.
  - `cd "your-repo-name"`
  - Create a virtual environment following this tutorial for your platform: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
    - `pip3 install venv` to install virtual environment
    - `python3 -m venv env` to create a virtual environment
  - `source env/bin/activate` to get into virtual environment
  - `pip3 install -r requirements.txt` to install the requirements such as kivy and mongoengine for the venv
3. Right-Click the "source" dir and (towards the bottom) click "mark directory as..." > "Sources Root"
4. Make sure your virtualenv is correctly configured in PyCharm following the steps here: https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html

#### Python Installation to Work w/ Pycharm
- Download Python 3.7.4 here
  - https://www.python.org/downloads/release/python-374/
    
#### Git Integration w/ Pycharm
- Install GIT here required for use w/ IDE (cross-platform)
  - https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
- OPTIONAL - Install Git Toolbox plugin on IDE's plugin list

#### Setting up Unit Tests
- `unittest` module should be provided already as a part of the language
  - You can just simply create a unit test by creating a new Python file, and then pick the unit test file option
  - See https://docs.python.org/3/library/unittest.html
    
#### What is Kivy?
- Kivy
  - Kivy is a free and open source Python library for developing mobile apps and other multitouch application software with a natural user interface.
  - Guide: https://kivy.org/doc/stable/guide/basic.html
  
#### Development Information
- Style guide
  - https://www.python.org/dev/peps/pep-0008/

## (TBA) Program Usage