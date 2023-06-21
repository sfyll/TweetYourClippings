from io import BytesIO
from dataclasses import dataclass
import hashlib
from pathlib import Path
import os
import random
import re
from string import ascii_letters
import textwrap
from typing import List, Dict, Optional

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont
from PIL.Image import Image as TypeImage

@dataclass
class ClippingData:
    clippings_per_book_title: Dict[str, List[str]]
    storedClipping: Optional[tuple[str,str]]
    image: Optional[TypeImage]

    def get_book_titles(self) -> List[str]:
        return list(self.clippings_per_book_title.keys())
    
    def get_clipping_for_book(self, book_title:str) -> List[str]:
        return self.clippings_per_book_title[book_title]
    
    def get_image_bytecode(self) -> BytesIO:
        # Save image in-memory
        b = BytesIO()
        self.image.save(b, "PNG")
        #locate pointer to first image byte
        b.seek(0)

        return b
    

class ImageBuilder:
    def __init__(self) -> None:
        self.current_path = Path(os.path.realpath(os.path.dirname(__file__)))
        self.clipping: Optional[ClippingData] = None

    def generate_clipping_data(self, font_ttf_path_extention: str = "/ttf/Death Note.ttf") -> Image:
        clippings = self.create_clippings()
        while not self.check_not_tweeted(clippings):
            continue
        else:
            self.clipping.image = self.create_png_from_string_and_save_quote_hash(font_path=str(self.current_path.parent)+font_ttf_path_extention)
    
    def write_to_hash_file(self) -> None:
        with open(str(self.current_path) + '/tweeted_clipping_hashes.txt', 'a') as file:
            file.write(hashlib.sha1(self.clipping.storedClipping[1].encode('utf-8')).hexdigest() + '\n')
    
    def create_clippings(self) -> ClippingData:
        path = str(self.current_path.parent) + '/KindleClippings'
        clippings_files = os.listdir(path)
        clippings_dict = {}

        for file_name in clippings_files:
            if file_name.endswith(".DS_Store"):
                continue
            file_path = os.path.join(path, file_name)
            with open(file_path, 'r') as file:
                content = file.read()

            delimiter_pattern = r'\n\n\.\.\.\n\n'
            clippings = re.split(delimiter_pattern, content)
            cleaned_clippings = [element for element in clippings if element != ""]
            clippings_dict[os.path.splitext(file_name)[0]] = cleaned_clippings

        return ClippingData(clippings_per_book_title=clippings_dict,
                            storedClipping=None, image=None)

    def check_not_tweeted(self, clipping: ClippingData) -> bool:
        with open(str(self.current_path) + '/tweeted_clipping_hashes.txt', 'r') as file:
            tweeted_clipping_hashes = file.read().splitlines(  )
        
        selected_book = random.choice(clipping.get_book_titles())

        selected_clippings = random.choice(clipping.get_clipping_for_book(selected_book))

        clipping_hash = hashlib.sha1(selected_clippings.encode('utf-8')).hexdigest()

        if clipping_hash not in tweeted_clipping_hashes:
            clipping.storedClipping = (selected_book, selected_clippings)
            self.clipping = clipping
            return True
        else:
            return False
    
    def create_png_from_string_and_save_quote_hash(self, font_path, font_size=34, text_color=(255,0,0,0), wrapping_factor = 0.618) -> Optional[TypeImage]:
        image = Image.open(str(self.current_path.parent)+"/public/wallpaper.jpeg")

        draw = ImageDraw.Draw(image)

        try:
            text, font = self.get_wrapped_text(self.clipping.storedClipping[1], image, font_path, font_size, wrapping_factor)
        except Exception as e:
            raise e
        
        self.write_to_hash_file()

        draw.text(xy=(image.size[0]/2, image.size[1] / 2), text=text , font=font, fill=text_color, anchor='rs')
        
        return image

    def get_wrapped_text(self, text, image, font_path, font_size, wrapping_factor) -> tuple[str,FreeTypeFont] :
        font = ImageFont.truetype(font_path, font_size)

        avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)

        max_char_count = int(image.size[0] * wrapping_factor / avg_char_width)

        wrapped_text =  textwrap.fill(text=text, width=max_char_count)

        #approximation of wrapped text height
        wrapped_text_height = len(wrapped_text.splitlines()) * font.getsize("b")[1]

        # Check if the wrapped text exceeds the image height
        if wrapped_text_height <= image.size[1]:
            return wrapped_text, font
        elif wrapped_text_height > image.size[1] and font_size > 0:
            print("Text exceeds image height. Trying with a lower font size")
            return self.get_wrapped_text(text, image, font_path, font_size-1, wrapping_factor)
        else:
            raise Exception("Sorry, the text does not fit in the picture with the given font and wrapping factor!")

if __name__ == "__main__":
    executor = ImageBuilder()