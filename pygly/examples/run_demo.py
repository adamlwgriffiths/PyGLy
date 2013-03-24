import argparse
import importlib

profiles = {
    "core":     True,
    "legacy":   False,
    }
applications = {
    "pyglet":   "application_pyglet",
    "pyglfw":   "application_pyglfw",
    "glut":     "application_glut",
    }
demos = {
    "basic":        "scene_basic",
    "texturing":    "scene_texture",
    "scene_graph":  "scene_scene_graph",
    "orthographic":   "scene_orthographic",
    "multiple_viewports":   "scene_multiple_viewports",
    "sorting":      "scene_sorting",
    }

def parse_arguments():
    parser = argparse.ArgumentParser(
        description = "PyGLy demo application"
        )
    parser.add_argument(
        "-g", "--opengl_profile",
        choices = profiles.keys(),
        default = "core",
        help = "The OpenGL profile to use. (default: core)",
        )
    parser.add_argument(
        "-p", "--platform",
        choices = applications.keys(),
        default = "pyglet",
        help = "The windowing platform to use. (default: pyglet)",
        )
    parser.add_argument(
        "-d", "--demo",
        choices = demos.keys(),
        default = "basic",
        help = "The demo to run. (default: basic)",
        )
    return parser.parse_args()

def run_demo( args ):
    global profiles, applications, demos

    print "Windowing system:\t", args.platform
    print "OpenGL profile:\t", args.opengl_profile
    print "Scene:\t", args.demo

    is_core = profiles[ args.opengl_profile ]

    scene_module = __import__( demos[ args.demo ], fromlist=[""] )
    scene = scene_module.Scene( is_core )

    app_module = __import__( applications[ args.platform ], fromlist=[""] )
    application = app_module.Application( scene )

    application.run()


if __name__ == "__main__":
    args = parse_arguments()
    run_demo( args )
