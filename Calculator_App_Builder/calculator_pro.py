import os
import runpy
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

runpy.run_module("time_calculator", run_name="__main__")
