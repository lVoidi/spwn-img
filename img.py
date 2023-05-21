"""
This file will convert any image into a 32 colors image and also will scale its height
to 100, so the image don't take too much memory and space in the level. Aditionally, to 
make the spwn file work, it will save the info of the image in a text file. By info i mean
the rgb values of each pixel in the image and its size.
"""

from sys import argv
import colorama
from PIL import Image
from os import getcwd

class PyImg2GD:
    def __init__(self, img_path: str):
        '''
        img_path: string
            The image path
        '''
        self.cwd = getcwd()
        self.img = img_path
        self.width = 80
        self.height = 80
        self.fourbit_convert()

    def write_values (self):
        '''
        This function will write the 
        image data values
        '''

        with open(f"{self.cwd}/data.txt", "w+") as txt:
            txt.write(f'{self.width} x {self.height}/{self.pix_values()}')
    
    def fourbit_convert (self):
        with Image.open(self.img) as img:
            nimg = img.convert("P", palette=Image.ADAPTIVE, colors=32)
            fixed_height = 100
            
            height_percent = (fixed_height / float(nimg.size[1]))

            width_size = int((float(nimg.size[0]) * float(height_percent)))
            nimg = nimg.resize((width_size, fixed_height), Image.ANTIALIAS)
            self.width, self.height = nimg.width, nimg.height
            nimg.save(f'IMAGE-16bit.png', format="png")

    def pix_values(self):
        '''
        This function will return the 
        rgb value of each pixel in an image
        
                  R    G  B
        example: (255, 0, 0)
        '''
        pix = ""
        with Image.open(f'{self.cwd}/IMAGE-16bit.png') as img:
            for x in range(img.width):
                for y in range(img.height):
                    nimg = img.convert("RGBA").transpose(method=Image.FLIP_LEFT_RIGHT) 
                    current_pixel = nimg.getpixel((img.width-x-1, img.height-y-1))
                    if len(current_pixel) == 4:
                        pix += f'{current_pixel[0]} {current_pixel[1]} {current_pixel[2]} {current_pixel[3]}/'

                    else:
                        pix += f'{current_pixel[0]} {current_pixel[1]} {current_pixel[2]} 255/'
                    
                    print(f'x: {x}, y: {y}, width: {self.width}, height: {self.height}', end="\r")
        print()
        return pix

if __name__ == "__main__":
    image = argv[len(argv)-1]
    
    for possible_extension in ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'svg']:
        if possible_extension in image:
            image_object = PyImg2GD(image)
            print(f'{colorama.Fore.LIGHTGREEN_EX}Writting data in {colorama.Style.BRIGHT}data.txt')
            image_object.write_values()
            exit()
        
    
    print(f'{colorama.Fore.LIGHTRED_EX}Invalid file')
