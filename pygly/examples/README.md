Examples
========

This directory contains all of the PyGLy examples.

Examples are run using the 'run_demo' python script.

The 'run_demo' script takes a number of command-line arguments in the following format:
```
python run_demo.py -p <platform> -g <profile> -d <demo>
```

Arguments
---------

Platform options includes:
   * pyglet
   * pyglfw
   * glut

Profile options include:
   * core
   * legacy

Demo options include:
   * basic
   * texturing
   * scene_graph


Example commands
----------------

```
python run_demo.py -p pyglet -g core -d simple
python run_demo.py -p pyglet -g legacy -d simple
python run_demo.py -p pyglfw -g core -d simple
python run_demo.py -p pyglfw -g legacy -d simple
```