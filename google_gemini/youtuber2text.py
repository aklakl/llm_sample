"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
#Seems like not working?????
import google.generativeai as genai

g_gemini_key="AIzaSyAG9M9CFujKMKgUD1z_n-hLGozCs90ZTJ8"
g_youtube_url="https://youtu.be/hOqa9tox-Kg"


genai.configure(api_key=g_gemini_key)

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["convert this video to text =>https://youtu.be/hOqa9tox-Kg"]
  },
  {
    "role": "model",
    "parts": ["**YouTube video title:** Build a Simple Home Security Camera System with Raspberry Pi\n\n**Description:**\n\nIn this video, I'll show you how to build a simple home security camera system using a Raspberry Pi. This project is perfect for anyone who wants to add an extra layer of security to their home without spending a lot of money.\n\n**Steps:**\n\n1. **Gather your materials.**\n\n* Raspberry Pi 3B+\n* Raspberry Pi camera module\n* Microphone\n* USB flash drive (at least 8GB)\n* Ethernet cable\n* Power supply\n* MicroSD card (at least 8GB)\n* Case for the Raspberry Pi (optional)\n\n2. **Install the Raspberry Pi OS.**\n\n* Download the latest version of the Raspberry Pi OS from the Raspberry Pi website.\n* Write the OS image to your microSD card using a microSD card reader.\n* Insert the microSD card into the Raspberry Pi.\n\n3. **Configure the Raspberry Pi.**\n\n* Connect the Raspberry Pi to a monitor, keyboard, and mouse.\n* Boot up the Raspberry Pi.\n* Follow the on-screen instructions to configure the Raspberry Pi.\n\n4. **Install the motion software.**\n\n* Motion is a free and open-source motion detection software that can be used to trigger the camera.\n* To install motion, open a terminal window and type the following commands:\n\n```\nsudo apt-get update\nsudo apt-get install motion\n```\n\n5. **Configure the motion software.**\n\n* To configure motion, open the motion.conf file in a text editor.\n* In the motion.conf file, find the following line:\n\n```\ndaemon on\n```\n\n* Uncomment this line by removing the \"#\" at the beginning of the line.\n* Save the motion.conf file.\n\n6. **Start the motion software.**\n\n* To start the motion software, open a terminal window and type the following command:\n\n```\nsudo service motion start\n```\n\n7. **Test the motion software.**\n\n* To test the motion software, walk in front of the camera.\n* The motion software should detect your movement and start recording a video.\n\n8. **Set up remote viewing.**\n\n* To view the camera feed remotely, you can use a VNC viewer.\n* To install a VNC viewer, open a terminal window and type the following command:"]
  },
])

convo.send_message("Could you please assist me in transcribing the voice from URL's video into text?")
print(convo.last.text)





