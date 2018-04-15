import time                                                                     
import sys                                                                      
import json                                                                     
# import smbus                                                                    
# bus = smbus.SMBus(1)   

DATA_SIZE = 8    
addrs = [0x04, 0x06, 0x08]                                                                                                                   
cmd = 255                                                                       
                                                            
                                          
def test(): 
    i = 0                                                                
    while True:
        i %= size
        array = [0] * size
        array[i] = 1    
        send_data(addr1, array)
        
        array = [0] * size
        array[(i+1)%DATA_SIZE] = 1 
        send_data(addr2, array)   

        array = [0] * size
        array[(i+2)%DATA_SIZE] = 1 
        send_data(addr3, array)   
        i += 1

def send_data(address, array):
    # try:                                                                    
    #     bus.write_i2c_block_data(address, cmd, array)                                                                                        
    # except OSError:                                                         
    #     print('oserror')                                                    
    print('address {} data {}'.format(address, array))                               
    time.sleep(0.1)     

def transmit(data):
    print(data)
    for i, addr in enumerate(addrs):
        send_data(addr, data[i * DATA_SIZE:(i+1) * DATA_SIZE])
