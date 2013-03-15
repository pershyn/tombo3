Tombo reincarnation developer guide
=======================================================

Goal:
-----

- ship stable, robust, maintainable cross-platform note-taking app that will succeed over Tomboy in linux env and will be used insted of original tombo in Windows env, as successor

Roots:
------

Original Tombo http://tombo.sourceforge.jp/En/ with all features
Improved in:

- encodings
- crossplatform support
- codebase

Prerequisites
-------------

### Git ###
- git SCM - Scott Chacon - Git Internals. Source code control and beyond, "Pro Git"
- githowto
- talk by Scott
- link to workflow
- When you pull from github, you will have only master repo, however, you may be interested at most in what is going on in development branch. So you will need to fetch this one also, in case you are newbie with git, take a look at [this](http://stackoverflow.com/questions/67699/how-do-i-clone-all-remote-branches-with-git) link on how to do that.

### python basics ###
- dive into python 2 and dive into python 3.
- http://docs.python.org


    -- "Core PYTHON Programming by Wesley Chun" - tutorial
    -- "Python in a Nutshell by Alex Martelli." This is an excellent reference book that gives detailed and accurate coverage of the Python language and Python’s standard library.
    -- "Python Cookbook 2nd Edition, edited by Alex Martelli, Anna Martelli Ravenscroft, and David Ascher" - This book provides lots of small  practical functions, classes, snippets, and ideas, and will help broaden any Python programmer’s awareness of what can be done with Python. The recipes are also available online at http://aspn.activestate.com/ASPN/Python/Cookbook.
	
### Qt ###
- Qt basics
- PyQt - "Rapid GUI Programming with Python and Qt. The Definitive Guide to PyQt Programming by Mark Summerfield"
- eclipse & python dev env in eclipse
- Yaml

### Design and Development ###
- Agile/Kanban
- OOP, Patterns, Unit-Tests, etc...

Technology stack:
-----------------

at the moment of writing this guide development is in prototype stage.
Next stack is intended to be used:

- Qt5 as UI library
- python 3.3 to describe logic
(not sure this is best solution so far, because bindings are not verified (pySide, PyQt))
- Currently PyQt (because of python 3 support and maturity), with goal to move to PySide later.

Steps to configure development environment:
---------------------------------------------------------

1. Make sure git is installed and configured
2. Get access to the repo and create local repo
3. Configure development environment

There are several options on what dev environment I plan to try:
1. Eclipse + PyDev
	http://popdevelop.com/2010/04/setting-up-ide-and-creating-a-cross-platform-qt-python-gui-application/

2. Text editor with bunch of tools over it. (console toolchain with plugins)
	trying this now

3. PyCharm + smth...
	not tried yet.
