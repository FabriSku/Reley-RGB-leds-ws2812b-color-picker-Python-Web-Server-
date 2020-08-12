import socket  ,time  , math , os,urequests   #, serial, pygame
#from pygame.locals import *
#from ntptime import settime
import ntptime
import utime
from sys import exit
#import androidhelper
import json
import ujson
import uselect as select
#from wsgiref.simple_server import make_server
#from pygame import Surface
#import time
#import wsgiref
#pygame.init()
import network , gc 
from machine import I2C, Pin
from machine import RTC
import ssd1306
import socket
import usocket
import machine
import binascii
from machine import Pin, PWM ,ADC
import servo
import socket  ,time  , math , os  #, serial, pygame
#from pygame.locals import *
from sys import exit
#import androidhelper
import json
#from wsgiref.simple_server import make_server
#from pygame import Surface
#import time
#import wsgiref
#pygame.init()
import network , gc 
from machine import I2C, Pin
import ssd1306
import socket
import usocket
import machine
import  urequests
#from ws2812 import WS2812
from machine import Pin, PWM ,ADC
#import servo_ori1
import servo
#from rpi_ws281x import *
import neopixel
import usocket as socket
import uselect as select
#---------------------------------------------------------------------------------------
#p26 = machine.Pin(26)

n =60
p = 0
np = neopixel.NeoPixel(machine.Pin(p), n)



#dati x connessione
LOCAL_ADDR = "192.168.1.32", 80
#TRACK_LOCAL_ADDR = "192.168.1.2", 5005
#

#Setup PINS
LED0 = machine.Pin(14, machine.Pin.OUT)
LED2 = machine.Pin(27, machine.Pin.OUT)



#---------------------------------------------------------------asegnazione pin
#global message,canale
#Setup PINS
#LED0 = machine.Pin(14, machine.Pin.OUT)
#LED2 = machine.Pin(27, machine.Pin.OUT)
in3= Pin(13, Pin.OUT)
in4 = Pin(27, Pin.OUT)
#p25 = machine.Pin(25)



in1= Pin(12, Pin.OUT)
in2 = Pin(14, Pin.OUT)
p26 = machine.Pin(26)

in5 = Pin(5, Pin.OUT)
in18 = Pin(18 ,Pin.OUT)
p17 = machine.Pin(17)


# in4.value(1)
# p26 = machine.Pin(25)
# servo = machine.PWM((p26) ,freq=50)#,duty=40)
# servo.duty(int(300))

#---------------------variabli velita uty pwm

vel400=400
vel800=800


