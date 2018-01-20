#This is some basic code to create modes on a joystick or controller

#def robotInt(self):
self.mode = 0

#def teleopPeriodic(self):
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
