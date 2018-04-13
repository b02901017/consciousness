import time                                                                     
# import smbus                                                                    
import sys                                                                      
import json                                                                     
                                                                                
# bus = smbus.SMBus(1)                                                            
# address1 = 0x04                                                                 
# address2 = 0x08     
# cmd = 255                                                                       
                                                            
# size = 10                                                                      
# array = [0,1,0,0,0,0,0,0,0,0]                                                   
# array = [0,0,0,0,0,0,0,0,0,1]                                                   
                                                                                
# def I2C_loop(): 
#     i = 0                                                                
#     while True:
#         i %= size
#         array = [0] * size
#         array[i] = 1    
#         send_data(address1, array)
#         array = [0] * size
#         array[size -1 - i] = 1 
#         send_data(address2, array)                                                            
#         i += 1


def send_data(address, array):
    try:                                                                    
        bus.write_i2c_block_data(address, cmd, array)                                                                                        
    except OSError:                                                         
        print('oserror')                                                    
    print('address {} data {}'.format(address, array))                               
    time.sleep(0.1)     

def process_i2c(data):
    send_data(address1, data[:8])
    send_data(address2, data[8:])
    
