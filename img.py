"""
Just testing with spwn
"""

# Modules
from sys import argv
import colorama
from PIL import Image
from os import getcwd
# Class
class PyImg2GD:
    def __init__(self, imgPath: str):
        '''
        imgPath: string
            The image path
        '''
        self.PWD = getcwd()
        self.IMG = imgPath
        self.WIDTH = 80
        self.HEIGHT = 80
        self.fourbit_convert()

    def write_values (self):
        '''
        This function will write the 
        image data values
        '''

        with open(f"{self.PWD}/data.txt", "w+") as txt:
            txt.write(f'{self.WIDTH} x {self.HEIGHT}/{self.pix_values()}')
    
    def fourbit_convert (self):
        with Image.open(self.IMG) as img:
            nimg = img.convert("P", palette=Image.ADAPTIVE, colors=32)
            fixed_height = 100
            
            height_percent = (fixed_height / float(nimg.size[1]))

            width_size = int((float(nimg.size[0]) * float(height_percent)))
            nimg = nimg.resize((width_size, fixed_height), Image.ANTIALIAS)
            self.WIDTH, self.HEIGHT = nimg.width, nimg.height
            nimg.save(f'IMAGE-16bit.png', format="png")

    def pix_values(self):
        '''
        This function will return the 
        rgb value of each pixel in an image
        
                  R    G  B
        example: (255, 0, 0)
        '''
        pix = ""
        with Image.open(f'{self.PWD}/IMAGE-16bit.png') as img:
            for x in range(img.width):
                for y in range(img.height):
                    nimg = img.convert("RGBA").transpose(method=Image.FLIP_LEFT_RIGHT) 
                    CURR_PIXEL = nimg.getpixel((img.width-x-1, img.height-y-1))
                    if len(CURR_PIXEL) == 4:
                        pix += f'{CURR_PIXEL[0]} {CURR_PIXEL[1]} {CURR_PIXEL[2]} {CURR_PIXEL[3]}/'

                    else:
                        pix += f'{CURR_PIXEL[0]} {CURR_PIXEL[1]} {CURR_PIXEL[2]} 255/'
                    
                    print(f'x: {x}, y: {y}, width: {self.WIDTH}, height: {self.HEIGHT}', end="\r")
        print()
        return pix

if __name__ == "__main__":
    IMAGE = argv[len(argv)-1]
    
    for POSSIBLE_EXTENSION in ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'svg']:
        if POSSIBLE_EXTENSION in IMAGE:
            IMG_OBJ = PyImg2GD(IMAGE)
            print(f'{colorama.Fore.LIGHTGREEN_EX}Writting data in {colorama.Style.BRIGHT}data.txt')
            IMG_OBJ.write_values()
            exit()
        
    
    print(f'{colorama.Fore.LIGHTRED_EX}Invalid file')
