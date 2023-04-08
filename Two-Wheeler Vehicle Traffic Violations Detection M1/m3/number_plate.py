

import os
import cv2
import warnings
import torch
import torchvision
import smtplib
import imghdr
from email.message import EmailMessage


from pathlib import Path

from matplotlib import pyplot as plt

warnings.filterwarnings('ignore')


class npDetectionTest:
    # The init method or constructor
    def __init__(self, input_file, output_dir, model_path):
        # Instance Variable
        self.input_file = input_file
        self.output_dir = output_dir
        self.model_path = model_path



    def np_detection(self):
        detection_path = "output"
        detection_path = os.path.join(self.output_dir, detection_path)
        os.makedirs(detection_path, exist_ok=True)

        # get a file name and file extension
        file_name = Path(self.input_file).stem
        file_extension = Path(self.input_file).suffix

        stripped = file_name.split('_', 1)[0]

        detection_path = os.path.join(detection_path, stripped)
        os.makedirs(detection_path, exist_ok=True)

        device = torch.device('cpu') if torch.cuda.is_available() else torch.device('cpu')

        model = torch.load(self.model_path, map_location=torch.device('cpu'))
        # model.load_state_dict(torch.load(self.model_path))
        model.eval()

        input_image = cv2.imread(self.input_file)
        input_img = torchvision.transforms.functional.to_tensor(input_image).to(device)

        checkbox_tensors = model([input_img])[0]["boxes"]
        prediction = checkbox_tensors.data.cpu().numpy()

        count = 0
        for table_tensor in prediction:
            table_tensor = [int(i) for i in table_tensor]
            detected_file = f'{detection_path}/{file_name}_{count}.jpg'
            cv2.imwrite(detected_file, input_image[table_tensor[1]:table_tensor[3], table_tensor[0]:table_tensor[2]])
            count += 1

        return detected_file

    def email_to_send(self):
        Sender_Email = "cryptdac@gmail.com"
        Reciever_Email = "arunds130801@gmail.com"
        Password = "qmgvwznbllxdnzwx"

        newMessage = EmailMessage()                         
        newMessage['Subject'] = "INFRINGEMENT ALERT"
        newMessage['From'] = Sender_Email                   
        newMessage['To'] = Reciever_Email                   
        newMessage.set_content('VIOLATION DETECTED AND TICKET ISSUED')

        with open(r'output/np/np_0.jpg', 'rb') as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
            image_name = f.name

        newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

            smtp.login(Sender_Email, Password)              
            smtp.send_message(newMessage)