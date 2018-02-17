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
        Button Map for Dual Joysticks
        Left Joystick (Intake):
        1. Chute + Loader (100%)
        2. Climb Up
        3. Chute + Loader (50%)
        4. Loader (50%)
        5. Chute (50%)

        Right Joystick (Outtake):
        1. Chute + Loader (-100%)
        2. Climb Down
        3. Chute + Loader (-50%)
        4. Loader (-50%)
        5. Chute (-50%)
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

##        self.l_motorFront.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)
##        self.r_motorFront.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)

        self.l_motorFront.setQuadraturePosition(0, 0)
        self.r_motorFront.setQuadraturePosition(0, 0)
        


        #Here is the encoder setup for the left and right chute motors
        self.l_chute = ctre.wpi_talonsrx.WPI_TalonSRX(5)
        self.l_chute.setInverted(False)
        self.r_chute = ctre.wpi_talonsrx.WPI_TalonSRX(6)
        self.r_chute.setInverted(False)

        self.l_chute.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        self.r_chute.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

##        self.l_chute.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)
##        self.r_chute.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)

        self.l_chute.setQuadraturePosition(0, 0)
        self.r_chute.setQuadraturePosition(0, 0)

        
        #This is the setup for the drive groups and loaders
        self.l_joy = wpilib.Joystick(0)
        self.r_joy = wpilib.Joystick(1)
        self.l_loader = wpilib.Spark(0)
        self.r_loader = wpilib.Spark(1)
        self.climb = wpilib.Spark(2)
        self.left = wpilib.SpeedControllerGroup(self.l_motorFront, self.l_motorBack)
        self.right = wpilib.SpeedControllerGroup(self.r_motorFront, self.r_motorBack)
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)

##        self.xbox = wpilib.XboxController(0)
##        self.accelerometer = wpilib.BuiltInAccelerometer(wpilib.BuiltInAccelerometer.Range.k2G)
##        self.vel = 0
##        self.pos = 0
##        self.grav = 9.82
##        self.counter = 0
##        wpilib.CameraServer.launch()
##        IP for camera server: http://10.38.81.101:1181/
        

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.l_motorFront.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast) 
        self.l_motorBack.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.r_motorFront.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast) 
        self.r_motorBack.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.l_chute.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        self.r_chute.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.l_motorFront.setQuadraturePosition(0, 0)
        self.r_motorFront.setQuadraturePosition(0, 0)

        self.l_chute.setQuadraturePosition(0, 0)
        self.r_chute.setQuadraturePosition(0, 0)

##        self.Gyro.reset()

        self.gameData = wpilib.DriverStation.getInstance().getGameSpecificMessage()
        if not self.gameData:
            self.gameData = 'LLL'
            msg = 'Empty Game Specific Message,Setting It To [0]'.format(self.gameData)
            self.logger.warn(msg)
            
        self.start = default_timer()

        
    
       

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
##        print (self.vel = self.vel + self.grav * self.accelerometer.getX()) 
        if(self.gameData[0] == 'L'):    	
            self.AutoPL()
            
        else: 
            self.AutoPR()


    def AutoPL(self):
        time = default_timer() - self.start
        if self.l_motorFront.getQuadraturePosition() >= -1300:
            self.drive.curvatureDrive(0.5,0,False)
            print ('secs: ',time)
            print ('Pos L: ',self.l_motorFront.getQuadraturePosition())
            print ('Pos R: ',self.r_motorFront.getQuadraturePosition())

        else:
            self.drive.curvatureDrive(0.0,0,False)
            

##        if self.auto_loop_counter % 50 == 0:
##            print(self.auto_loop_counter, ' pos: ', self.Gyro.getAngle() , self.Gyro.getRate())

        self.auto_loop_counter +=1

        
    def AutoPR(self):
        time = default_timer() - start
        if self.l_motorFront.getQuadraturePosition() >= -1300:
            self.drive.curvatureDrive(0.5,0,False)
            print ('secs: ',time)
            print ('Pos R: ',self.r_motor1.getQuadraturePosition())
            print ('Pos L: ',self.l_motor1.getQuadraturePosition())

        else:
            self.drive.curvatureDrive(0.0,0,False)
            

        self.auto_loop_counter +=1

        
     
       
    def teleopInit(self):
        """This function is run once each time the robot enters operator control mode."""
        self.l_motorFront.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast) 
        self.l_motorBack.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.r_motorFront.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast) 
        self.r_motorBack.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.l_chute.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        self.r_chute.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.l_motorFront.setQuadraturePosition(0, 0)
        self.r_motorFront.setQuadraturePosition(0, 0)

        self.l_chute.setQuadraturePosition(0, 0)
        self.r_chute.setQuadraturePosition(0, 0)

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        
        self.drive.tankDrive(self.l_joy.getRawAxis(1) , self.r_joy.getRawAxis(1))
        #self.tankDrive = (self.xbox.getRawAxis(5) , self.xbox.getRawAxis(1))
        
        #Right Joystick Intake for Loader and Chute(Ground Pickup)
        if self.r_joy.getRawButton(1):
            self.l_loader.set(1) 
            self.l_chute.set(1)
            self.r_loader.set(1)
            self.r_chute.set(1)
        else:
            self.l_loader.set(0) 
            self.l_chute.set(0)
            self.r_loader.set(0)
            self.r_chute.set(0)

    
        #Left Joystick Outtake for Loader and Chute(Ground Pickup)
        if self.l_joy.getRawButton(1):
            self.l_loader.set(-1) 
            self.l_chute.set(-1)
            self.r_loader.set(-1)
            self.r_chute.set(-1)
        else:
            self.l_loader.set(0)
            self.l_chute.set(0)
            self.r_loader.set(0)
            self.r_chute.set(0)


        #Right Joystick Intake for Chute(Transfer Pickup)
        if self.r_joy.getRawButton(4):
            self.l_chute.set(1)
            self.r_chute.set(1)
        else:
            self.l_chute.set(0)
            self.r_chute.set(0)

    
        #Left Joystick Outtake for Chute(Transfer Pickup)
        if self.l_joy.getRawButton(4):
            self.l_chute.set(-1)
            self.r_chute.set(-1)
        else:
            self.l_chute.set(0)
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
        
       
        
        self.auto_loop_counter +=1

        self.counter += 1

        if self.counter % 50 == 0:
            msg = 'Posistion of Left & Right Drive Motors{0} {1}'.format(self.l_motorFront.getQuadraturePosition() , self.r_motorFront.getQuadraturePosition())
            msg = 'Velocity of Left & Right Drive Motors{0} {1}'.format(self.l_motorFront.getQuadratureVelocity() , self.r_motorFront.getQuadratureVelocity())

            msg = 'Posistion of Left & Right Chute Motors{0} {1}'.format(self.l_chute.getQuadraturePosition() , self.r_chute.getQuadraturePosition())
            msg = 'Velocity of Left & Right Chute Motors{0} {1}'.format(self.l_chute.getQuadratureVelocity() , self.r_chute.getQuadratureVelocity())
            self.logger.info(msg)

##          msg = 'Acceleration of X + Y + Z Axes {0: 7.4f} {1: 7.4f} {2: 7.4f}'.format(self.accelerometer.getX() , self.accelerometer.getY() , self.accelerometer.getZ())
##          self.logger.info(msg)



if __name__ == "__main__":
    wpilib.run(MyRobot)
