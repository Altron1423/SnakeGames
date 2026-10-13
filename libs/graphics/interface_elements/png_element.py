from libs.graphics.interface_elements.buttons_element import Button
from libs.graphics.polygons import Polygon
from libs.loaders.image_loader import image_loader


class PngElement(Button):
    """A button element that displays a PNG image.

    Attributes:
        png_polygon (Polygon | None): The polygon representing the image.
    """
    png_polygon: Polygon | None

    def set_png(self, png):
        """Sets the PNG image for the element.

        Args:
            png (str | list[str]): The path to the image(s).
        """
        if type(png) == str:
            self.png_polygon.set_png(image_loader.get(png))
        elif type(png) == list:
            i = i2 = 0
            while i < len(png) and i2 < len(self.polygons.polygons):
                if self.polygons.polygons[i2].type == 3:
                    self.polygons.polygons[i2].set_png(image_loader.get(png[i]))
                    i += 1
                i2 += 1
        self.polygons._redraw()
