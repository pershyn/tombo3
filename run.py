import sys
import os


def initialize_path():
    c = os.path.abspath(os.path.curdir)
    tombopkg = os.path.join(c, "..")
    modules_path = os.path.join(tombopkg, "tombo")
    sys.path.append(tombopkg)
    sys.path.append(modules_path)
    print(sys.path)


initialize_path()
import tombo
tombo.main()
