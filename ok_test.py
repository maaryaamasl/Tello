from djitellopy import Tello

tello = Tello()
tello.connect()
print(tello.get_battery())
# tello.set_video_resolution("360p") # Error with Tello2 lib

# tello.takeoff()

# tello.move_left(15)
# tello.rotate_counter_clockwise(90)
# tello.move_forward(100)
# tello.move_right(15)

# tello.land()