#------------------------------------settaggio schermo oled 128x64??
rst = Pin(16, Pin.OUT)
rst.value(1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.ifconfig(('192.168.1.32','255.255.255.0','192.168.1.1','85.37.17.17'))#[0]
        sta_if.connect('TIM-28391995', 'casapiccia66acasapiccia66a')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    #IPaddr= sta_if.ifconfig()[0]
    oled.text(sta_if.ifconfig()[0], 10, 35)
    oled.text('La Faglia', 10, 50)
    oled.show()

do_connect()



def do_something_else():   
#The other script to be executed besides of the blocking socket
    url = "http://worldtimeapi.org/api/timezone/Europe/Rome" #http://worldtimeapi.org/timezone/Europe/Rome" # see http://worldtimeapi.org/timezones
    web_query_delay = 60000 # interval time of web JSON query
    retry_delay = 5000 # interval time of retry after a failed Web query
    rtc=RTC()
    # set timer
    update_time = utime.ticks_ms() - web_query_delay
    #settime()
    tempo=utime.localtime()
    print((str(tempo)))
    
#     oled.text(str(tempo), 10, 50)
#     oled.show()
   # while True:
        # query and get web JSON every web_query_delay ms
    if utime.ticks_ms() - update_time >= web_query_delay:
    
        # HTTP GET data
        response_tempo = urequests.get(url)
    
        if response_tempo.status_code == 200: # query success
        
            print("JSON response:\n", response_tempo.text)
            
            # parse JSON
            parsed = response_tempo.json()
            datetime_str = str(parsed["datetime"])
            year = int(datetime_str[0:4])
            month = int(datetime_str[5:7])
            day = int(datetime_str[8:10])
            hour = int(datetime_str[11:13])
            minute = int(datetime_str[14:16])
            second = int(datetime_str[17:19])
            subsecond = int(round(int(datetime_str[20:26]) / 10000))
            #if minute ==31:
                #Client_handler(LEDON0=6)
                #LED2.value(1)
                #print (("LED0 value="),LED0.value())
            # update internal RTC
            rtc.datetime((year, month, day, 0, hour, minute, second, subsecond))
            update_time = utime.ticks_ms()
            print("RTC updated\n")
   
        else: # query failed, retry retry_delay ms later
            update_time = utime.ticks_ms() - web_query_delay + retry_delay
        
    # generate formated date/time strings from internal RTC
    date_str = "Date: {2:02d}/{1:02d}/{0:4d}".format(*rtc.datetime())  
    time_str = "Time: {4:02d}:{5:02d}:{6:02d}".format(*rtc.datetime())

    # update SSD1306 OLED display
    oled.fill(0)
    oled.text("ESP32 WebClock", 0, 5)
    oled.text(date_str, 0, 25)
    oled.text(time_str, 0, 45)
    oled.show()
    
    utime.sleep(0.1)
    
#-----------------------------class motor----------
# class motor():
#      def __init__(self,Ena,In1,In2):
#         self.Ena = Ena
#         self.In1 = In1
#         self.In2 = In2
#         GPIO.setup(self.Ena,GPIO.OUT)
#         GPIO.setup(self.In1,GPIO.OUT)
#         GPIO.setup(self.In2,GPIO.OUT)
#         self.pwm = GPIO.PWM(self.Ena, 100)
#         self.pwm.start(0)
#     def moveF(self,x=100,t=0):
#         self.pwm.ChangeDutyCycle(x)
#         GPIO.output(self.In1,GPIO.HIGH)
#         GPIO.output(self.In2,GPIO.LOW)
#         sleep(t)
#     def moveB(self,x=100,t=0):
#         self.pwm.ChangeDutyCycle(x)
#         GPIO.output(self.In1,GPIO.LOW)
#         GPIO.output(self.In2,GPIO.HIGH)
#         sleep(t)
#     def stop(self,t=0):
#         self.pwm.ChangeDutyCycle(0)
#         sleep(t)
#  
# motor1 = motor(2,3,4)
# while True:
#     
#     motor1.moveF(30,2)
#     motor1.stop(1) 
#     motor1.moveB(t=2)
#     motor1.stop(1)
#-------------------------------------------


        
        
def Client_handler(client_obj):
#Do this when there's a socket connection
    
    def set_color(int_r, int_g, int_b):
                for i in range(n):
                    np[i] = int_r, int_g, int_b
                np.write()
    
    
    
    request = conn.recv(1024)
    print("Content = %s" % str(request))
    
    request = str(request)
    LEDON0 = request.find('/?LED=ON0')
    LEDOFF0 = request.find('/?LED=OFF0')
    LEDON2 = request.find('/?LED=ON2')
    LEDOFF2 = request.find('/?LED=OFF2')
    ON_RED = request.find('/?LED=ON_RED')
    OFF_RED = request.find('/?LED=OFF_RED')
    ON_GREEN = request.find('/?LED=ON_GREEN')
    OFF_GREEN = request.find('/?LED=OFF_GREEN')
    ON_BLU = request.find('/?LED=ON_BLU')
    OFF_BLU = request.find('/?LED=OFF_BLU')
    ON_BOUNCE = request.find('/?LED=ON_BOUNCE')
    OFF_BOUNCE = request.find('/?LED=OFF_BOUNCE')
    ON_BIANCO = request.find('/?LED=ON_BIANCO')
    OFF_BIANCO = request.find('/?LED=OFF_BIANCO')
    RED = (255, 0, 0, 0)
    YELLOW = (255, 150, 0, 0)
    GREEN = (0, 255, 0, 0)
    CYAN = (0, 255, 255, 0)
    BLUE = (0, 0, 255, 0)
    PURPLE = (180, 0, 255, 0)
    
    #print("Data: " + str(LEDON0))
    #print("Data2: " + str(LEDOFF0))
    if LEDON0 == 6:
        print('TURN LED0 ON')
        LED0.value(0)
    if LEDOFF0 == 6:
        print('TURN LED0 OFF')
        LED0.value(1)
    if LEDON2 == 6:
        print('TURN LED2 ON')
        LED2.value(0)
    if LEDOFF2 == 6:
        print('TURN LED2 OFF')
        LED2.value(1)
        
        
    if ON_RED == 6 :
                set_color(255, 0, 0)
                
    if OFF_RED == 6 :
                set_color(0, 0, 0)
  
    if ON_GREEN == 6 :
                set_color(0, 255, 0)
                
    if OFF_GREEN == 6 :
                set_color(0, 0, 0)
                 
    
    if ON_BLU == 6 :
                set_color(0, 0, 255)
                
    if OFF_BLU == 6 :
                set_color(0, 0, 0)
                
                
    if ON_BIANCO == 6 :
                set_color(255,255,255)
                
    if OFF_BIANCO == 6 :
                set_color(0, 0, 0) 
                
    if ON_BOUNCE == 6 :
        
        
        
        
        
        
        def color_chase( wait=0.01):
            for i in range(n):
                np[i] = GREEN
                time.sleep(wait)
                np.write()              
            for i in range(n):
                np[i] = RED
                time.sleep(wait)
                np.write()
            for i in range(n):
                np[i] = BLUE
                time.sleep(wait)
                np.write()       
            #time.sleep(1)
        color_chase(0.01)    
        
   #----------------    # fade in/out
        for i in range(0, 4 * 256, 8):
            for j in range(n):
                if (i // 256) % 2 == 0:
                    val = i & 0xff
           
                    
                else:
                    val = 255 - (i & 0xff)
                
                np[j] = (0, 0,val)
                
            np.write()
            time.sleep_ms(2)
# #             
# #---------------------------------------------
         
         
#         def rainbow_cycle(wait=5):
#             for j in range(255):
#                 for i in range(n):
#                     np= (i * 256 // n) + j
#                     np[i] = wheel(pixel_index & 255)
#                 np.write()
#                 time.sleep(wait)

        # clear
#         for i in range(n):
#             np[i] = (0, 0, 0)
#         np.write()
#         

#                 # bounce
        for i in range(4 * n):
            for j in range(n):
                np[j] = (0, 0, 0)
            if (i // n) % 2 == 0:
                np[i % n] = (0, 0, 255)
#                 if OFF_BOUNCE == 6 :
#                     set_color(0, 0, 0)  
            else:
                np[n - 1 - (i % n)] = (0, 0, 255)
#                 if OFF_BOUNCE == 6 :
#                     set_color(0, 0, 0)  
            np.write()
            time.sleep(0.01)
            
            
        #def color_chase(color=(255,0,0), wait=10):
        
        adj = ["red", "big", "tasty"]
        fruits = ["apple", "banana", "cherry"]
        
        def wheel(pos=200):
            # Input a value 0 to 255 to get a color value.
            # The colours are a transition r - g - b - back to r.
            if pos < 0 or pos > 255:
                r = g = b = 0
            elif pos < 85:
                r = int(pos * 3)
                g = int(255 - pos * 3)
                b = 0
            elif pos < 170:
                pos -= 85
                r = int(255 - pos * 3)
                g = 0
                b = int(pos * 3)
            else:
                pos -= 170
                r = 0
                g = int(pos * 3)
                b = int(255 - pos * 3)
            return (r, g, b) 
         
         
        def rainbow_cycle(wait):
        
            for j in range(255):
                for i in range(n):                   
                    pixel_index = (i * 8 // n) + j   #se metto uno passa da un singolo colore a l'altro se metto 256 fa arcobaleno mobile su tutti i led colori misti
                    np[i] = wheel(pixel_index & 255)
                        
                np.write()
                time.sleep(0.05)
               #break
        rainbow_cycle(5)  
       
                            
                   

                
    if OFF_BOUNCE == 6 :
                set_color(0, 0, 0)              
             
 #-----------------------input txt singoli uno red uno green uno blu-------------------------               
       
    r= str(request.partition("GET /?R")[2].partition("&")[0] )
    str_r=str(r)
    if str_r=="" :
        str_r=0
    print(("str_r"),str_r)
    #int_r=int(str_r)
    #self.int_split_req=int_split_req
    
    g= str(request.partition("GET /?G")[2].partition("&")[0] )
    str_g=str(g)
    if str_g=="" :
        str_g=0
    print(("str_g"),str_g)
    #int_g=int(str_g)
    #self.int_split_req=int_split_req
    
    b= str(request.partition("GET /?B")[2].partition("&")[0] )
    str_b=str(b)
    if str_b=="" :
        str_b=0
    print(("str_b"),str_b)
    #int_b=int(str_b)
    #self.int_split_req=int_split_req
      
#-----------------------------------------------------------------------------
    
    
    
    
#----------------input text rgb valore sano intervallato da "!" e "!!" -----------------------------
    
    rgb= str(request.partition("GET /?val_rgb")[2].partition("&")[0] )
    str_rgb=str(rgb)
    if str_rgb=="" :
        str_rgb=0
    print(("str_rgb"),str_rgb)
    
    if rgb !="" :
        int_r_s = str(request.partition("GET /?val_rgb")[2].partition("!")[0] )
        print(("Red in rgb"),type(int_r_s),int_r_s)
       
        if int_r_s=="" :
             int_r_s=0
    #     hex_r_s = hex(int_r_s)
    #     print(("HEX_R_S "),type(hex_r_s),hex_r_s)
        int_r = int(int_r_s)
       # print(("INT_R "),type(int_r),int_r)
    #     
        
        
        int_g_s = str(request.partition("!")[2].partition("!!")[0] )
        print(("Green in rgb"),int_g_s)
        str_g_s=str(int_g_s)
        if str_g_s=="" :
            str_g_s=0
        int_g = int(str_g_s)
    #     hex_g = hex(str_g) 
    #     int_g = int(hex_g)
    #     print(("int_g da hexadecimale a decimale"),int_g)
        
        
        
        int_b_s  = str(request.partition("!!")[2].partition("&")[0] )            #=rgb[4:6]
        print(("Blu in rgb"),int_b_s)
        str_b_s=str(int_b_s)
        if str_b_s=="" :
            str_b_s=0
        int_b = int(str_b_s)
    #     hex_b = hex(str_b) 
    #     int_b = int(hex_b,16)
    #     
    #     if len(request) <8 :
    #         
    #             rgb_presenza = "r"
    #             print(("request se piu corto di 8 "),rgb_presenza)
    #             set_color(int_r, int_g, int_b)
    #     else :
    #         pass
        #print(("request[6]"),request[6])
       # if request[6] =="r" :
            
        set_color(int_r, int_g, int_b)
        
        
        
            # ------------------------------input del pick color web     ---------------------------------   

    rgb_pick= str(request.partition("GET /?")[2].partition("&")[0] )
    str_rgb_pick=str(rgb_pick)
    if str_rgb_pick=="" :
        str_rgb_pick=0
    print(("str_rgb_pick"),str_rgb_pick)
    
    
                
    if rgb_pick !="" and rgb_pick[0]=="r" :
        
        
        
        #print (("request8 col botto  pick "),request[8])
         
        
        int_r_s_pick = str(rgb_pick.partition("r")[2].partition("g")[0] )
        print(("Red in rgb_pick"),type(int_r_s_pick),int_r_s_pick)
        str_r_s_pick=str(int_r_s_pick)
        if str_r_s_pick =="" :
            str_r_s_pick =0
        int_r = int(str_r_s_pick)
        print(("INT_R_pick "),type(int_r),int_r)
    #     
        
        
        int_g_s_pick = str(rgb_pick.partition("g")[2].partition("b")[0] )
        print(("Green in rgb_pick"),int_g_s_pick)
        
        str_g_s_pick=str(int_g_s_pick)
        if str_g_s_pick =="" :
            str_g_s_pick =0
        int_g = int(str_g_s_pick)
    #     hex_g = hex(str_g) 
    #     int_g = int(hex_g)
    #     print(("int_g da hexadecimale a decimale"),int_g)
        
        int_b_sano_pick  = str(request)
        if  int_b_sano_pick ==""  :
             int_b_sano_pick =="0"
             
        print(("request SANO_pick"),int_b_sano_pick)
        int_b_s_pick  = str(int_b_sano_pick.split("b")[2].partition("&")[0] )          #=rgb[4:6]
        print(("Blu in rgb _pick"),int_b_s_pick)
        str_b_s_pick=str(int_b_s_pick)
        if str_b_s_pick =="" or request[6] !="r"  :
            str_b_s_pick =0
        int_b = int(int_b_s_pick)
        print(("INT B derivato da sano per PICKER"),int_b)
        
        set_color(int_r, int_g, int_b)
     
    else :
       pass
         
    #          controllo_req_pick == "r" 
        
    
        #     
        #     int_b_s  = str(request.partition("!!")[2].partition("&")[0] )            #=rgb[4:6]
        #     print(("Blu in rgb"),int_b_s)
        #     str_b_s=str(int_b_s)
        #     if str_b_s=="" :
        #         str_b_s=0
        #     int_b = int(str_b_s)
        #     hex_b = hex(str_b) 
        #     int_b = int(hex_b,16)


    #  --------------------------------------------------------------------------
            
            
        #set_color(int_r, int_g, int_b)
        
    
    
    
    
    #--------------------------------------------------------------------------------------------------------------    
#     def demo(np):
#         n = np.n
# 
#         # cycle
#         for i in range(1 * n):
#             for j in range(n):
#                 np[j] = (0, 0, 0)
#             np[i % n] = (29, 2, 255)
#             np.write()
#             time.sleep_ms(25)
# 
#         # bounce
#         for i in range(4 * n):
#             for j in range(n):
#                 np[j] = (0, 0, 0)
#             if (i // n) % 2 == 0:
#                 np[i % n] = (29, 2, 125)
#             else:
#                 np[n - 1 - (i % n)] = (29, 2, 125)
#             np.write()
#             time.sleep_ms(5)
# 
#         # fade in/out
#         for i in range(0, 4 * 256, 8):
#             for j in range(n):
#                 if (i // 256) % 2 == 0:
#                     val = i & 0xff
#                 else:
#                     val = 255 - (i & 0xff)
#                 np[j] = (val, 0, 0)
#             np.write()
# 
#         # clear
#         for i in range(n):
#             np[i] = (0, 0, 0)
#         np.write()    
#     
    
#     demo(np)
    #--------------------------------------------------------------------------------------------------------------
    response = web_page()          
    conn.send('HTTP/1.1 200 OK\n')          
    conn.send('Content-Type: text/html\n')           
    conn.send('Connection: close\n\n')           
    conn.sendall(response)
    conn.close()
    

# def Client_handler(client_obj):
# #Do this when there's a socket connection
#     request = conn.recv(1024)
#     print("Content = %s" % str(request))
#     
#     request = str(request)
#     LEDON0 = request.find('/?LED=ON0')
#     LEDOFF0 = request.find('/?LED=OFF0')
#     LEDON2 = request.find('/?LED=ON2')
#     LEDOFF2 = request.find('/?LED=OFF2')
#     #print("Data: " + str(LEDON0))
#     #print("Data2: " + str(LEDOFF0))
#     if LEDON0 == 6:
#         print('TURN LED0 ON')
#         LED0.value(0)
#     if LEDOFF0 == 6:
#         print('TURN LED0 OFF')
#         LED0.value(1)
#     if LEDON2 == 6:
#         print('TURN LED2 ON')
#         LED2.value(0)
#     if LEDOFF2 == 6:
#         print('TURN LED2 OFF')
#         LED2.value(1)
#     
#         
#     
#     response = web_page()
#     
#     conn.send('HTTP/1.1 200 OK\n')
#     
#     conn.send('Content-Type: text/html\n')
#     
#     conn.send('Connection: close\n\n')
#     
#     conn.sendall(response)
#     
#     conn.close()
    
#----------------------------------------------------
#'---------------------test rele 3108--------------
#rboard1 = Pin(14, Pin.OUT)
#rboard1.value(1)
#-----------------------------------------------

#led = Pin(14, Pin.OUT)
#led.value(1)
#--------------------------------------------


#dati x connessione
LOCAL_ADDR = "192.168.1.32", 80
#TRACK_LOCAL_ADDR = "192.168.1.2", 5005
#
#----------------------------------------------
#istruzioni per ritardo invio a client

# def sock_rd(s):
#         try:
#             return s.recvfrom(LEN_UDP_BUFFER)
#         except:
#            return "".encode("ascii"), ("", 0)
#-----------------------------------------------------
# def sock_trak(track):
#         try:
#             return trak.recvfrom(LEN_UDP_BUFFER)
#         except:
#            return "".encode("ascii"), ("", 0)
# #----------------------------
# 

# web = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# web.bind(LOCAL_ADDR)
# web.listen(5)
# ser= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# ser.bind(TRACK_LOCAL_ADDR)


oled.fill(0)
def web_page(): 
    if LED0.value() == 0:
        gpio_state_0="ON"
    else:
        gpio_state_0="OFF"
        
    if LED2.value() == 0:
        gpio_state_2="ON"
    else:
        gpio_state_2="OFF"
    #<meta http-equiv="refresh" content="1" />    
    html = """<!DOCTYPE html>
    <html>
   
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">


<body>
    
    
    <center><h5>Semplice webserver per switchare on e off luci con Esp32 della Heltec e Micropython </h5></center>
    <center><h6>(dati dal 66 alla Faglia e viceversa (legge e scrive (monitoring and control) )</h6></center>
     <form>
    Lampadario del Drone (led0) :  GPIO state: <strong>""" +  gpio_state_0 + """</strong>
    
    <button name="LED" value="ON0"   type="submit">LED ON </button> 
    <button name="LED" value="OFF0"  type="submit">LED OFF</button> </p>
    
    <p>Luce laterale frontale giardino: GPIO state: <strong>""" +  gpio_state_2 + """</strong>
    <button name="LED" value="ON2"  type="submit">LED ON</button>
    <button name="LED" value="OFF2" type="submit">LED OFF</button>
    <p>


  

    
<style>
.LED {
color: #fff !important;
text-transform: uppercase;
text-decoration: none;
background: #ff0000;
padding: 10px;
border-radius: 30px;
display: inline-block;
border: none;
transition: all 0.4s ease 0s;
}
</style>
<div>
    <p style ="color:Red;">bottone RGB rosso : GPIO state: <strong>""" +  gpio_state_2 + """</strong>
    <button name="LED" value="ON_RED"  class="LED"   type="submit">RED ON    </button>
    <button name="LED" value="OFF_RED" type="submit">RED OFF</button></p></div>


<style>
.LEDg {
color: #fff !important;
text-transform: uppercase;
text-decoration: none;
background: #00ff00;
padding: 10px;
border-radius: 30px;
display: inline-block;
border: none;
transition: all 0.4s ease 0s;
}
</style>
<div>
    <p style ="color:Green;">bottone RGB VERDE : GPIO state: <strong>""" +  gpio_state_2 + """</strong>
    <button name="LED" class="LEDg" value="ON_GREEN" type="submit">GREEN ON</button>
    <button name="LED" value="OFF_GREEN" type="submit">GREEN OFF</button>
    <p></div>


<style>
.LEDb {
color: #fff !important;
text-transform: uppercase;
text-decoration: none;
background: #0000ff;
padding: 10px;
border-radius: 30px;
display: inline-block;
border: none;
transition: all 0.4s ease 0s;
}
</style>
<div>
    <p style ="color:Blue;">bottone RGB BLU : GPIO state: <strong>""" +  gpio_state_2 + """</strong>
    <button name="LED" class="LEDb" value="ON_BLU" type="submit">BLU ON</button>
    <button name="LED" value="OFF_BLU" type="submit">BLU OFF</button>
    <p></div>


<style>
.LEDw {
color: #000 !important;
text-transform: uppercase;
text-decoration: none;
background: #ffffff;
padding: 10px;
border-radius: 30px;
display: inline-block;
border: yes;
transition: all 0.4s ease 0s;
}
</style>
<div>

 bottone BIANCO : GPIO state: <strong>""" +  gpio_state_2 + """</strong>
    <button name="LED" class="LEDw" value="ON_BIANCO type="submit">BIANCO ON</button>
    <button name="LED" value="OFF_BIANCO" type="submit">BIANCO OFF</button>
    <p></div>




bottone BOUNCE: GPIO state: <strong>""" +  gpio_state_2 + """</strong>
    <button name="LED" value="ON_BOUNCE type="submit">BOUNCE ON</button>
    <button name="LED" value="OFF_BOUNCE" type="submit">BOUNCE OFF</button>
    <p>

            
</form>



    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    

         Immetti codice RGB inserisci in formato   "val r ! val g !! val r":<input id="joy1Y" type="text"  required pattern="\d+!\d+!!\d+" onchange="servo_imm_rgb(this.value)">     
            <script>
            function servo_imm_rgb(pos) {
          $.get("/?val_rgb" + pos + "&");
          {Connection: close};
        }
        </script>
        
        
        
        
            
   
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
            <link rel=\"icon\" href=\"data:,\">
            <link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css\">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
            <script src=\"https://cdnjs.cloudflare.com/ajax/libs/jscolor/2.0.4/jscolor.min.js\"></script>
      
           </head>
            <body>
<form>
            <div class=\"container\"><div class=\"row\"><h1>ESP Color Picker</h1></div>
            <a class=\"btn btn-primary btn-lg\" href=\"#\" id=\"change_color\" role=\"button\">Change Color</a> 
            <input class=\"jscolor {onFineChange:'update(this)'}\" id=\"rgb\"></div>
      </form>
      
      <script>
function update(picker) {
document.getElementById('rgb').innerHTML = Math.round(picker.rgb[0]) + ', ' +  Math.round(picker.rgb[1]) + ', ' + Math.round(picker.rgb[2]);
document.getElementById(\"change_color\").href=\"?r\" + Math.round(picker.rgb[0]) + \"g\" +  Math.round(picker.rgb[1]) + \"b\" + Math.round(picker.rgb[2]) + \"&\";};

</script>
</body>
</html>
    
    
   
    
   
    


        </html>
        """
        #return self.int_split_req
    return html
        



#print(("valore int_split_req con classe"),R.controllo(int_split_req))









# #Setup PINS
# LED0 = machine.Pin(14, machine.Pin.OUT)
# LED2 = machine.Pin(27, machine.Pin.OUT)

#Setup Socket WebServer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(0)
s.bind(('', 80))
s.listen(5)
while True:
    #def tempo():
    #try:
       
        #tempo()
    #except:

            
            
        r, w, err = select.select ((s,), (), (), 1)
        if r:
            for readable in r:
                conn, addr = s.accept()
                print("Got a connection from %s" % str(addr))
                conn.settimeout(5)
                
                try:
                     Client_handler(conn)
                except OSError as e:
                        pass
#         LED2.value(1)
#         time.sleep(1)
      
        #do_something_else()        



#while True:
    
#     in3= Pin(13, Pin.OUT)
#     in3.value(1)
#     in4 = Pin(27, Pin.OUT)
#     in4.value(0)
#     p26 = machine.Pin(25)
#     servo = machine.PWM((p26) ,freq=50)#,duty=205)
#     
#     servo.duty(int(500))
#     time.sleep(2)
#     in3= Pin(13, Pin.OUT)
#     in3.value(0)
#     in4 = Pin(27, Pin.OUT)
#     in4.value(1)
#     p26 = machine.Pin(25)
#     servo = machine.PWM((p26) ,freq=50)#,duty=40)
#     servo.duty(int(300))
#     time.sleep(2)
#     oled.text('se move?', 10, 50)
#     oled.show()
#------------------------------------------------------------------------------






# def scale_value3(value, in_min, in_max, out_min, out_max):
#       scaled_value3 = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
#       return scaled_value3
#     
# d3 = scale_value3(messageint3, float(0),float(15), 512,1023) #(30/20), (30/10))
# if d3>549 and d3<749:
#     d3=649
#     time.sleep(0.02)
#     servo.duty(int(d3))
#     print (("d3="),float(d3))
#     #time.sleep(0.02)
#     oled.text((str(int(d3))), 70, 30)
#     oled.show()
# 
# else:
#     d3 = scale_value3(messageint3, float(0), float(15), 512,1023) #(30/20), (30/10))
#     #time.sleep(0.02)
#     #print (("d2="),float(d2))
#     servo.duty(int(d3))
#     #time.sleep(0.02)
#     print (("d3="),float(d3))
#     oled.text((str(int(d3))), 70, 30)
#     oled.show()
