# CilantroAudit
Capstone Team C Summer/Fall 2019
---
## Overview

This project will be an electronic auditing system which should simplify the process of creating audits, filling them out and tracking the data they provide in order to better analyze trends and safety risks.

## License

*This project is licensed under the MIT license. Please view LICENSE for more details.*
Copyright (c) 2019 Sean Lesch

## Contributors

*Capstone Team C* - Aaron, Bader, Bradley, Erik, Kegan, Josiah, Sean, Steven

### How to Contribute

This project will be developed using a feature-branch strategy.
1. Create a new branch. Good convention to have the name describe the feature being implemented.
2. Fully implement that feature.
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
  - 'pip3 install' the following:
    - mongoengine
    - pymongo (maybe?)
    - kivy
3. Right-Click the "source" dir and (towards the bottom) click "mark directory as..." > "Sources Root"

#### Python Installation to Work w/ Pycharm
- Download Python 3.7.4 here
  - https://www.python.org/downloads/release/python-374/
    
#### Git Integration w/ Pycharm
- Install GIT here required for use w/ IDE (cross-platform)
  - https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
- OPTIONAL - Install Git Toolbox plugin on IDE's plugin list

#### Flask & Django Integration
- Already is an option on Pycharm when you click on setting up a new project.
- Django project as a template is also provided as an option.

#### Linking IDE to DB (MongoDB)
- Install `Mongo Plugin` in the plugins window on Pycharm
  - This tool allows accessing to Mongo databases and provides CRUD operations on mongo collections.

#### Setting up Built-in Python Dev Tools (unit tests and tkinter)
- `unittest` module should be provided already as a part of the language
  - You can just simply create a unit test by creating a new Python file, and then pick the unit test file option
  - See https://docs.python.org/3/library/unittest.html
  - Example program
```
import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
```
- tkinter module needs to be installed
   - Please install tkinter via `sudo apt-get install python3-tk`
    - See https://tkdocs.com/tutorial/install.html for other platform installations
   - See https://docs.python.org/3/library/tkinter.html
   - Example program
```
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
```
    
#### What is Django, Flask, and Tkinter?
- Django
  - A Python-based free and open-source web framework, which follows the model-template-view architectural pattern.
  - Tutorial: https://docs.djangoproject.com/en/2.2/intro/tutorial01/
- Flask
  - A popular, extensible web microframework for building web applications with Python.
  - Tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
- Tkinter
  - The standard Python interface or module for creating GUIs.


## How to use
