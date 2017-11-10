import logging
import asyncio
import json
import base64
import time
import math
import sys
import os
import django


##Needed to be able to write data to web server
os.environ["DJANGO_SETTINGS_MODULE"] = 'mysite.settings'
django.setup()

from demo.models import TBRsensorData, tagDetection
##

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2


#Full DEVeui can be found by uncommenting console logs in the node application running on the conduit.
DEVeui = ['82-78-00-00-00-00-87-00','82-78-00-00-00-00-82-00']

@asyncio.coroutine
def uptime_coro():
    C = MQTTClient()
    try:
        #Change IP address to the broker/server IP
        yield from C.connect('mqtt://localhost')
        #Edit here for what lora cards you want to receive data from.
        yield from C.subscribe([
                ('lora/'+DEVeui[0]+'/down',QOS_1),
                ('lora/'+DEVeui[1]+'/down',QOS_1)
             ])
        
        while True:
            try:
                message = yield from C.deliver_message()
                packet = message.publish_packet
                print("%s => %s" % (packet.variable_header.topic_name, str(packet.payload.data)))
                decode = json.loads(packet.payload.data)
                handle_packet(decode,packet.variable_header.topic_name)
            except MQTTException:
                logger.debug("Error reading packet")
            
        #yield from C.unsubscribe(['lora/86-78-00-00-00-00-86-00/down']) #Might be unnessessary
        yield from C.disconnect()
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)
        yield from C.disconnect()
    except KeyboardInterrupt:
        yield from C.disconnect()

def handle_packet(decode,topic):
    ##Decodes received data from base64 to bytes
    data = base64.b64decode(decode['data'])
    
    ##Sorts data in TBR spec, writes to console, stores to SQL/webserver and writes to file.
    message_format.sort_message(data)
    
    ##Write to file. Storing raw data, not intended for finished product 
    data_ints = {}

    for i in range(0, len(data)):
        data_ints[i] = int(data[i])
    f = open('test2.txt','a')
    f.writelines([str(topic)," ",str(data_ints),'\n'])
    f.close()
    ###
    
    ###
    
    ##Run position algorithm
    #posAlg.positionAlg()

class message_format:
    serial=-1
    timestamp=0
    codeType=0
    codeID=0
    codeData=0
    SNR=0
    millisec=0
    temperature=0
    noise=0
    noiseLP=0
    frequency=0
    def __init__(self):
        pass
    def sort_message(data):
        print("Nr. messages received: ",(len(data)-1)%10)
        for i in range(0,int((len(data)-1)/11)):
            message = message_format()
            message.serial = data[0]
            for j in range(0,11):
                index = 11*i+j+1
                #Unix time stamp
                if j >= 0 and j <= 3:   
                    message.timestamp = message.timestamp + data[index]*math.pow(256,(3-j))
                #CodeType
                elif j == 4:            
                    message.codeType = data[index]
                #Temperature/CodeID   
                elif j >= 5 and j <= 6: 
                    if message.codeType == 255:
                        message.temperature = message.temperature + data[index]*math.pow(256,(6-j))
                    else:
                        message.codeID = message.codeID + data[index]*math.pow(256,(6-j))
                #Code Data
                elif j >= 7 and j <= 8 and message.codeType != 255:
                    message.codeData = message.codeData + data[index]*math.pow(256,(8-j))
                #6 bit SNR & 2 bit millisec
                elif j == 9 and message.codeType != 255:
                    mask = 0b00000011
                    value = mask & data[index]
                    message.millisec = value*math.pow(2,8)
                    snr = bin(data[index])
                    message.SNR = int(snr[0:8],2)
                #8 bit millisec
                elif j == 10 and message.codeType != 255:
                    message.millisec = message.millisec + data[index]
                #Noise
                elif j == 7 and message.codeType == 255:
                    message.noise = data[index]
                #Noise LP
                elif j == 8 and message.codeType == 255:
                    message.noiseLP = data[index]
                #Frequency
                elif j == 10 and message.codeType == 255:
                    message.frequency = data[index]
                
            message.temperature = (message.temperature-50)/10     
            print("------Message nr.",i,"------")
            print("TBR serial:",message.serial)
            print("Timestamp: ",message.timestamp)
            print("codeType:  ",message.codeType)
            
            if message.timestamp > 1483228800:  #Simple mechanism to prevent storing corrupted messages, implement improved method later
                if message.codeType != 255:
                    #Print
                    print("codeID:    ",message.codeID)
                    print("codeData:  ",message.codeData)
                    print("SNR:       ",message.SNR)
                    print("millisec:  ",message.millisec)
                    #SQLite/webserver. See ../mysite/demo/models.py to add different data
                    tagDetection(timestamp=message.timestamp,codeID=message.codeID,codeData=message.codeData,snr=message.SNR,millisec=message.millisec).save()
                    #Write to file. The text file is an end-stop, i.e. it's not used by any other application for reading/processing. So changing the format shouldn't be a problem. 
                    f = open('tagDetections.txt','a')
                    f.writelines([str(int(message.timestamp)),"\t",str(message.codeType),"\t",str(int(message.codeID)),"\t",str(int(message.codeData)),"\t",str(message.SNR),"\t",str(int(message.millisec)),'\n'])
                    f.close()
                elif message.codeType == 255:
                    #Print
                    print("temperature:",message.temperature)
                    print("Noise:      ",message.noise)
                    print("NoiseLP:    ",message.noiseLP)
                    print("frequency:  ",message.frequency)
                    #SQLite/webserver. See ../mysite/demo/models.py to add different data
                    TBRsensorData(timestamp=message.timestamp,temp=message.temperature,noise=message.noise,noiseLP=message.noiseLP,freq=message.frequency).save()
                    #Write to file. The text file is an end-stop, i.e. it's not used by any other application for reading/processing. So changing the format shouldn't be a problem.
                    f = open('TBRSensorData.txt','a')
                    f.writelines([str(int(message.timestamp)),"\t",str(message.codeType),"\t",str(message.temperature),"\t",str(message.noise),"\t",str(message.noiseLP),"\t",str(message.frequency),'\n'])
                    f.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(uptime_coro())
