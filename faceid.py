import face_recognition as fr
import cv2
import time
import datetime
from twilio.rest import Client


def initTwilio():
    # Your Account SID from twilio.com/console
    account_sid = 'AC1987dfb59ace010634e69ba5f01bd734'
    # Your Auth Token from twilio.com/console
    auth_token  = '951576f76b5e57fc514a9906b3d04e9f'

    client = Client(account_sid, auth_token)
    return client


def notifyPhone(client, picture, name):
    #sends picture and text to phone with ID
    message = client.messages.create(
        to="+12016632797",
        from_="+17853284264",
        body=f'{name} is accessing your computer.')


def getCamera():
    camera = cv2.VideoCapture(0)
    time.sleep(2)
    return camera


def releaseCamera(camera):
    camera.release()


def takePicture(camera):
    success, frame = camera.read()
    path = './img/unknown/img{}.png'.format(datetime.datetime.now())
    cv2.imwrite(path, frame)
    return frame, path

def addKnownFace(image):
    pass

def main():
    #starting messaging service
    sms_client = initTwilio()

    #take picture
    cam = getCamera()
    frame, path = takePicture(cam)

    #load known faces
    dan_image = fr.load_image_file('./img/known/Daniel Novikov.png')
    unknown_image = fr.load_image_file(path)

    #encode faces for faceID algorithm
    try:
        dan_face_encoding = fr.face_encodings(dan_image)[0]
        unknown_face_encoding = fr.face_encodings(unknown_image)[0]
    except IndexError:
        print("No faces in at least one of these images.")
        quit()

    #Compare face encondings with known faces and send results over sms
    results = fr.compare_faces([dan_face_encoding], unknown_face_encoding)
    if results[0]:
        notifyPhone(sms_client, 0, 'Daniel')
    else:
        notifyPhone(sms_client, 0, 'Unknown person')

    releaseCamera(cam)


if __name__ == "__main__":
    main()
