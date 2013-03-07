Legacy Examples
===============

Contains examples showing off OpenGL Legacy (<=2.1) functionality using PyGLy.

Examples have their filename prefixed with'demo_'.

Examples
--------

### Window creation

demo_window_creation.py

Creates a Window.

### Application

application.py

Base application class for most examples.

Creates a Window and implements camera, viewport and rendering code.

### Simple

demo_simple.py

Uses application.py and adds a basic scene graph with 3 tiers of scene nodes all rotating around each other.

### Orthographic

demo_orthographic.py

Same as Simple example, except renders the viewport using an orthographic view matrix.

### Multiple Viewports

demo_multiple_viewports.py

Same as Simple example, except renders a second viewport using the same camera.

### Sorting

demo_sorting.py

Renders a scene of transparent cubes.

The uses PyGLys sorter to avoid transparency rendering issues.

The colour of each cube indicates the order it is rendered in the scene. Colours are from blue to white, with blue rendered first and white last.

