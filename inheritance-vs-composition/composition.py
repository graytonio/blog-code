from abc import ABC, abstractmethod
from typing import Tuple
import pathlib

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
  
class FileBasedInterface(ABC):
    @abstractmethod()
    def save(self, img: Image):
        pass
    
    @abstractmethod()
    def load(self, img: Image):
        pass
                
class JPGImage(FileBasedInterface):
    def __init__(self, path: str):
        self.path = path
        
    def save(self, img: Image):
        saveImageAsJPG(self.image, self.path)
        
    def load(self, img: Image):
        loadJPG(self.image, self.path)
        
class PNGImage(FileBasedInterface):
    def __init__(self, path: str):
        self.path = path
        
    def save(self, img: Image):
        saveImageAsPNG(self.image, self.path)
        
    def load(self, img: Image):
        loadPNG(self.image, self.path)
        
class BMPImage(FileBasedInterface):
    def __init__(self, path: str):
        self.path = path
        
    def save(self, img: Image):
        saveImageAsBMP(self.image, self.path)
        
    def load(self, img: Image):
        loadBMP(self.image, self.path)
        
class DrawableImage():
    def __init__(self, img: Image):
        self.img = img
    
    def drawLine(self, sX: int, sY: int, eX: int, eY: int):
        # Implementation
        pass
    
    def drawPoint(self, x, y):
        # Implementation
        pass

class MyImageAppUI:
    image: Image
    
    def __init__(self, file: FileBasedInterface):
        self.file = file
        self.file.load(self.image)
    

    def onSaveClicked(self):
        self.file.save(self.image)
        
    def onFlipClicked(self, horizontal: bool):
        if horizontal:
            self.image.flipHorizontal()
        else:
            self.image.flipVertical()
            
    # Since our components are composable we can orchestrate them together with just the components we need to accomplish our goal
    def onLineTool(self, sX: int, sY: int, eX: int, eY: int):
        drawable = DrawableImage(self.image)
        drawable.drawLine(sX, sY, eX, eY)