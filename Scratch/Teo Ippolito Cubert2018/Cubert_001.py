#!/usr/bin/env python3
"""
    WHEA Robotics 3881 code for FRC 2017.
#test
"""
#import robotpy
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
        1. Chute
        2. Loader
        3. Climber
        """
        
        # Configure shooter motor controller.
        self.Gyro = wpilib.ADXRS450_Gyro()
        self.Chute = ctre.wpi_talonsrx.WPI_TalonSRX(7)
        self.Chute = ctre.wpi_talonsrx.WPI_TalonSRX(8)# Create a CANTalon object.
        self.Chute.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0 , 0) # Choose an encoder as a feedback device.  The default should be QuadEncoder already, but might as well make sure.
        # I thought the encoder was 20 pulses per revolution per phase, which would require "80" as an argument below, but after trying it, it looks like there are 12.
        # Setting this parameter changes things so getPosition() returns decimal revolutions, and getSpeed() returns RPM.
        #self.shooter.configEncoderCodesPerRev(48)
        # resets shooter position on startup
        #self.unloader.setQuadraturePosition(0, 0)
        #self.unloader.setNeutralMode(ctre.wpilib.Spark.NeutralMode.Coast)# This should change between brake and coast modes.
        

        self.l_motor1 = ctre.wpi_talonsrx.WPI_TalonSRX(0)
        self.l_motor2 = ctre.wpi_talonsrx.WPI_TalonSRX(1) 
        self.l_motor1.setInverted(False)
        self.l_motor2.setInverted(False)
        self.r_motor1 = ctre.wpi_talonsrx.WPI_TalonSRX(2)
        self.r_motor2 = ctre.wpi_talonsrx.WPI_TalonSRX(3)
        self.r_motor1.setInverted(False)
        self.r_motor2.setInverted(False)
        # Configure shooter motor controller.
         # Create a CANTalon object.
        self.l_motor1.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        self.l_motor1.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)
        self.l_motor2.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        self.l_motor2.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)
        self.l_motor1.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        self.r_motor1.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)
        self.l_motor2.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        self.r_motor2.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)# Choose an encoder as a feedback device.  The default should be QuadEncoder already, but might as well make sure.
        # I thought the encoder was 20 pulses per revolution per phase, which would require "80" as an argument below, but after trying it, it looks like there are 12.
        # Setting this parameter changes things so getPosition() returns decimal revolutions, and getSpeed() returns RPM.
        #self.l_motor1.configEncoderCodesPerRev(48)
        #self.l_motor2.configEncoderCodesPerRev(48)
        #self.r_motor1.configEncoderCodesPerRev(48)
        #self.r_motor2.configEncoderCodesPerRev(48)
        # resets shooter position on startup
        self.l_motor1.setQuadraturePosition(0, 0)
        self.l_motor2.setQuadraturePosition(0, 0)
        self.r_motor1.setQuadraturePosition(0, 0)
        self.r_motor2.setQuadraturePosition(0, 0)

        #self.stick = wpilib.Joystick(0)
        self.l_joy = wpilib.Joystick(0)
        self.r_joy = wpilib.Joystick(1)
        self.loader = ctre.wpi_talonsrx.WPI_TalonSRX(4)
        self.climber = wpilib.Spark(6)
        self.loader = ctre.wpi_talonsrx.WPI_TalonSRX(5)
        self.drive = wpilib.RobotDrive(self.l_motor1 , self.l_motor2 , self.r_motor1 , self.r_motor2)
        self.counter = 0
        self.mode = 0
        #wpilib.CameraServer.launch()
        #IP for camera server: http://10.38.81.101:1181/
        
        
        

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.auto_loop_counter = 0
        self.l_motor1.setQuadraturePosition(0, 0)
        self.r_motor1.setQuadraturePosition(0, 0)
        self.l_motor1.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake)
        self.r_motor1.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake)
        self.l_motor2.setQuadraturePosition(0, 0)
        self.r_motor2.setQuadraturePosition(0, 0)
        self.l_motor2.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake)
        self.r_motor2.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake)
        self.Gyro.reset()
        
        self.gameData = wpilib.DriverStation.getInstance().getGameSpecificMessage()
        if not self.gameData:
            self.gameData = 'LLL'
            msg = 'Empty Game Specific Message,Setting It To [0]'.format(self.gameData)
            self.logger.warn(msg)


		
    

    def autonomousPeriodic(self):
        
        if(self.gameData[0] == 'L'):    	
            self.AutoPL()
            
        else: 
            self.AutoPR()

    def AutoPL(self):

        if self.r_motor1.getQuadraturePosition()> -2000 and self.auto_loop_counter <200:
            self.drive.drive(-0.5,0)

        else:
            self.drive.drive(0,0)

        self.auto_loop_counter +=1

        if self.auto_loop_counter % 50 == 0:
            # Uncomment whichever line you want to use.  Need to have a shooter to use the second one.
            print(self.auto_loop_counter, ' pos: ', self.Gyro.getAngle() , self.Gyro.getRate())
        #This counter runs 50 times a second

    def AutoPR(self):
        
        if self.r_motor1.getQuadraturePosition()> -2000 and self.auto_loop_counter <200:
            self.drive.drive(-0.5,0)

        else:
            self.drive.drive(0,0)

        self.auto_loop_counter +=1

        if self.auto_loop_counter % 50 == 0:
            # Uncomment whichever line you want to use.  Need to have a shooter to use the second one.
            print(self.auto_loop_counter, ' pos: ', self.Gyro.getAngle() , self.Gyro.getRate())
        #This counter runs 50 times a second
            
            
            
            


    def teleopInit(self):
        #resets printed shooter position on enable
        #self.unloader.setQuadraturePosition(0, 0)
        self.l_motor1.setQuadraturePosition(0, 0)
        self.r_motor1.setQuadraturePosition(0, 0)
        self.l_motor2.setQuadraturePosition(0, 0)
        self.r_motor2.setQuadraturePosition(0, 0)
        self.tele_counter = 0
        self.auto_loop_counter = 0
        self.l_motor1.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        self.r_motor1.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        self.l_motor2.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        self.r_motor2.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        
        

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        
        self.drive.tankDrive(self.l_joy.getRawAxis(1) , self.r_joy.getRawAxis(1))
        
       # if self.l_joy.getRawButton(4) or self.r_joy.getRawButton(4):
        #    self.climber.set(1)
       # else:
            #self.climber.set(0)

        if self.r_joy.getRawButton(3):
            self.loader.set(1)
            self.Chute.set(1)
        else:
            self.loader.set(0)
            self.Chute.set(0)


        if self.l_joy.getRawButton(3):
            self.loader.set(-1)
            self.Chute.set(-1)
        else:
            self.loader.set(0)
            self.Chute.set(0)

       
       
            


            

        # Now do things based on the value of the counter.
       # if self.auto_loop_counter == 0:
        #    self.Chute.set(0) # If zero, we are stopped.
         #   self.Chute.set(0)
       # elif self.auto_loop_counter > 0 and self.auto_loop_counter <= 100:
        # First two seconds shooter only is on.  Technically, we would only have to set when entering this condition, but this makes it clear.
         #    self.Chute.set(1)
        #else:
        # Executed if self.auto_loop_counter is > 100, or trigger held longer than 2 seconds.
          #   self.Chute.set(1)
           #  self.loader.set(0.5)
        
       # self.auto_loop_counter +=1

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
            print(self.auto_loop_counter, ' pos: ', self.Gyro.getAngle() , self.Gyro.getRate())
            

            """
            print(self.counter)
            """
            print(self.auto_loop_counter, ' pos: ', self.Gyro.getAngle() , self.Gyro.getRate())
            

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()
        


if __name__ == "__main__":
    wpilib.run(MyRobot)
