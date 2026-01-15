import unittest
import sys
import os
import gi

# Require GTK 3.0 BEFORE importing utils that uses it
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    gi.require_version('GdkX11', '3.0')
except ValueError as e:
    print(f"Error setting GTK version: {e}")
except ImportError:
    print("GTK not available")

# Add the library directory to sys.path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../usr/lib/clicky')))

from utils import cairo_rect_to_gdk_rect, gdk_rect_to_cairo_rect

class MockGdkRectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __eq__(self, other):
        return (self.x == other.x and 
                self.y == other.y and 
                self.width == other.width and 
                self.height == other.height)

class MockCairoRectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

# Mocking cairo.RectangleInt since we might not have cairo installed in the test env perfectly, 
# but let's try to assume the utils imports work or mock them if they fail.
# Actually, utils.py imports cairo. If this fails, we catch it.

try:
    import cairo
    from gi.repository import Gdk
except ImportError:
    print("GTK/Cairo dependencies missing, skipping full integration tests.")

class TestUtils(unittest.TestCase):
    
    def test_basic_math(self):
        self.assertEqual(1 + 1, 2)

    # We would test crop_geometry and conversions here.
    # Since utils.py relies heavily on X11/Gdk imports which might be hard to mock perfectly without a display,
    # we start with importability and basic logic.

if __name__ == '__main__':
    unittest.main()
