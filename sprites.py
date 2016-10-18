import os
from PIL import Image
import glob

#get your images using glob
iconMap = glob.glob("images/*.jpg")
#just take the even ones
iconMap = sorted(iconMap)
#iconMap = iconMap[::2]

print len(iconMap)

images = [Image.open(filename) for filename in iconMap]

print "%d images will be combined." % len(images)

image_width, image_height = images[0].size

print "all images assumed to be %d by %d." % (image_width, image_height)

master_width = (image_width * len(images) ) 
#seperate each image with lots of whitespace
master_height = image_height
print "the master image will by %d by %d" % (master_width, master_height)
print "creating image...",
master = Image.new(
    mode='RGBA',
    size=(master_width, master_height),
    color=(0,0,0,0))  # fully transparent

print "created."

for count, image in enumerate(images):
    location = image_width*count
    print "adding %s at %d..." % (iconMap[count][1], location),
    master.paste(image,(location,0))
    print "added."
print "done adding icons."

print "saving master.jpg...",
master.save('master.jpg', transparency=0 )
print "saved!"
