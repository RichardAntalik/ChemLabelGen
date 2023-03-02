import pubchempy 
import urllib.request
import json
import pprint

from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageMath

class PC:
    def __init__(self, data):
        self.data = data

    def s(self, name):
        for section in self.data:
            if section["TOCHeading"] == name:
                try: 
                    return PC(section["Section"])
                except KeyError:
                    return PC(section["Information"])
                
    def value(self, unit = None):
        if unit != None:
            for item in self.data:
                value = ""
                try:
                    value = item["Value"]["StringWithMarkup"][0]["String"]
                except KeyError:
                    if hasattr(item["Value"], "Unit"):
                        value = str(item["Value"]["Number"][0]) + " " + item["Value"]["Unit"]
                if unit in value:
                    break
        else: 
            value = self.data[0]["Value"]["StringWithMarkup"][0]["String"]
            
        return value
        

def get_text(data, comment):
    pc = PC(data)
    try:
        mw = pc.s("Chemical and Physical Properties").s("Computed Properties").s("Molecular Weight").value() + " g/mol"
    except AttributeError:
        mw = "N/A"
    try:
        bp = pc.s("Chemical and Physical Properties").s("Experimental Properties").s("Boiling Point").value("°C")
    except AttributeError:
        bp = "N/A"
    try:
        mp = pc.s("Chemical and Physical Properties").s("Experimental Properties").s("Melting Point").value("°C")
    except AttributeError:
        mp = "N/A"
    try:
        dens = pc.s("Chemical and Physical Properties").s("Experimental Properties").s("Density").value().split()[0]
    except AttributeError:
        dens = "N/A"
    
    text = comment + "\n"
    text += "Boiling Point: " + bp + "\n"
    text += "Melting Point: " + mp + "\n"
    text += "Molecular weight: " + mw + "\n"
    text += "Density: " + dens + "\n"
    
    return text

def draw_title(draw_ctx):
    fnt = ImageFont.truetype("Pillow/Tests/fonts/times.ttf", 40)
    _, _, w, h = draw_ctx.textbbox((0, 0), name, font=fnt)
    if w > 700:
        fnt = ImageFont.truetype("Pillow/Tests/fonts/times.ttf", 30)
        _, _, w, h = draw_ctx.textbbox((0, 0), name, font=fnt)
        
    title_x = (700 - w) / 2
    draw_ctx.text((title_x, 20), name, font=fnt, fill=(0, 0, 0))

def draw_text(draw_ctx, struct_img, struct_padding):
    fnt = ImageFont.truetype("Pillow/Tests/fonts/times.ttf", 20)
    text_padding = 10
    d.multiline_text((struct_img.width + struct_padding[0] + text_padding, struct_padding[1] + 100), text, font=fnt, fill=(0, 0, 0)) 

def get_struct_img(img_url):
    with urllib.request.urlopen(img_url) as response:
        struct_img = Image.open(response)
        struct_img = struct_img.convert('L')
        brightness = ImageEnhance.Contrast(struct_img)
        struct_img = brightness.enhance(1.5)
        contrast = ImageEnhance.Contrast(struct_img)
        return contrast.enhance(10)

def white_to_alpha(img, threshold):
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] >= threshold and item[1] >= threshold and item[2] >= threshold:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)


name = input("Gimme PubChem CID, formula or name: ")
comment = input("Any comment? ")

if name.isnumeric():
    cid = name
else:
    cid = pubchempy.get_compounds(name, 'name')[0].cid
    
print("CID:", cid)

url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/" + str(cid) + "/JSON"

with urllib.request.urlopen(url) as response:
    data = response.read()
data = json.loads(data)
name = data["Record"]["RecordTitle"]
text = get_text(data["Record"]["Section"], comment)

out = Image.new("RGBA", (700, 350), (255, 255, 255))

img_url = "https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid=" + str(cid) + "&t=l"
struct_img = get_struct_img(img_url)

struct_img = struct_img.convert('RGBA')
white_to_alpha(struct_img, 240)

struct_padding = (80, 50)

out.paste(struct_img, box=struct_padding)
d = ImageDraw.Draw(out)
draw_title(d)
draw_text(d, struct_img, struct_padding)

white_to_alpha(out, 255)
out.save("label.png", dpi=(254,254))
print("label saved.")
