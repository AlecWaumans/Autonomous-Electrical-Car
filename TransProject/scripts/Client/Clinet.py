import cv2
import imutils
from imutils.video import VideoStream
import requests
import time
import json
from mDev import mDEV 

class CameraClient:
    def __init__(self, server_url, mdev_instance):
        """
        Initializes the camera client.
        :param server_url: URL of the server to send photos to.
        """
        self.server_url = server_url
        self.vs = VideoStream(src=0).start()  # Start the video stream
        time.sleep(2.0)  # Warm-up the camera
        self.mdev = mdev_instance

    def move(self, dir_left, dir_right, speed=500):
        """
        Moves the motors in the specified directions at a fixed speed.
        :param dir_left: Direction for left motor (0 = backward, 1 = forward)
        :param dir_right: Direction for right motor (0 = backward, 1 = forward)
        :param speed: PWM value (0 - 1000)
        :param duration: Duration of movement in seconds
        """
        print(f"Moving: Left DIR={dir_left}, Right DIR={dir_right}, Speed={speed}")

        # Set motor directions
        self.mdev.writeReg(self.mdev.CMD_DIR1, dir_left)
        self.mdev.writeReg(self.mdev.CMD_DIR2, dir_right)

        # Set motor speeds
        self.mdev.writeReg(self.mdev.CMD_PWM1, speed)
        self.mdev.writeReg(self.mdev.CMD_PWM2, speed)

    def get_distance(self):
        """
        Measures distance using the ultrasonic sensor.
        :return: Distance in centimeters
        """
        try:
            distance = self.mdev.getSonic()
            return distance
        except Exception as e:
            print(f"Error reading ultrasonic sensor: {e}")
            return float('inf')  # Return infinity if there's an error
        
        
    def take_photo(self):
        """
        Captures a photo from the video stream and sends it to the server.
        """
        print("Taking a photo...")
        frame = self.vs.read()  # Capture a frame from the camera
        frame = imutils.resize(frame, width=500)  # Resize for consistent dimensions

        # Encode the frame as JPEG
        _, encoded_image = cv2.imencode(".jpg", frame)
        if encoded_image is None:
            print("Error encoding the image.")
            return None

        # Generate a filename for the image
        filename = "photo.jpg"  # You can make this dynamic if needed

        # Send the photo to the server
        try:
            print("Sending photo to server...")
            response = requests.post(
                f"{self.server_url}/upload",
                files={"file": (filename, encoded_image.tobytes(), 'image/jpeg')}  # Specify the filename and MIME type
            )

            if response.status_code == 200:
                try:
                    # Attempt to parse JSON response
                    response_data = response.json()
                    print(f"Parsed JSON response: {response_data}")
                    return (f"{response_data}")  # Extract 'direction' key
                except ValueError:
                    # If response is not JSON, treat it as plain text
                    print("Response is not JSON, treating as plain text.")
                    return response.text.strip()  # Assume plain text and strip whitespace
            else:
                print(f"Error: Server returned status code {response.status_code}")
                return None
        except Exception as e:
            print(f"Error sending photo: {e}")
            return None



    def go_left(self, speed=400):
        print("Turning LEFT...")
        time.sleep(0.5)
        self.mdev.setServo("3",130)
        time.sleep(0.5)
        self.move(dir_left=0, dir_right=0, speed=490)  # Turn left
        time.sleep(1.3) #time for rotation
    
    def go_right(self, speed=400):
        print("Turning RIGHT...")
        time.sleep(0.5)
        self.mdev.setServo("3",50)
        time.sleep(0.5)
        self.move(dir_left=1, dir_right=1, speed=490)  # Turn right
        time.sleep(1.3) #time for rotation

    def go_forward(self, speed=400):
        # Move forward if no obstacle or distance reading is invalid
        self.move(dir_left=0, dir_right=1, speed=speed)

    def go_backward(self, speed=400):
        self.move(dir_left=1, dir_right=0, speed=500) 
        time.sleep(0.3) # 0.6
        self.stop_wheels() 
        
        
        
    def stop_wheels(self):
        """Stops both motors."""
        print("Stopping motors...")
        self.mdev.writeReg(self.mdev.CMD_PWM1, 0)
        self.mdev.writeReg(self.mdev.CMD_PWM2, 0)

    def stop(self):
        """
        Stops the video stream.
        """
        print("Stopping the video stream...")
        self.vs.stop()
        
        
    def boocleForCar(self, speed=400, obstacle_distance=20):

        print("Starting route navigation...")
        
        try:
            while True:
                distance = self.get_distance()
                print(f"Distance: {distance:.2f} cm")
                mdev_instance.setServo("2",10) #move servo (ultrasonic sensor placement)

                if distance > obstacle_distance or distance == 0:
                    mdev_instance.setLed(0,0,1);
                    # Move forward if no obstacle
                    self.mdev.setServo("3",90)
                    self.go_forward()
                    print("Moving forward...")
                else:
                    # Stop when obstacle is detected
                    mdev_instance.setLed(1,0,0);
                    self.stop_wheels()
                    time.sleep(1)
                    self.go_backward()
                    mdev_instance.setServo("2",90) #turn servo (camera placement)
                    time.sleep(0.5)
                    turn_direction = self.take_photo()
                    print("response:", turn_direction)
                    time.sleep(1)
                    
                    if turn_direction == "left":
                        mdev_instance.setLed(0,1,0);
                        mdev_instance.setServo("2",10) #move servo (ultrasonic sensor placement)
                        print("Turning LEFT...")
                        time.sleep(0.5)
                        self.go_left()
                        
                    elif turn_direction == "right":
                        mdev_instance.setLed(0,1,0);
                        mdev_instance.setServo("2",10) #move servo (ultrasonic sensor placement)
                        print("Turning RIGHT...")
                        time.sleep(0.5)
                        self.go_right()
                    elif turn_direction == "stop":
                        print("stoping program")
                        time.sleep(3)
                        #return

                    #self.stop_wheels()
                    print("Turn completed. Rechecking distance...")
                    time.sleep(1) 

        except KeyboardInterrupt:
            print("Navigation stopped by user.")
            self.stop_wheels()
            self.stop()

if __name__ == "__main__":
    SERVER_URL = "http://192.168.1.100:9090"  # Replace <SERVER_IP> with the actual server address
    mdev_instance = mDEV()  # Create an instance of the mDEV class
    motor_test = CameraClient(SERVER_URL,mdev_instance)    
    mdev_instance.setServo("3",90) # trun servo (forward wheel position)
    mdev_instance.setServo("2",10) # trun servo (ultrasonic sensor poisition)
    motor_test.boocleForCar()
    

    client = CameraClient(SERVER_URL)
    
    client.stop()
