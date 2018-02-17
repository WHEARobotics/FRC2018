#import robotpy
import wpilib
import ctre
import wpilib.drive
import time
import os
from threading import Thread
from timeit import default_timer

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
        #self.Gyro = wpilib.ADXRS450_Gyro()
        self.Chute_l = ctre.wpi_talonsrx.WPI_TalonSRX(4)
        self.Chute_r = ctre.wpi_talonsrx.WPI_TalonSRX(5)# Create a CANTalon object.
         # Choose an encoder as a feedback device.  The default should be QuadEncoder already, but might as well make sure.
        # I thought the encoder was 20 pulses per revolution per phase, which would require "80" as an argument below, but after trying it, it looks like there are 12.
        # Setting this parameter changes things so getPosition() returns decimal revolutions, and getSpeed() returns RPM.
        #self.shooter.configEncoderCodesPerRev(48)
        # resets shooter position on startup
        #self.unloader.setQuadraturePosition(0, 0)
        #self.unloader.setNeutralMode(ctre.wpilib.Spark.NeutralMode.Coast)# This should change between brake and coast modes.
        

        self.l_motor1 = ctre.wpi_talonsrx.WPI_TalonSRX(3)
        self.l_motor2 = ctre.wpi_talonsrx.WPI_TalonSRX(2) 
        self.l_motor1.setInverted(False)
        self.l_motor2.setInverted(False)
        self.r_motor1 = ctre.wpi_talonsrx.WPI_TalonSRX(0)
        self.r_motor2 = ctre.wpi_talonsrx.WPI_TalonSRX(1)
        self.r_motor1.setInverted(False)
        self.r_motor2.setInverted(False)
        # Configure shooter motor controller.
         # Create a CANTalon object.
        self.l_motor1.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        #self.l_motor1.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)
        self.l_motor2.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        self.l_motor1.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        #self.r_motor1.configSelectedFeedbackSensor(ctre.wpi_talonsrx.WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)
        self.l_motor2.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)
        # Choose an encoder as a feedback device.  The default should be QuadEncoder already, but might as well make sure.
        # I thought the encoder was 20 pulses per revolution per phase, which would require "80" as an argument below, but after trying it, it looks like there are 12.
        # Setting this parameter changes things so getPosition() returns decimal revolutions, and getSpeed() returns RPM.
        #self.l_motor1.configEncoderCodesPerRev(48)
        #self.l_motor2.configEncoderCodesPerRev(48)
        #self.r_motor1.configEncoderCodesPerRev(48)
        #self.r_motor2.configEncoderCodesPerRev(48)
        # resets shooter position on startup
        self.l_motor1.setQuadraturePosition(0, 0)
        self.r_motor1.setQuadraturePosition(0, 0)


        #self.stick = wpilib.Joystick(0)
        self.l_joy = wpilib.Joystick(0)
        self.r_joy = wpilib.Joystick(1)
        self.loader_l = wpilib.Spark(1)
        self.loader_r = wpilib.Spark(0)
        self.climber = wpilib.Spark(3)
        self.left = wpilib.SpeedControllerGroup(self.l_motor1, self.l_motor2)
        self.right = wpilib.SpeedControllerGroup(self.r_motor1, self.r_motor2)
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)
        self.accelerometer = wpilib.BuiltInAccelerometer(wpilib.BuiltInAccelerometer.Range.k2G)
        self.vel = 0
        self.pos = 0
        self.grav = 9.82
        self.counter = 0
        #wpilib.CameraServer.launch()
        #IP for camera server: http://10.38.81.101:1181/

    def autonomousInit(self):
        self.auto_loop_counter = 0
        self.l_motor1.setQuadraturePosition(0, 0)
        self.r_motor1.setQuadraturePosition(0, 0)
        self.l_motor1.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake)
        self.r_motor1.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake)
        self.l_motor2.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake)
        self.r_motor2.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake)
        #self.Gyro.reset()
        
        self.gameData = wpilib.DriverStation.getInstance().getGameSpecificMessage()
        if not self.gameData:
            self.gameData = 'LLL'
            msg = 'Empty Game Specific Message,Setting It To [0]'.format(self.gameData)
            self.logger.warn(msg)
            
        self.start = default_timer()


		
    

    def autonomousPeriodic(self):
       # print (self.vel = self.vel + self.grav * self.accelerometer.getX()) 
        if(self.gameData[0] == 'L'):    	
            self.AutoPL()
            
        else: 
            self.AutoPR()
            

    def AutoPL(self):
        time = default_timer() - self.start
        if self.l_motor1.getQuadraturePosition() >= -1300:
        #if self.r_motor1.getQuadraturePosition()> -2000 and self.auto_loop_counter <30:
            self.drive.curvatureDrive(0.5,0,False)
            print ('secs: ',time)
            print ('Pos L: ',self.l_motor1.getQuadraturePosition())
            print ('Pos R: ',self.r_motor1.getQuadraturePosition())

        else:
            self.drive.curvatureDrive(0.0,0,False)
            

       

        self.auto_loop_counter +=1

        #if self.auto_loop_counter % 50 == 0:
            # Uncomment whichever line you want to use.  Need to have a shooter to use the second one.
            #print(self.auto_loop_counter, ' pos: ', self.Gyro.getAngle() , self.Gyro.getRate())
            #This counter runs 50 times a second

    def AutoPR(self):
        time = default_timer() - start
        if self.l_motor1.getQuadraturePosition() >= -1300:
        #if self.r_motor1.getQuadraturePosition()> -2000 and self.auto_loop_counter <30:
            self.drive.curvatureDrive(0.5,0,False)
            print ('secs: ',time)
            print ('Pos R: ',self.r_motor1.getQuadraturePosition())
            print ('Pos L: ',self.l_motor1.getQuadraturePosition())

        else:
            self.drive.curvatureDrive(0.0,0,False)
            

        self.auto_loop_counter +=1



    def teleopInit(self):
        
        self.l_motor1.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake) 
        self.l_motor2.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake)

        self.r_motor1.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake) 
        self.r_motor2.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake)

        self.l_motor1.setQuadraturePosition(0, 0)
        self.r_motor1.setQuadraturePosition(0, 0)

    def teleopPeriodic(self):  
        self.drive.tankDrive(self.l_joy.getRawAxis(1) , self.r_joy.getRawAxis(1))
##        msg = 'Acceleration of X + Y + Z Axes {0: 7.4f} {1: 7.4f} {2: 7.4f}'.format(self.accelerometer.getX() , self.accelerometer.getY() , self.accelerometer.getZ())
##        self.logger.info(msg)
        self.counter += 1
        if self.counter % 50 == 0:
            msg = 'Getting Posistion of Left & Right {0} {1}'.format(self.l_motor1.getQuadraturePosition() , self.r_motor1.getQuadraturePosition())
            self.logger.info(msg)



        
        
if __name__ == "__main__":
    wpilib.run(MyRobot)

        
    
