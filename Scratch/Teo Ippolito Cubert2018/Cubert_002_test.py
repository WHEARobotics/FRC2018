#!/usr/bin/env python3
"""
    WHEA Robotics 3881 code for FRC 2018.
#test
"""

import wpilib
import wpilib.drive  # Add this import.
import ctre

class MyRobot(wpilib.IterativeRobot):
    
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """

        """
        Button Map for Dual Joysticks:
        1: Climber
        2: Shooter/Loader (Intake)
        3: Shooter/Loader (Outtake)
        """
        
        # Configure shooter motor controller.
        # For 2018, the class names have changed from CANTalon to this:
        self.shooter = ctre.wpi_talonsrx.WPI_TalonSRX(3) # Create a WPI_TalonSRX object with CAN device number = 3.

        # Configure the sensor.
        # In 2017, it was "setFeedbackDevice", but in 2018 it is configSelectedFeedbackSensor, and the parameters are different, too.
        # Note that when I try to simulate with the quadrature encoders, I get a "NotImplementedError".
        # This would be the Python implementation lagging the C++ implementation--the guy can't do everything.
        # We can comment this line out (and others like it) for simulation.
        self.shooter.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0) # Choose an encoder as a feedback device.

        # We may need the following line to change the phase of the sensor so that increasing sensor positions correspond to positive drive on the motor.
        # True or False, we'll test when we have the robot together.
        #self.shooter.setSensorPhase(True)

        # The encoder is 12 pulses per revolution per phase.
        # Delete the lines where we configure the encoder codes per revolution, as this year's functions report pulses, not revolutions.
        # self.shooter.getSelectedSensorPosition(0) # Gets the raw sensor units of the sensor selected for closed loop control.
        # self.shooter.getSelectedSensorVelocity(0)  # Gets the velocity (pulses per 100msec) of the sensor selected for closed loop control.
        # self.shooter.getQuadraturePosition() # Gets the quadrature encoder position, regardless of whether it is used for closed loop control.
        # self.shooter.getQuadratureVelocity() # Gets the quadrature encoder velocity (pulses per 100msec), regardless of whether it is used for feedback.

        # Resets shooter encoder position on startup.
        # In 2017, the function was "setPosition".  For 2018, it is "setQuadraturePosition"
        # First parameter is position, second is timeout.
        # Found in (robotpy.readthedocs.io, CTRE libraries, TalonSRX section)
        self.shooter.setQuadraturePosition(0, 0)

        # Changing the motor controller between brake and coast modes when we give it a neutral (zero) input.
        # For 2017, the function was "enableBrakeMode"; for 2018 it is "setNeutralMode".
        # Substitute "Brake" for "Coast" below if desired.
        # Found in the robotpy.readthedocs.io page, and also the CTRE documentation:
        # https://github.com/CrossTheRoadElec/Phoenix-Documentation/blob/master/README.md#installing-phoenix-framework-onto-your-frc-robot
        self.shooter.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        

        self.l_motor = ctre.wpi_talonsrx.WPI_TalonSRX(1)
        self.l_motor.setInverted(True)
        self.r_motor = ctre.wpi_talonsrx.WPI_TalonSRX(2)
        self.r_motor.setInverted(True)
        # Configure shooter motor controller.
        # Create a CANTalon object.
        self.l_motor.setFeedbackDevice(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder)
        self.r_motor.setFeedbackDevice(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder)# Choose an encoder as a feedback device.  The default should be QuadEncoder already, but might as well make sure.
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

        # In 2017, there was a RobotDrive class.  It is still around, but not recommended for new designs.
        # In 2018, the class we want is wpilib.drive.DifferentialDrive.
        # Note that for a 4-motor drive train, we'll have to do something a little different.
        # (old) self.drive = wpilib.RobotDrive(self.l_motor , self.r_motor)
        self.drive = wpilib.drive.DifferentialDrive(self.l_motor , self.r_motor)


        self.counter = 0
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
       

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""


        # Note that for 2018, we'll want to use self.drive.arcadeDrive() or self.drive.curvatureDrive()
        # in autonomous.  I suspect the latter one.
        if self.r_motor.getPosition()> -4000 and self.auto_loop_counter <800:
            self.drive.drive(-1,0)

        else:
            self.drive.drive(0,0)
        
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
        self.auto_loop_counter = 0
        self.l_motor.enableBrakeMode(False)
        self.r_motor.enableBrakeMode(False)
        

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



