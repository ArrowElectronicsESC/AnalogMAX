import serial
import numpy as np
from matplotlib import pyplot as plt
from time import time
from ipywidgets import widgets
from IPython.display import clear_output



##################################################################################################
# Accelerometer sensor demo
##################################################################################################
def ADXL362_write_reg(reg, value, serialport):
    cmd = "<0a%0.2x%0.2x>" % (reg, value) # Write command 0x0A
    serialport.write(bytearray(cmd,'utf8'))  # Send command, REG and value
    return

def ADXL362_read_reg8(reg, serialport):
    serialport.reset_input_buffer()
    cmd = "<0b%0.2x..>" % reg # Read command 0x0B
    serialport.write(bytearray(cmd,'utf8'))  # Send command, REG and value
    s = ser.read(2)
    return int(s,16)                  # Convert hex to int
#
def ADXL362_read_reg16(reg, serialport):
    serialport.reset_input_buffer()
    cmd = "<0b%0.2x..><0b%0.2x..>" % (reg+1, reg) # Read command 0x0B
    serialport.write(bytearray(cmd,'utf8'))  # Send command, REG and value
    s = serialport.read(4)
    return int(s,16)                 # Convert hex to int
#
# Read sign extended 16 bit register 
#
def ADXL362_read_reg16_sx(reg, serialport):
    t = ADXL362_read_reg16(reg, serialport)
    if t > 32768: t = t - 65536
    return t    

def ADXL362_read_axis(axis, serialport):
    return ADXL362_read_reg16_sx(axis*2 + 0x0e, serialport)



##################################################################################################
# Smoke sensor demo
##################################################################################################
#
# ADPD register access functions
#
def ADPD_write_reg(reg, value, serialport):
    serialport.reset_input_buffer() #
    cmd = "<c8K%0.2xK%0.2xK%0.2xK>" % (reg, (value >> 8), (value & 0xFF))
    serialport.write(bytearray(cmd,'utf8'))  # Send command, REG and value
    return

def ADPD_read_reg(reg, serialport):
    serialport.reset_input_buffer() #
    cmd = "<c8K%0.2xK<c9K..m..M>" % reg  # 
    serialport.write(bytearray(cmd,'utf8'))  # Send command, REG and value
    s = serialport.read(4)
    return int(s, 16)

def ADPD_read_fifo(serialport):
    fifolevel = ADPD_read_reg(0x00, serialport) >> 8
    # Do something if fifo level < 2 ?
    retval = ADPD_read_reg(0x60, serialport)
    retval = 1.0 * retval/16384
    return retval
#
# ADPD register init from ADI Wavetool Application
# Filename: ADPD188BI_SK.dcfg
#
def ADPD_init_SK(serialport):
    ADPD_write_reg(0x00 ,0x1000, serialport)
    ADPD_write_reg(0x01 ,0xC0FF, serialport)
    ADPD_write_reg(0x02 ,0x0005, serialport)
    ADPD_write_reg(0x06 ,0x0F00, serialport)
    ADPD_write_reg(0x09 ,0x00C8, serialport)
    ADPD_write_reg(0x10 ,0x0000, serialport)
    ADPD_write_reg(0x11 ,0x30A9, serialport)
    ADPD_write_reg(0x12 ,0x0050, serialport)
    ADPD_write_reg(0x14 ,0x0117, serialport)
    ADPD_write_reg(0x15 ,0x0220, serialport)
    ADPD_write_reg(0x18 ,0x1F00, serialport)
    ADPD_write_reg(0x19 ,0x3FFF, serialport)
    ADPD_write_reg(0x1A ,0x3FFF, serialport)
    ADPD_write_reg(0x1B ,0x3FFF, serialport)
    ADPD_write_reg(0x1E ,0x1F00, serialport)
    ADPD_write_reg(0x1F ,0x3FFF, serialport)
    ADPD_write_reg(0x20 ,0x3FFF, serialport)
    ADPD_write_reg(0x21 ,0x3FFF, serialport)
    ADPD_write_reg(0x22 ,0x3531, serialport)
    ADPD_write_reg(0x23 ,0x3533, serialport)
    ADPD_write_reg(0x24 ,0x3531, serialport)
    ADPD_write_reg(0x25 ,0x6317, serialport)
    ADPD_write_reg(0x30 ,0x0319, serialport)
    ADPD_write_reg(0x31 ,0x0810, serialport)
    ADPD_write_reg(0x34 ,0x0000, serialport)
    ADPD_write_reg(0x35 ,0x0319, serialport)
    ADPD_write_reg(0x36 ,0x0810, serialport)
    ADPD_write_reg(0x38 ,0x0000, serialport)
    ADPD_write_reg(0x39 ,0x2203, serialport)
    ADPD_write_reg(0x3B ,0x2203, serialport)
    ADPD_write_reg(0x3C ,0x31C6, serialport)
    ADPD_write_reg(0x3E ,0x0320, serialport)
    ADPD_write_reg(0x3F ,0x0320, serialport)
    ADPD_write_reg(0x42 ,0x1C34, serialport)
    ADPD_write_reg(0x43 ,0xADA5, serialport)
    ADPD_write_reg(0x44 ,0x1C34, serialport)
    ADPD_write_reg(0x45 ,0xADA5, serialport)
    ADPD_write_reg(0x4B ,0x269C, serialport)
    ADPD_write_reg(0x4D ,0x0082, serialport)
    ADPD_write_reg(0x54 ,0x0AA0, serialport)
    ADPD_write_reg(0x58 ,0x0000, serialport)
    ADPD_write_reg(0x59 ,0x0808, serialport)
    ADPD_write_reg(0x5A ,0x0010, serialport)
    ADPD_write_reg(0x5E ,0x0808, serialport)
    ADPD_write_reg(0x5F ,0x0000, serialport)
    return
    
