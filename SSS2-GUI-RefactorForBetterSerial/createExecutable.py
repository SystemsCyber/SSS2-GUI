from distutils.core import setup
import py2exe
setup(
    windows = [
        {
            "script": "SSS2-Interface.py",
            "icon_resources": [(1, "synerconlogo.ico")]
        }
    ],
)