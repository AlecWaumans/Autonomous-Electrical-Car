import time
from mDev import mDEV  # Import the mDEV class from mDev.py

class MotorTest:
    def __init__(self, mdev_instance):
        self.mdev = mdev_instance

    def move(self, dir_left, dir_right, speed=1000):
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


    def stop(self):
        """Stops both motors."""
        print("Stopping motors...")
        self.mdev.writeReg(self.mdev.CMD_PWM1, 0)
        self.mdev.writeReg(self.mdev.CMD_PWM2, 0)
        
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
            
    def navigate_until_clear(self, speed=450, obstacle_distance=22):
        """
        Moves the robot forward until an obstacle is detected, then turns right
        until the path is clear, and repeats the process.
        :param speed: Motor speed (0 - 1000)
        :param obstacle_distance: Distance threshold in cm to stop when an obstacle is detected
        """
        print(f"Starting navigation: Forward until obstacle, then turning right...")
        
        try:
            while True:
                distance = self.get_distance()
                print(f"Distance: {distance:.2f} cm")

                if distance > obstacle_distance or distance == 0:
                    # Move forward if no obstacle or distance reading is invalid
                    self.move(dir_left=0, dir_right=1, speed=speed)
                    print("Moving forward...")
                else:
                    # Stop and turn right if obstacle detected
                    print("Obstacle detected! Stopping and turning right...")
                    self.stop()
                    time.sleep(1)  # Small pause before turning
                    
                    # Turn right until path is clear
                    while distance <= obstacle_distance:
                        # test left
                        #self.move(dir_left=0, dir_right=0, speed=600)
                        # test right
                        self.move(dir_left=1, dir_right=1, speed=500)
                        print("Turning right...")
                        time.sleep(0.1)  # Short delay for sensor checking
                        distance = self.get_distance()
                        print(f"Current Distance: {distance:.2f} cm")
                    
                    print("Path cleared! Moving forward...")
                    self.stop()  # Stop turning before resuming forward movement
                    time.sleep(1)

        except KeyboardInterrupt:
            print("Navigation stopped by user.")
            self.stop()


    def navigate_route(self, speed=400, obstacle_distance=20):
        """
        Moves the robot forward and follows a predefined route of left and right turns.
        The sequence of turns is based on the number of obstacles encountered.
        :param speed: Motor speed (0 - 1000)
        :param obstacle_distance: Distance threshold in cm to detect an obstacle
        """
        turns = ["left", "right", "right", "left", "left", "right", "right", "left", "left", "right", "right"]
        obstacle_count = 0  # Counter for encountered obstacles

        print("Starting predefined route navigation...")
        
        try:
            while obstacle_count < len(turns):
                distance = self.get_distance()
                print(f"Distance: {distance:.2f} cm")

                if distance > obstacle_distance or distance == 0:
                    # Move forward if no obstacle
                    self.mdev.setServo("3",90)
                    self.move(dir_left=0, dir_right=1, speed=speed)
                    print("Moving forward...")
                else:
                    # Stop when obstacle is detected
                    print(f"Obstacle {obstacle_count + 1} detected! Stopping...")
                    self.stop()
                    time.sleep(1)

                    # Determine the turn direction based on the route
                    turn_direction = turns[obstacle_count]
                    if turn_direction == "left":
                        print("Turning LEFT...")
                        self.move(dir_left=1, dir_right=0, speed=speed) 
                        time.sleep(0.6)
                        self.stop()
                        time.sleep(0.5)
                        self.mdev.setServo("3",130)
                        time.sleep(0.5)
                        self.move(dir_left=0, dir_right=0, speed=600)  # Turn left
                        time.sleep(2.1) 
                        
                    elif turn_direction == "right":
                        print("Turning RIGHT...")
                        self.move(dir_left=1, dir_right=0, speed=speed) 
                        time.sleep(0.6)
                        self.stop()
                        time.sleep(0.5)
                        self.mdev.setServo("3",50)
                        time.sleep(0.5)
                        self.move(dir_left=1, dir_right=1, speed=600)  # Turn right
                        time.sleep(2.1) 

                    
                    #time.sleep(2.45)  
                    
                   
                    self.stop()
                    print("Turn completed. Rechecking distance...")
                    time.sleep(1) 

                    # Increment the obstacle counter
                    obstacle_count += 1

        except KeyboardInterrupt:
            print("Navigation stopped by user.")
            self.stop()



if __name__ == "__main__":
    try:
        print("Starting motor test...")
        
        mdev_instance = mDEV()  # Create an instance of the mDEV class
        
        mdev_instance.setServo("3",90)
        motor_test = MotorTest(mdev_instance)
        mdev_instance.setServo("2",10)
        
        # Turn Servo3 to oriantate wheels
        #mdev_instance.setServo("3", 120)   #turn left 30 degrees
        #time.sleep(1)           # Wait for 1 second
        #mdev_instance.setServo("3", 90)  # forward (position inital)
        #ss
        #time.sleep(1)
        #mdev_instance.setServo("3", 60) #turn right 30 degrees
        ##time.sleep(1)
        #mdev_instance.setServo("3", 90) #forward (position inital)

        # Forward movement
        #print("Moving forward...")
        #motor_test.move(dir_left=0, dir_right=1, speed=800, duration=2)

        # Backward movement
        #print("Moving backward...")
        #motor_test.move(dir_left=1, dir_right=0, speed=800, duration=2)

        # Turn left
        #print("Turning left...")
        #motor_test.move(dir_left=1, dir_right=1, speed=800, duration=2)

        # Turn right
        #print("Turning right...")
        #motor_test.move(dir_left=0, dir_right=0, speed=800, duration=2)
        #motor_test.navigate_until_clear()
        
        
        
        motor_test.navigate_route()

        print("Motor test completed successfully.")
    except Exception as e:
        print(f"Error during motor test: {e}")
