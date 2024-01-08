# importing modules   refer:https://www.geeksforgeeks.org/how-to-open-an-image-from-the-url-in-pil/   PIL=Python Imaging Library(Pillow is based on PIL model fork)
import urllib.request 
from PIL import Image 
import requests
from io import BytesIO


#file = "C://Users/ABC/Motorbike.jpg"
#img = Image.open(file)  #local file
#image_url = "https://www.tutorialspoint.com/images/logo.png"
#image_url = "https://live-cdn-www.nypl.org/s3fs-public/csr-icons.jpg"
image_url = "https://s3.amazonaws.com/formaloo-en/f/uploads/ur/89cd8be71d781d86/fm/NriKaD2r/441f164e-2ec6-45ad-8500-0e3c5def228b.png"

# #These are based on base64 formatting with "data:image/x-icon;base64,"
#image_url = "https://oss.feidee.net/oss/group_oss_trans3_f9651cb59a6ee921_1597X1276.jpg"
#image_url = "https://drive.google.com/file/d/1fQL0N2gOJdCdkuNoNyZJMkpSSHYkFQO5/view?file=tmp_image.jpg"


# #urllib.request.urlretrieve('https://media.geeksforgeeks.org/wp-content/uploads/20210318103632/gfg-300x300.png', "tmp_image.jpg") 
# urllib.request.urlretrieve(image_url,"tmp_image.jpg") 
# img = Image.open("tmp_image.jpg") 
# img.show()
# img.save("./new_img.jpg")
print("COMPLETE")


# Download the image using requests
my_res = requests.get(image_url)
# Open the downloaded image in PIL
my_img = Image.open(BytesIO(my_res.content))
my_img.save("./temp.png")
# Show the image
my_img.show()

# #to save the image_url in to local, but this is not supporting the base64 formatting  with "data:image/x-icon;base64,"
# img_data = requests.get(image_url).content
# with open('image_name.png', 'wb') as handler:
#     handler.write(img_data)


print("COMPLETE")