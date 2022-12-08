import network
import socket
from time import sleep
import machine
from machine import Pin, PWM
#from pynput.mouse import Listener


ssid = 'wcrl' #soft access wifi credentials 
password = 'wcrl1234'

led = machine.Pin("LED",machine.Pin.OUT) #define onboard LED
ina1 = Pin(18, Pin.OUT) #AIN1 as GPIO18
ina2 = Pin(17, Pin.OUT) #AIN2 as GPIO17
inb1 = Pin(19, Pin.OUT) #BIN1 as GPIO19
inb2 = Pin(20, Pin.OUT) #BIN1 as GPIO20
pwma = PWM(Pin(16))     #PWMA as GPIO16
pwmb = PWM(Pin(15))     #PWMB as GPIO15
esc = PWM(Pin(11))      #ESC as GPIO11

led.on() #toggle led on

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



#Function to connect Pico to ESP8266 soft access network
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
    
    
#Open ip socket   
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection
    

##UI with 5 buttons: forward, reverse, left, right and ESC control
##Currently only supports mouse release commands. New code testing below
def webpage():
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
            </body>
            </html>
            """
    return str(html)



# ##New code with mouseup and mousedown inputs
# def webpage():
#     #Template HTML
#     html = f"""
#             <!DOCTYPE html>
#             <html>
#             <head>
#             <title>WCRL Test</title>
#             </head>
#             <center><b>
#             <button onmousedown="onDown('forward')" onmouseup="onUp('forward')">Foward</button>
#             <input type="submit" value="Forward" style="height:120px; width:120px" />
#             <table><tr>
#             <td><button onmousedown="onDown('left')" onmouseup="onUp('left')">Left</button></td>
#             <input type="submit" value="Left" style="height:120px; width:120px" />
#             <td><button onmousedown="onDown('esc')" onmouseup="onUp('esc')">ESC</button></td>
#             <input type="submit" value="ESC" style="height:120px; width:120px" />
#             <td><button onmousedown="onDown('right')" onmouseup="onUp('right')">Right</button></td>
#             <input type="submit" value="Right" style="height:120px; width:120px" />
#             </tr></table>
#             <button onmousedown="onDown('back')" onmouseup="onUp('back')">Back</button>
#             <input type="submit" value="Back" style="height:120px; width:120px" />
#             
#             <script>
#                 function onDown(button){
#                 // Make a GET request to /button_down
#                 fetch('/'+button+'_down');
#                 }
# 
#                 function onUp(button) {
#                 // Make a GET request to button_down
#                 //fetch('/'+button+'_down');
#                 }
#             </script>
#             </body>
#             </html>
#             """
#     return str(html)



#Integrate UI with motor and esc functions on button press
def serve(connection, *args):
    #Start web server
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
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
        html = webpage()
        client.send(html)
        client.close()



#Execute code
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
        machine.reset()
        
        
    