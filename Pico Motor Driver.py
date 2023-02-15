try:
 import usocket as socket        #importing socket
except:
 import socket
import network            #importing network
import gc
import machine
from time import sleep
from machine import Pin, PWM
#machine.reset() DO NOT USE THIS COMMAND, IT WILL BRICK YOUR PICO


#Network credentials
gc.collect()
ssid = 'WCRL test'                  #Set access point name 
password = '12345678'      #Set your access point password


#Pin definitions
led = machine.Pin("LED",machine.Pin.OUT) #define onboard LED
ina1 = Pin(18, Pin.OUT) #AIN1 as GPIO18
ina2 = Pin(17, Pin.OUT) #AIN2 as GPIO17
inb1 = Pin(19, Pin.OUT) #BIN1 as GPIO19
inb2 = Pin(20, Pin.OUT) #BIN1 as GPIO20
pwma = PWM(Pin(16))     #PWMA as GPIO16
pwmb = PWM(Pin(15))     #PWMB as GPIO15
esc = PWM(Pin(11))      #ESC as GPIO11


#ESC/PWM calibration
frequency = float(50) 
esc.freq(int(frequency))  #set frequency of ESC
esc.duty_u16(3901) #ESC calibration value 1
esc.duty_u16(4031) #ESC calibration value 2

pwma.freq(1500)  #Set PWWA frequency for motors
pwmb.freq(1500)  #Set PWMB frequency for motors


# define function for PWM generation
def pwmGenerate(duty):
    #esc_duty_cycle = float(6.2)
    esc_duty_cycle = int( duty * 65025 / 100  )
    esc.duty_u16(esc_duty_cycle)

def forward(duty):  #Move motors forward at specified duty cycle
    ina1.value(1)
    ina2.value(0)
    inb1.value(0)
    inb2.value(1)
    duty_16 = int((duty*65536)/100)
    pwma.duty_u16(duty_16)
    pwmb.duty_u16(duty_16)

def reverse(duty):  #Move motors reverse at specified duty cycle
    ina1.value(0)
    ina2.value(1)
    inb1.value(1)
    inb2.value(0)
    duty_16 = int((duty*65536)/100)
    pwma.duty_u16(duty_16)
    pwmb.duty_u16(duty_16)
    
def turnLeft(duty):  #Turn left at specified duty cycle
    ina1.value(1)
    ina2.value(0)
    inb1.value(1)
    inb2.value(0)
    duty_16 = int((duty*65536)/100)
    pwma.duty_u16(duty_16)
    pwmb.duty_u16(duty_16)

def turnRight(duty):  #Turn right at specified duty cycle
    ina1.value(0)
    ina2.value(1)
    inb1.value(0)
    inb2.value(1)
    duty_16 = int((duty*65536)/100)
    pwma.duty_u16(duty_16)
    pwmb.duty_u16(duty_16)

def StopMotor():   #Stop all motors
    ina1.value(0)
    ina2.value(0)
    pwma.duty_u16(0)
    pwmb.duty_u16(0)


#Soft access point generator
ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)            #activating

while ap.active() == False:
  pass
print('Connection is successful')
print(ap.ifconfig())

##UI with 5 buttons: forward, reverse, left, right and ESC control
##Currently only supports mouse release commands
def web_page():
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>WCRL Test</title>
            </head>
            <center><b>
            <form action="./forward">
            <input type="submit" value="Forward" style="height:120px; width:120px" />
            </form>
            <table><tr>
            <td><form action="./left">
            <input type="submit" value="Left" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./ESC">
            <input type="submit" value="ESC" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./right">
            <input type="submit" value="Right" style="height:120px; width:120px" />
            </form></td>
            </tr></table>
            <form action="./back">
            <input type="submit" value="Back" style="height:120px; width:120px" />
            </form>
            <form action="./stop">
            <input type="submit" value="Stop" style="height:120px; width:120px" />
            </form>
            </body>
            </html>
            """
    return str(html)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
s.bind(('', 80))
s.listen(5)


# while True:
#   conn, addr = s.accept()
#   print('Got a connection from %s' % str(addr))
#   request = conn.recv(1024)
#   print('Content = %s' % str(request))
#   response = web_page()
#   conn.send(response)
#   conn.close()
  
led.on() #toggle led on

#Start web server
while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    request = str(request)
    try:
        request = request.split()[1]
    except IndexError:
        pass
        
    if request == '/forward?':
        forward(20)
        sleep(1)
        StopMotor()
    elif request =='/left?':
        turnLeft(20)
        sleep(1)
        StopMotor()
    elif request =='/ESC?':
        pwmGenerate(6.3)
        sleep(1)
        pwmGenerate(6.2)
    elif request =='/right?':
        turnRight(20)
        sleep(1)
        StopMotor()
    elif request =='/back?':
        reverse(20)
        sleep(1)
        StopMotor()
    elif request =='\stop?':
        StopMotor()
    response = web_page()
    conn.send(response)
    conn.close()
    print('Got a connection from %s' % str(addr))