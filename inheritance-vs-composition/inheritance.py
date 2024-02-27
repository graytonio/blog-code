from abc import abstractmethod
from typing import Tuple
import pathlib

# Base class with abstract methods for saving and loading
class Image:
    def __init__(self, width: int = 0, height: int = 0):
        self.width = width
        self.height = height
        self.setSize(width, height)
    
    def setSize(self, width: int, height: int):
        self.pixels = [[(0, 0, 0) for x in range(width)] for y in range(height)]
        
    def getPixel(self, x: int, y: int) -> Tuple[int, int, int]:
        return self.pixels[x][y]
    
    def setPixel(self, x: int, y: int, rgb: Tuple[int, int, int]):
        self.pixels[x][y] = rgb
    
    def resizeImage(self, scale: float):
        newHeight = int(self.height * scale)
        newWidth = int(self.width * scale)
        newPixels = [[(0, 0, 0) for x in range(newWidth)] for y in range(newHeight)]
        
        for row in range(newHeight):
            for column in range(newWidth):
                origin = self.getPixel(int(column/scale), int(row/scale))
                newPixels[row][column] = origin
    
        self.height = newHeight
        self.width = newWidth
        self.pixels = newPixels
        

    def flipHorizontal(self):
        for row in range(self.height):
            for column in range(self.width/2):
                inverseColumn = self.width - 1 - column
                
                temp = self.pixels[row][column]
                self.pixels[row][column] = self.pixels[row][inverseColumn]
                self.pixels[row][inverseColumn] = temp
    
    def flipVertical(self):
        for row in range(self.height/2):
            for column in range(self.height):
                inverseRow = self.height - 1 - row
                
                temp = self.pixels[row][column]
                self.pixels[row][column] = self.pixels[inverseRow][column]
                self.pixels[inverseRow][column] = temp
    
    @abstractmethod()
    def save(self):
        pass
    
    @abstractmethod()
    def load(self):
        pass

# Child classes that implement the abstract classes of the parent
class JPGImage(Image):
    def __init__(self, path: str):
        self.path = path
        
    def save(self):
        saveImageAsJPG(self.pixels, self.path)
    
    def load(self):
        loadJPG(self.pixels, self.path)
        
class PNGImage(Image):
    def __init__(self, path: str):
        self.path = path
        
    def save(self):
        saveImageAsPNG(self.pixels, self.path)
    
    def load(self):
        loadPNG(self.pixels, self.path)

class BMPImage(Image):
    def __init__(self, path: str):
        self.path = path
        
    def save(self):
        saveImageAsBMP(self.pixels, self.path)
    
    def load(self):
        loadBMP(self.pixels, self.path)

# Out drawable image that breaks out parent classes assumption. This is one way to handle the changes but it breaks 
class DrawableImage(Image):
    def drawLine(self, sX: int, sY: int, eX: int, eY: int):
        # Implementation
        pass
    
    def drawPoint(self, x, y):
        # Implementation
        pass
    
    def save(self):
        raise Exception("Not implemented")
    
    def load(self):
        raise Exception("Not implemented")

# Main application class that uses out image classes
class MyImageAppUI:
    
    image: Image
    
    def __init__(self, path: str):
        match pathlib.Path(path).suffix:
            case ".jpg":
                self.image = JPGImage(path)    
            case ".png":
                self.image = PNGImage(path)
            case ".bmp":
                self.image = BMPImage(path)
        
        self.image.load()
        
    def onSaveClicked(self):
        self.image.save()
        
    def onFlipClicked(self, horizontal: bool):
        if horizontal:
            self.image.flipHorizontal()
        else:
            self.image.flipVertical()
    
    # How would could you implement this function to allow a line tool now? How would you save the result?
    def onLineTool(self, sX: int, sY: int, eX: int, eY: int):
        pass