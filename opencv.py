import cv2
from djitellopy import Tello
import time
import numpy as np
# import tensorflow_hub as hub
# import tensorflow as tf
# from tf_helper import *

# FasterRCNN+InceptionResNet V2: high accuracy, # 83 second
# ssd+mobilenet V2: small and fast. #
# module_handle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"
# detector = hub.load(module_handle).signatures['default']

tello = Tello()
tello.connect()
print("### Battery:", tello.get_battery())

# tello.set_video_resolution("360p")  # Options: "720p", "480p", "360p"
# tello.set_video_fps('30')  # Options: 30 or 15 frames per second
tello.streamon()
frame_read = tello.get_frame_read()

# while True:
#     img = frame_read.frame
#     cv2.imshow("Tello Object Detection", img)
#     key = cv2.waitKey(1) & 0xff
#     if key == 27:  # ESC
#         break

tello.takeoff()

counter = 0
while True:
    counter += 1
    # img = frame_read.frame
    # height, width, _ = img.shape
    # blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    img = frame_read.frame
    if counter%100 == 0: print("### Battery:", tello.get_battery())
    ######################################################################
    # img = tf.convert_to_tensor(img)
    # converted_img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
    # start_time = time.time()
    # result = detector(converted_img)
    # end_time = time.time()
    # result = {key: value.numpy() for key, value in result.items()}
    # print("***Found %d objects." % len(result["detection_scores"]))
    # print("***Inference time: ", end_time - start_time)
    #
    # image_with_boxes = draw_boxes(
    #     img, result["detection_boxes"], # .numpy()
    #     result["detection_class_entities"], result["detection_scores"])
    ######################################################################
    classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    bboxes = classifier.detectMultiScale(img)
    max = 0
    for box in bboxes:
        x, y, width, height = box
        if ((width*height)>max) : max = width*height
        x2, y2 = x + width, y + height
        cv2.rectangle(img, (x, y), (x2, y2), (0, 0, 255), 1)
    ######################################################################
    cv2.imshow("Tello Object Detection", img)

    move = 15
    if max > 50000:  # Adjust the threshold as needed
        # Drone command to avoid the object (example: move backward)
        print("Go Back")
        tello.move_back(max(move,int(max/50000)))

    key = cv2.waitKey(1) & 0xff
    if key == 27:  # ESC
        break
    elif key == ord('w'):
        tello.move_forward(move)
    elif key == ord('s'):
        tello.move_back(move)
    elif key == ord('a'):
        tello.move_left(move)
    elif key == ord('d'):
        tello.move_right(move)
    elif key == ord('e'):
        tello.rotate_clockwise(move)
    elif key == ord('q'):
        tello.rotate_counter_clockwise(move)
    elif key == ord('r'):
        tello.move_up(move)
    elif key == ord('f'):
        tello.move_down(move)

tello.land()
tello.streamoff()
cv2.destroyAllWindows()

