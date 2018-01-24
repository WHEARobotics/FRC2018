#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
import wpilib.drive


class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        # Comments begin with a "#".  I will be making liberal use of comments.
        #
        # These initializations won't do anything on our robot at the moment, but won't
        # hinder a simulation.
        # Sparks are motor controllers. The Spark class in the library contains code to talk to them.
        # "self" refers to the object being defined by this class, or in other words our robot.
        # This is saying that the variable "left_motor" is part of the class's definition and
        # is accessible from any function in the class.
        self.left_motor = wpilib.Spark(0)  # Create an object of the Spark class on PWM channel 0 and call it left_motor.
        self.right_motor = wpilib.Spark(1) # Create another object of the Spark class.
        # An object of the class DifferentialDrive helps us to control a drive train with all left wheels connected
        # and all right wheels connected, similar to a Bobcat skid-steer or a bulldozer.
        self.drive = wpilib.drive.DifferentialDrive(self.left_motor, self.right_motor)
        self.stick = wpilib.Joystick(1)    # Joystick is a class that talks to the joysticks connected to the driver station computer.
        # Timer to control periodic logging of messages.
        self.print_timer = wpilib.Timer()
        self.print_timer.start()
        # Another timer, this one to help us measure time during play modes.
        self.play_timer = wpilib.Timer()
        self.play_timer.start()        

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.play_timer.reset() # Reset play timer so we can time things in autonomous.


    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""

        # Drive for two seconds
        # The DifferentialDrive class (remember, that's what self.drive is)
        # has functions/methods made to ease control from a single joystick: arcadeDrive(),
        # znd another that is good if you have left and right joysticks is tankDrive()
        if self.play_timer.get() < 2.0:
            self.drive.arcadeDrive(-0.5, 0)  # Drive forwards at half speed
        else:
            self.drive.arcadeDrive(0, 0)  # Stop robot

    def teleopInit(self):
        """This function is run once when the robot enters teleop mode."""
        # Reset the timers.
        self.play_timer.reset()  # Play timer so we have time from the beginning of teleop.
        self.print_timer.reset() # Print timer so we can send info to the logger periodically from the beginning of teleop.


    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.drive.arcadeDrive(self.stick.getY(), self.stick.getX())

        # Send something to the log every 2 seconds.
        if self.print_timer.hasPeriodPassed(2.0):
            # Note that hasPeriodPassed() resets the timer in question.  
            # That's why we are using two timers and sending the play timer to the log.
            # The strange syntax: 'a string {0:.2f}'.format(variable) substitutes the value
            # of variable into the spot between the {}, and formats it with 2 decimal places.
            self.logger.info('tick {0:.2f}'.format(self.play_timer.get()))
        

        


if __name__ == "__main__":
    wpilib.run(MyRobot)
