import time
from datetime import datetime
import cv2
import face_recognition as fr
from twilio.rest import Client
from imgurpython import ImgurClient


def initTwilio():
    # Your Account SID from twilio.com/console
    account_sid = #Your Twilio SID
    # Your Auth Token from twilio.com/console
    auth_token  = #Your Twilio Token
    client = Client(account_sid, auth_token)
    return client


def initImgur():
    #Initializes Imgur API
    client_id = #YOUR CLIENT ID
    client_secret = #YOUR SECRET
    imgurClient = ImgurClient(client_id, client_secret)
    return imgurClient


def notifyPhone(name, client, imgur_response_object):
    #sends picture and text to phone with ID
    #passes uploaded image Imgur link to URL
    message = client.messages.create(
        to="5",  #Replace 5 with destination number
        from_="+1", # Add your Twilio number here
        body=f'{name} is accessing your computer.',
        media_url=(imgur_response_object['link']))


def getCamera():
    camera = cv2.VideoCapture(0)
    time.sleep(2)
    return camera


def deleteImage():
    pass


def saveDeleteHash(imgur_response_object):
    with open('./deletehashes/deletehashes.txt', 'a') as f:
        f.write('\n{}'.format(imgur_response_object['deletehash']))


def uploadToImgur(path, imgur_client):
    imgur_response_object = imgur_client.upload_from_path(path, config=None, anon=True)
    return imgur_response_object


def releaseCamera(camera):
    camera.release()


def takePicture(camera):
    success, frame = camera.read()
    path = './img/unknown/img{}.png'.format(datetime.now())
    cv2.imwrite(path, frame)
    return frame, path

#Change names accordingly
def faceID(marvin, dan, unknown, sms_client, imgur_response_object):

    testDan = fr.compare_faces(dan, unknown, tolerance = 0.5)
    
    if testDan[0]:
        notifyPhone('Daniel', sms_client, imgur_response_object)
    else:
        testMarvin = fr.compare_faces(marvin, unknown, tolerance=0.5)
        if testMarvin[0]:
            notifyPhone('Marvin', sms_client, imgur_response_object)
        else:
            notifyPhone('Unknown person', sms_client, imgur_response_object)


def main():
    #starting messaging and upload services
    sms_client = initTwilio()
    imgur_client = initImgur()

    #take picture
    cam = getCamera()
    frame, path = takePicture(cam)
    releaseCamera(cam)

    imgur_response_object = uploadToImgur(path, imgur_client)
    saveDeleteHash(imgur_response_object)

    #load known faces
    dan_image = fr.load_image_file('./img/known/dan.png')   #Replace with your known image file
    marvin_image = fr.load_image_file('./img/known/marvin.jpg') #
    unknown_image = fr.load_image_file(path)

    #encode faces for faceID algorithm
    try:
        dan_face_encoding = fr.face_encodings(dan_image)[0]
        marvin_face_encoding = fr.face_encodings(marvin_image)[0]
        unknown_face_encoding = fr.face_encodings(unknown_image)[0]
    except IndexError:
        print("No faces in at least one of these images.")
        quit()

    #Compare face encondings with known faces and send results over sms
    faceID([marvin_face_encoding],
            [dan_face_encoding],
            unknown_face_encoding,
            sms_client,
            imgur_response_object)


if __name__ == "__main__":
    main()
