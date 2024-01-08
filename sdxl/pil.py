# importing modules   refer:https://www.geeksforgeeks.org/how-to-open-an-image-from-the-url-in-pil/
import urllib.request 
from PIL import Image 
import requests
from io import BytesIO


#file = "C://Users/ABC/Motorbike.jpg"
#img = Image.open(file)  #local file
#image_url = "https://www.tutorialspoint.com/images/logo.png"
#image_url = "https://oss.feidee.net/oss/group_oss_trans3_f9651cb59a6ee921_1597X1276.jpg"
image_url = "https://drive.google.com/file/d/1fQL0N2gOJdCdkuNoNyZJMkpSSHYkFQO5/view?file=tmp_image.jpg"
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
# Show the image
my_img.show()

print("COMPLETE")