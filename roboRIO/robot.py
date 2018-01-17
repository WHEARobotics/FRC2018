#!/usr/bin/env python3
"""
    WHEA Robotics 3881 code for FRC 2017.
#test
"""

import wpilib
import ctre

class MyRobot(wpilib.IterativeRobot):
    
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """

        """
        Button Map for Dual Joysticks:
        1: Shooter + Loader (Hold for 1 second)
        2: Climber
        3: Gatherer
        """
        
        # Configure shooter motor controller.
        self.shooter = ctre.CANTalon(3) # Create a CANTalon object.
        self.shooter.setFeedbackDevice(ctre.CANTalon.FeedbackDevice.QuadEncoder) # Choose an encoder as a feedback device.  The default should be QuadEncoder already, but might as well make sure.
        # I thought the encoder was 20 pulses per revolution per phase, which would require "80" as an argument below, but after trying it, it looks like there are 12.
        # Setting this parameter changes things so getPosition() returns decimal revolutions, and getSpeed() returns RPM.
        self.shooter.configEncoderCodesPerRev(48)
        # resets shooter position on startup
        self.shooter.setPosition(0)
        self.shooter.enableBrakeMode(False)# This should change between brake and coast modes.
        

        self.l_motor = ctre.CANTalon(1)
        self.l_motor.setInverted(True)
        self.r_motor = ctre.CANTalon(2)
        self.r_motor.setInverted(True)
        # Configure shooter motor controller.
         # Create a CANTalon object.
        self.l_motor.setFeedbackDevice(ctre.CANTalon.FeedbackDevice.QuadEncoder)
        self.r_motor.setFeedbackDevice(ctre.CANTalon.FeedbackDevice.QuadEncoder)# Choose an encoder as a feedback device.  The default should be QuadEncoder already, but might as well make sure.
        # I thought the encoder was 20 pulses per revolution per phase, which would require "80" as an argument below, but after trying it, it looks like there are 12.
        # Setting this parameter changes things so getPosition() returns decimal revolutions, and getSpeed() returns RPM.
        self.l_motor.configEncoderCodesPerRev(48)
        self.r_motor.configEncoderCodesPerRev(48)
        # resets shooter position on startup
        self.l_motor.setPosition(0)
        self.r_motor.setPosition(0)

        #self.stick = wpilib.Joystick(0)
        self.l_joy = wpilib.Joystick(0)
        self.r_joy = wpilib.Joystick(1)
        self.climb = wpilib.Spark(0)
        self.gatherer = wpilib.Spark(1)
        self.agitator = wpilib.Jaguar(2)
        self.loader = wpilib.Jaguar(3)
        self.drive = wpilib.RobotDrive(self.l_motor , self.r_motor)
        self.counter = 0
        self.mode = 0
        #wpilib.CameraServer.launch()
        #IP for camera server: http://10.38.81.101:1181/
        
        
        

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.auto_loop_counter = 0
        self.shooter.setPosition(0)
        self.l_motor.setPosition(0)
        self.r_motor.setPosition(0)
        self.l_motor.enableBrakeMode(True)
        self.r_motor.enableBrakeMode(True)
        self.agitator.set(0.7)
    

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        """
        #Rotates
        if self.auto_loop_counter <34:
            self.drive.drive(-0.5,-1)
        """
        if self.r_motor.getPosition()> -4000 and self.auto_loop_counter <800:
            self.drive.drive(-1,0)

        else:
            self.drive.drive(0,0)
        """
        if self.auto_loop_counter <100:
            self.drive.drive(-0.5,0)
        
        #Drives
        if self.auto_loop_counter >=100 and self.auto_loop_counter <300:
            self.drive.drive(1,0)
        
        if self.auto_loop_counter <50:
            self.drive.drive(0,1)
        elif self.auto_loop_counter >=50 and self.auto_loop_counter <100:
            self.drive.drive(1,1)
        elif self.auto_loop_counter >=100 and self.auto_loop_counter <150:
            self.shooter.set(1)
        elif self.auto_loop_counter >=200 and self.auto_loop_counter <250:
            self.drive.drive(-1,-1)
        
        #This stops the robot at 14.5 seconds
        #elif self.auto_loop_counter >=(725):
            #self.robot_drive.drive(0,0)
        
        else:
            self.drive.drive(0,0)
        
        """
        self.auto_loop_counter +=1

        if self.auto_loop_counter % 50 == 0:
            # Uncomment whichever line you want to use.  Need to have a shooter to use the second one.
            print(self.auto_loop_counter, ' pos: ', self.l_motor.getPosition() , self.r_motor.getPosition())
        #This counter runs 50 times a second
        

       
            
            
            
            


    def teleopInit(self):
        #resets printed shooter position on enable
        self.shooter.setPosition(0)
        self.l_motor.setPosition(0)
        self.r_motor.setPosition(0)
        self.tele_counter = 0
        self.auto_loop_counter = 0
        self.l_motor.enableBrakeMode(False)
        self.r_motor.enableBrakeMode(False)
        self.agitator.set(0.7)
        

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        
        self.drive.tankDrive(self.l_joy.getRawAxis(1) , self.r_joy.getRawAxis(1))
        
        if self.l_joy.getRawButton(3) or self.r_joy.getRawButton(3):
            self.gatherer.set(-1)
        else:
            self.gatherer.set(0)

        if self.l_joy.getRawButton(2) or self.r_joy.getRawButton(2):
            self.climb.set(1)
        else:
            self.climb.set(0)
            

        # Pulling the trigger starts the shooting/loading process, releasing stops it.
        if self.l_joy.getRawButton(1):
            self.shooter.set(1)
            self.auto_loop_counter += 1 # Setting it to nonzero starts it up; only increments when trigger held.
        else:
            self.auto_loop_counter = 0 # setting to zero stops below.

        # Now do things based on the value of the counter.
        if self.auto_loop_counter == 0:
            self.shooter.set(0) # If zero, we are stopped.
            self.loader.set(0)
        elif self.auto_loop_counter > 0 and self.auto_loop_counter <= 50:
        # For one second the shooter is only on.  Technically, we would only have to set when entering this condition, but this makes it clear.
             self.shooter.set(1)
        else:
        # Executed if self.auto_loop_counter is > 100, or trigger held longer than 1 second.
             self.shooter.set(1)
             self.loader.set(0.7)
        
        self.auto_loop_counter +=1

        """
        if self.mode == 0:
            self.release.set(1)
            if self.r_joy.getRawButton(1):
                self.mode = 1
                self.tele_counter = 0
        elif self.mode == 1:
            self.release.set(0.5)
            if self.tele_counter < 100:
                self.mode = 0
        self.tele_counter += 1
        """
        
        self.counter += 1
        if self.counter % 90 == 0:
            # Uncomment whichever line you want to use.  Need to have a shooter to use the second one.
            print(self.counter, ' pos: ', self.l_motor.getPosition() , self.r_motor.getPosition())
            

            """
            print(self.counter)
            print(self.counter, ' axis: ', self.l_joy.getRawAxis(2) and self.r_joy.getRawAxis(2), ' pos: ', self.shooter.getPosition(), ' rpm: ', self.shooter.getSpeed())
            """

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()
        


if __name__ == "__main__":
wpilib.run(MyRobot)
