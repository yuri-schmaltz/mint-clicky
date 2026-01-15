import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import cairo
import math

class CanvasWidget(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.BUTTON_RELEASE_MASK |
                        Gdk.EventMask.POINTER_MOTION_MASK)
        self.connect("draw", self.on_draw)
        self.connect("button-press-event", self.on_button_press)
        self.connect("motion-notify-event", self.on_motion_notify)
        self.connect("button-release-event", self.on_button_release)
        self.connect("size-allocate", self.on_size_allocate)

        self.surface = None
        self.image_surface = None
        self.original_pixbuf = None
        
        # Tools: 'pen', 'highlighter', 'eraser'
        self.current_tool = 'pen' 
        self.is_drawing = False
        self.last_x = 0
        self.last_y = 0

    def set_pixbuf(self, pixbuf):
        self.original_pixbuf = pixbuf
        self.queue_draw()

    def on_size_allocate(self, widget, allocation):
        # When resized, we might arguably want to keep the surface or resize it.
        # For simplicity in a screenshot tool, the canvas size usually matches image size
        # or we accept the allocation.
        # Let's create a surface that matches the allocation if it doesn't exist
        if self.surface is None or self.surface.get_width() != allocation.width or self.surface.get_height() != allocation.height:
             self.create_surface(allocation.width, allocation.height)
             self.redraw_canvas()

    def create_surface(self, width, height):
        self.surface = self.get_window().create_similar_surface(
            cairo.CONTENT_COLOR_ALPHA, width, height)
        
        # Clear surface
        cr = cairo.Context(self.surface)
        cr.set_source_rgba(0.2, 0.2, 0.2, 1) # Dark gray background
        cr.paint()

    def redraw_canvas(self):
        if self.surface is None: 
            return
            
        cr = cairo.Context(self.surface)
        
        # 1. Clear text/drawings
        cr.set_source_rgba(0.2, 0.2, 0.2, 1)
        cr.paint()
        
        # 2. Draw Image
        if self.original_pixbuf:
            Gdk.cairo_set_source_pixbuf(cr, self.original_pixbuf, 0, 0)
            cr.paint()
            
        # If we had a history of paths, we would redraw them here.
        # For this simple "paint on surface" implementation, we just clear and paste image.
        # A more complex one would keep strokes in a list. 
        # For MVP: drawings are destructive on the surface? 
        # No, let's keep a separate "drawing layer" if possible, or just paint fast.
        # Decision: "Paint on top" architecture. Resetting pixbuf clears drawings.
        pass

    def on_draw(self, widget, cr):
        if self.surface:
            cr.set_source_surface(self.surface, 0, 0)
            cr.paint()
        return False

    def on_button_press(self, widget, event):
        if event.button == 1 and self.surface:
            self.is_drawing = True
            self.last_x = event.x
            self.last_y = event.y
        return True

    def on_motion_notify(self, widget, event):
        if self.is_drawing and self.surface:
            self.draw_stroke(event.x, event.y)
            self.last_x = event.x
            self.last_y = event.y
        return True

    def on_button_release(self, widget, event):
        if event.button == 1 and self.is_drawing:
            self.is_drawing = False
            self.draw_stroke(event.x, event.y)
        return True

    def draw_stroke(self, x, y):
        cr = cairo.Context(self.surface)
        
        if self.current_tool == 'pen':
            cr.set_source_rgba(1, 0, 0, 1) # Red
            cr.set_line_width(3)
        elif self.current_tool == 'highlighter':
            cr.set_source_rgba(1, 1, 0, 0.4) # Yellow transparent
            cr.set_line_width(20)
        elif self.current_tool == 'eraser':
            # This is tricky with a single layer. 
            # Ideally we'd just repaint the image region?
            # For MVP, eraser might just paint white or "undo"?
            # Let's leave eraser as "Paint transparent" which acts as erasing on a layer,
            # but on a single composite, it reveals black.
            # Better: Repaint original pixbuf content at that location? Too complex for MVP.
            # Let's skip Eraser for MVP or make it simple "Blue Pen" for now as 'Pen 2'.
            cr.set_source_rgba(0, 0, 1, 1) # Blue
            cr.set_line_width(3)

        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        
        cr.move_to(self.last_x, self.last_y)
        cr.line_to(x, y)
        cr.stroke()
        
        self.queue_draw()

    def get_result_pixbuf(self):
        # Convert surface to pixbuf
        if self.surface:
            width = self.surface.get_width()
            height = self.surface.get_height()
            return Gdk.pixbuf_get_from_surface(self.surface, 0, 0, width, height)
        return self.original_pixbuf
