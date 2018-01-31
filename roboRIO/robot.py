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
    
        #Here is the encoder setup for the 4 motor drivetrain
        self.l_motorFront = ctre.wpi_talonsrx.WPI_TalonSRX(0)
        self.l_motorFront.setInverted(False)

        self.l_motorBack = ctre.wpi_talonsrx.WPI_TalonSRX(1)
        self.l_motorBack.setInverted(False)

        self.r_motorFront = ctre.wpi_talonsrx.WPI_TalonSRX(2)
        self.r_motorFront.setInverted(False)
        
        self.r_motorBack = ctre.wpi_talonsrx.WPI_TalonSRX(3)
        self.r_motorBack.setInverted(False)

        self.l_motorFront.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast) 
        self.l_motorBack.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.r_motorFront.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast) 
        self.r_motorBack.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.l_motorFront.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)
        self.l_motorBack.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)

        self.r_motorFront.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)
        self.r_motorBack.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)

        self.l_motorFront.setQuadraturePosition(0, 0)
        self.l_motorBack.setQuadraturePosition(0, 0)

        self.r_motorFront.setQuadraturePosition(0, 0)
        self.l_motorBack.setQuadraturePosition(0, 0)


        #Here is the encoder setup for the left and right chute motors
        self.l_chute = ctre.wpi_talonsrx.WPI_TalonSRX(5)
        self.l_chute.setInverted(False)
        self.r_chute = ctre.wpi_talonsrx.WPI_TalonSRX(6)
        self.r_chute.setInverted(False)

        self.l_chute.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        self.r_chute.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.l_chute.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)
        self.r_chute.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)

        self.l_chute.setQuadraturePosition(0, 0)
        self.r_chute.setQuadraturePosition(0, 0)

        
        #This is the setup for the drive groups and loaders
        self.l_joy = wpilib.Joystick(0)
        self.r_joy = wpilib.Joystick(1)
        self.l_loader = wpilib.Spark(0)
        self.r_loader = wpilib.Spark(1)
        #self.climb = wpilib.Spark(2)
        self.left = wpilib.SpeedControllerGroup(self.l_motorFront, self.l_motorBack)
        self.right = wpilib.SpeedControllerGroup(self.r_motorFront, self.r_motorBack)
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)
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
        
        self.l_motorFront.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast) 
        self.l_motorBack.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.r_motorFront.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast) 
        self.r_motorBack.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.l_chute.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        self.r_chute.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.l_motorFront.setQuadraturePosition(0, 0)
        self.l_motorBack.setQuadraturePosition(0, 0)

        self.r_motorFront.setQuadraturePosition(0, 0)
        self.l_motorBack.setQuadraturePosition(0, 0)

        self.l_chute.setQuadraturePosition(0, 0)
        self.r_chute.setQuadraturePosition(0, 0)

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
##            
##            
##        #Right Joystick Climb Up, Left Joystick Climb Down
##        if self.r_joy.getRawButton(2):
##            self.climb.set(1)
##        else:
##            self.climb.set(0)
##
##        if self.l_joy.getRawButton(2):
##            self.climb.set(-1)
##        else:
##            self.climb.set(0)
        
       
        
##        self.auto_loop_counter +=1

        self.counter += 1
        if self.counter % 90 == 0:
            # Uncomment whichever line you want to use.  Need to have a shooter to use the second one.
            print(self.counter, ' pos: ', self.l_motorFront.getQuadraturePosition() , self.r_motorFront.getQuadraturePosition())
            

            """
            print(self.counter)
            """
            print(self.counter, ' axis: ', self.l_joy.getRawAxis(1) and self.r_joy.getRawAxis(1), ' pos: ', self.l_chute.getQuadraturePosition(), ' rpm: ', self.l_chute.getQuadratureVelocity(),' pos: ', self.r_chute.getQuadraturePosition(), ' rpm: ', self.r_chute.getQuadratureVelocity())
        
            
        
    def testPeriodic(self):
        """This function is called periodically during test mode."""
        #wpilib.LiveWindow.run()
        pass
        


if __name__ == "__main__":
    wpilib.run(MyRobot)
