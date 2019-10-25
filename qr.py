# License MIT

# Copyright 2019 Derwent Ready

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import qrcode
import qrcode.image.svg

def getFilename():
    filename = input("Filename: ")
    return filename.strip()

print("Please enter QR Data. To end press enter with no other text.")

sentinel = '' # QR Data ends when this string is seen
factory = None

version = None

data = '\n'.join(iter(lambda: input("QR Data: "), sentinel)).strip() # Allows for multiline input. Requires the sentinel string to end input. lambda allows to pass the prompt parameter to *_input() otherwise use iter(input, sentinel)

img_type = input("Image Type (svg/png/jpg/bmp): ")

img_type = img_type.lower().strip()
ext = ""

if img_type == "svg":
    ext = ".svg"
    valid = False
    while not valid:
        method = input("SVG Type (basic/fragment/path): ")
        method = method.lower().strip()
        valid = (method in ["basic", "fragment", "path"])
        continue
        print("Invalid type " + method)

    if method == 'basic':
	    factory = qrcode.image.svg.SvgImage
    elif method == 'fragment':
	    factory = qrcode.image.svg.SvgFragmentImage
    elif method == 'path':
	    factory = qrcode.image.svg.SvgPathImage

    img_type = img_type.upper()

elif img_type in ["png", "jpg", "bmp"]:
    ext = "." + img_type

    version = input("QR Version: (1-40/auto)")
    vers = version.strip()
    if vers.lower() in ["auto", ""]:
        version = None
    else:
        version = int(vers)
        if version < 0 or version > 40:
            print("Version out of bounds (1-40). Defaulting to auto instead.")
            version = 0
    if version == 0:
        version = None

    img_type = "image"

else:
    print("Incorrect input parameters, please try again. Goodbye.")
    quit()

fill_col = input("Fill colour: (colorname/hexcode [default: black])")
if fill_col.strip() == "":
    fill_col = "black"
back_col = input("Back colour: (colorname/hexcode [default: white])")
if back_col.strip() == "":
    back_col = "white"

valid = False
while not valid:
    size = input("Box size: [default: 10]")
    try:
        box_size = int(size)
        valid = True
    except:
        print("Please input an integer for box size")

filename = getFilename()
if not filename.endswith(ext):
    filename += ext

qr = qrcode.QRCode(
        version = version,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = box_size,
        border = 4,
        image_factory = factory,
)

qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color=fill_col, back_color=back_col)

img.save(filename)
print("QR %s generated" % img_type)
