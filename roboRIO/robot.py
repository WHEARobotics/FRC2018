#!/usr/bin/env python3
"""
    WHEA Robotics 3881 code for FRC 2018.
#test
"""

import wpilib
import ctre
import wpilib.drive


class MyRobot(wpilib.IterativeRobot):
    
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """

        """
        Button Map for Dual Joysticks:
        Left Joystick:
        1. Chute Intake
        2. Climb Up
        3. Loader Intake

        Right Joystick:
        1. Chute Outtake
        2. Climb Down
        3. Loader Outtake
        """
        
##        # Configure shooter motor controller.
##        #self.shooter = ctre.wpi_talonsrx.WPI_TalonSRX(3) # Create a CANTalon object.
##        #self.shooter.setFeedbackDevice(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder) # Choose an encoder as a feedback device.  The default should be QuadEncoder already, but might as well make sure.
##        # I thought the encoder was 20 pulses per revolution per phase, which would require "80" as an argument below, but after trying it, it looks like there are 12.
##        # Setting this parameter changes things so getPosition() returns decimal revolutions, and getSpeed() returns RPM.
##        #self.shooter.configEncoderCodesPerRev(48)
##        # resets shooter position on startup
##        #self.shooter.setPosition(0)
##        #self.shooter.enableBrakeMode(False)# This should change between brake and coast modes.
        

        self.l_motorFront = ctre.wpi_talonsrx.WPI_TalonSRX(1)
        self.l_motorFront.setInverted(True)

        self.l_motorBack = ctre.wpi_talonsrx.WPI_TalonSRX(2)
        self.l_motorBack.setInverted(True)

        self.r_motorFront = ctre.wpi_talonsrx.WPI_TalonSRX(3)
        self.r_motorFront.setInverted(True)
        
        self.r_motorBack = ctre.wpi_talonsrx.WPI_TalonSRX(4)
        self.r_motorBack.setInverted(True)

        
##        # Configure shooter motor controller.
##         # Create a CANTalon object.
##        self.l_motor.setFeedbackDevice(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder)
##        self.r_motor.setFeedbackDevice(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder)# Choose an encoder as a feedback device.  The default should be QuadEncoder already, but might as well make sure.
##        # I thought the encoder was 20 pulses per revolution per phase, which would require "80" as an argument below, but after trying it, it looks like there are 12.
##        # Setting this parameter changes things so getPosition() returns decimal revolutions, and getSpeed() returns RPM.
##        # resets shooter position on startup
##        self.l_motor.setPosition(0)
##        self.r_motor.setPosition(0)
        
        #self.stick = wpilib.Joystick(0)
        self.l_joy = wpilib.Joystick(0)
        self.r_joy = wpilib.Joystick(1)
        #self.l_loader = ctre.wpi_talonsrx.WPI_TalonSRX(5)
        #self.r_loader = ctre.wpi_talonsrx.WPI_TalonSRX(6)
        #self.l_chute = wpilib.Spark(0)
        #self.r_chute = wpilib.Spark(1)
        #self.climb = wpilib.Spark(2)
        self.left = wpilib.SpeedControllerGroup(self.l_motorFront, self.l_motorBack)
        self.right = wpilib.SpeedControllerGroup(self.r_motorFront, self.r_motorBack)
        self.drive = DifferentialDrive(self.left, self.right)
        self.counter = 0
        #wpilib.CameraServer.launch()
        #IP for camera server: http://10.38.81.101:1181/
        

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        
##        self.auto_loop_counter = 0
##        self.shooter.setPosition(0)
##        self.l_motor.setPosition(0)
##        self.r_motor.setPosition(0)
##        self.l_motor.enableBrakeMode(True)
##        self.r_motor.enableBrakeMode(True)
        
        pass
       

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        
##        if self.r_motor.getPosition()> -4000 and self.auto_loop_counter <800:
##            self.drive.drive(-1,0)
##
##        else:
##            self.drive.drive(0,0)
##        
##        self.auto_loop_counter +=1
##
##        if self.auto_loop_counter % 50 == 0:
##            # Uncomment whichever line you want to use.  Need to have a shooter to use the second one.
##            print(self.auto_loop_counter, ' pos: ', self.l_motor.getPosition() , self.r_motor.getPosition())
##        #This counter runs 50 times a second
        
        pass
       
    def teleopInit(self):
        
##        #resets printed shooter position on enable
##        self.shooter.setPosition(0)
##        self.l_motor.setPosition(0)
##        self.r_motor.setPosition(0)
##        self.auto_loop_counter = 0
        
        self.l_motorFront.enableBrakeMode(False)
        self.l_motorBack.enableBrakeMode(False)

        self.r_motorFront.enableBrakeMode(False)
        self.r_motorBack.enableBrakeMode(False)
        

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        
        self.drive.tankDrive(self.l_joy.getRawAxis(1) , self.r_joy.getRawAxis(1))

        
        #Right Joystick Intake for Loader and Chute
        if self.r_joy.getRawButton(3):
            self.l_loader.set(1) 
            self.l_chute.set(1)
            self.r_loader.set(1)
            self.r_chute.set(1)
        else:
            self.l_loader.set(0) 
            self.l_chute.set(0)
            self.r_loader.set(0)
            self.r_chute.set(0)

    
        #Left Joystick Outtake for Loader and Chute
        if self.l_joy.getRawButton(3):
            self.l_loader.set(-1) 
            self.l_chute.set(-1)
            self.r_loader.set(-1)
            self.r_chute.set(-1)
        else:
            self.l_loader.set(0)
            self.l_chute.set(0)
            self.r_loader.set(0)
            self.r_chute.set(0)
            
            
        #Right Joystick Climb Up, Left Joystick Climb Down
        if self.r_joy.getRawButton(2):
            self.climb.set(1)
        else:
            self.climb.set(0)

        if self.l_joy.getRawButton(2):
            self.climb.set(-1)
        else:
            self.climb.set(0)
        
       
        
##        self.auto_loop_counter +=1
##
##        
##        self.counter += 1
##        if self.counter % 90 == 0:
##            # Uncomment whichever line you want to use.  Need to have a shooter to use the second one.
##            print(self.counter, ' pos: ', self.l_motor.getPosition() , self.r_motor.getPosition())
##            
##
##            
##            print(self.counter)
##            print(self.counter, ' axis: ', self.l_joy.getRawAxis(2) and self.r_joy.getRawAxis(2), ' pos: ', self.shooter.getPosition(), ' rpm: ', self.shooter.getSpeed())
            
        
    def testPeriodic(self):
        """This function is called periodically during test mode."""
        #wpilib.LiveWindow.run()
        pass
        


if __name__ == "__main__":
    wpilib.run(MyRobot)
