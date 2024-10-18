name = "screenSpacer"

version = "0.1.0"

authors = [
    "Beau C. Pratt",
    "Jeremy Andriambolisoa",
]

description = \
    """
    A tool for fixing the visual flicker created when a character 
    is animated in stepped mode with a moving camera.
    """

requires = [
    "python-3+",
    "maya-2025+"
]

uuid = "ThePrattBros.screenSpacer"

build_command = 'python {root}/build.py {install}'

def commands():
    env.PYTHONPATH.append("{root}/python")