def ADPD_init(serialport):
    ADPD_init_SK(serialport)
    # Change one setting
    ADPD_write_reg(0x11 ,0x3065, serialport)  # Channel A,B, Average, 16 bit sum of channels
    # Enter normal mode
    ADPD_write_reg(0x10 ,0x0002, serialport)
    return



##################################################################################################
# Temperature Sensor demo
##################################################################################################
#
# ADT7320 register access functions
#
def ADT7320_read_reg8(reg, serialport):
    serialport.reset_input_buffer()
    cmd = "<%0.2x..>" % (reg*8 + 64) 
    serialport.write(bytearray(cmd,'utf8'))   # Send read register command
    s = serialport.read(2)                    # Read data byte
    return int(s,16)                          # return unsigned 8 bit int

def ADT7320_read_reg16(reg, serialport):
    serialport.reset_input_buffer()
    cmd = "<%0.2x....>" % (reg*8 + 64)
    serialport.write(bytearray(cmd,'utf8'))   # Send read register command
    s = serialport.read(4)                    # Read two data bytes
    x = int(s,16)                             # Convert hex to int
    if x > 32768: x = x - 65536               # Convert to signed int
    return x    



##################################################################################################
# AnalogMax: AD5592R ADC/DAC/GPIO Demo
##################################################################################################
#
# AD5592 register access functions
#
ADC_GAIN = 1 # Default Gain is 1 after reset/poweron

def AD5592_write_reg(reg, value, serialport):
    cmd = "<%0.4x>" % ((reg << 11) + (value & 0xfff))
    serialport.write(bytearray(cmd,'utf8'))  # Send command, REG and value
    return

def AD5592_write_dac(dac, value, serialport):
    cmd = "<%0.4x>" % ((dac << 12) + (value & 0xfff) | 0x8000)
    serialport.write(bytearray(cmd,'utf8'))  # Send command, REG and value
    return

def AD5592_read16(serialport):
    serialport.reset_input_buffer()
    serialport.write(b'<....>')   # Read result, (scan-in NOP)
    s = serialport.read(4)        # Read two data bytes
    return int(s,16)       # Convert hex to int
#
# Temperature(C) = 25 + (ADC - 820/Gain)/2.654
#
def AD5592_get_temperature(serialport):
    # Get result, assume that temp channel is enabled!
    t = AD5592_read16(serialport) & 0xfff # Strip Channel bits
    t = 25 + (t - 820/ADC_GAIN)/2.654
    return round(t,2)    
#
def AD5592_get_adc(serialport):
    # Get result, assume that single ADC channel is enabled!
    t = ADC_GAIN*2.5*(AD5592_read16(serialport) & 0xfff)/4096      # Strip Channel bits
    return round(t,2) 
