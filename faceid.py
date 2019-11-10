import face_recognition as fr
import cv2
import time
import datetime
from twilio.rest import Client
from imgurpython import ImgurClient

def initTwilio():
    # Your Account SID from twilio.com/console
    account_sid = 'AC1987dfb59ace010634e69ba5f01bd734'
    # Your Auth Token from twilio.com/console
    auth_token  = '9a556d22940430df20a7f596a64bc230'

    client = Client(account_sid, auth_token)
    return client

def initImgur():
    client_id = '0cdef4993f98863'
    client_secret = '810c1862f54a8a9038220d4de00c6cb2449ad620'
    imgurClient = ImgurClient(client_id, client_secret)
    return imgurClient

def notifyPhone(client, picture, name, imgur):
    #sends picture and text to phone with ID
    message = client.messages.create(
        to="+19737479013",
        from_="+17853284264",
        body=f'{name} is accessing your computer.',
        media_url=(imgur['link']))

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
    #starting messaging and upload services
    sms_client = initTwilio()
    mms_client = initImgur()

    #take picture
    cam = getCamera()
    frame, path = takePicture(cam)

    #upload picture
    imgur = mms_client.upload_from_path(path, config=None, anon=True)

    #load known faces
    #dan_image = fr.load_image_file('./img/known/Daniel Novikov.png')
    marvin_image = fr.load_image_file('./img/known/marvin.jpg')
    unknown_image = fr.load_image_file(path)

    #encode faces for faceID algorithm
    try:
        #dan_face_encoding = fr.face_encodings(dan_image)[0]
        marvin_face_encoding = fr.face_encodings(marvin_image)[0]
        unknown_face_encoding = fr.face_encodings(unknown_image)[0]
    except IndexError:
        print("No faces in at least one of these images.")
        quit()

    #Compare face encondings with known faces and send results over sms
    #results = fr.compare_faces([dan_face_encoding], unknown_face_encoding)
    results = fr.compare_faces([marvin_face_encoding], unknown_face_encoding)
    if results[0]:
        #notifyPhone(sms_client, 0, 'Daniel')
        notifyPhone(sms_client, 0, 'Marvin', imgur)
    else:
        notifyPhone(sms_client, 0, 'Unknown person', imgur)

    releaseCamera(cam)


if __name__ == "__main__":
    main()
