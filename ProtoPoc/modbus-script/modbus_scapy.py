from scapy.all import *
import time
import socket


# Modbus Master写单个线圈函数  func_code 0x5
def modbus_write_single_coin(ip, port, trans_id, unit_id, reference_num, data):
    """
    Args            
    ip              : modbus slave ip
    port            : modbus slave serve port
    trans_id        : transaction id
    reference_num   : referene address
    data            : write coin value
    """

    if (data != 0x0 and data != 0xff):
        print("write coin data is not valid ,only 0x0 and 0xff is allowed.\n")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    protocol_id = 0     #tcp
    
    modbus_header = struct.pack('>HHHBBH', trans_id, protocol_id, 6, unit_id, 0x5, reference_num) # 这里默认按照每个data item为short类型计算长度
    modbus_data = struct.pack(f'>BB', data, 0x0) # 1字节0x0 padding
    modbus_payload =  modbus_header + modbus_data
    
    sock.send(modbus_payload)    
    
    return sock.recv(1024)

# Modbus Master写多个线圈器函数  func_code 0xf
def modbus_write_multi_coins(ip, port, trans_id, unit_id,reference_num, num_bits, data):
    """
    Args            
    ip              : modbus slave ip
    port            : modbus slave serve port
    trans_id        : transaction id
    reference_num   : referene address
    num_bits        : number of coin bits to write
    data            : write coin bits value(1 byte ==> 8 bits value),
                        in array format
    """
    num_byte = len(data)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    protocol_id = 0     #tcp
    
    modbus_header = struct.pack('>HHHBBHHB', trans_id, protocol_id, 7+num_byte, unit_id, 0xf, reference_num, num_bits, num_byte) # 这里默认按照每个data item为short类型计算长度
    modbus_data = struct.pack(f'>{num_byte}B', *data)
    modbus_payload =  modbus_header + modbus_data
    
    sock.send(modbus_payload)    
    
    return sock.recv(1024)


# Modbus Master写单个寄存器函数  func_code 0x6:写单个寄存器
def modbus_write_single_register(ip, port, trans_id, unit_id, reference_num, data):
    """
    Args            
    ip              : modbus slave ip
    port            : modbus slave serve port
    trans_id        : transaction id
    reference_num   : referene address
    data            : write register value(short type)
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    protocol_id = 0     #tcp
    
    modbus_header = struct.pack('>HHHBBH', trans_id, protocol_id, 6, unit_id, 0x6, reference_num) # 这里默认按照每个data item为short类型计算长度
    modbus_data = struct.pack(f'>H', data)
    modbus_payload =  modbus_header + modbus_data
    
    sock.send(modbus_payload)    
    
    return sock.recv(1024)

# Modbus Master写多个寄存器函数  func_code 0x10:多个寄存器
def modbus_write_multi_registers(ip, port, trans_id, unit_id,reference_num, data):
    """
    Args            
    ip              : modbus slave ip
    port            : modbus slave serve port
    trans_id        : transaction id
    reference_num   : referene address
    data            : write registers value(short type), in array format
    """
    num_regs = len(data)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    protocol_id = 0     #tcp
    
    modbus_header = struct.pack('>HHHBBHHB', trans_id, protocol_id, 7+num_regs*2, unit_id, 0x10, reference_num, num_regs, 2*num_regs) # 这里默认按照每个data item为short类型计算长度
    modbus_data = struct.pack(f'>{num_regs}H', *data)
    modbus_payload =  modbus_header + modbus_data
    
    sock.send(modbus_payload)    
    
    return sock.recv(1024)

# Modbus Master读写多个寄存器函数  func_code 0x17:多个寄存器
def modbus_read_write_multi_registers(ip, port, trans_id, unit_id,read_ref_num, read_count, write_ref_num, data):
    """
    Args            
    ip              : modbus slave ip
    port            : modbus slave serve port
    trans_id        : transaction id
    write_ref_num   : write referene address
    data            : write registers value(short type), in array format
    read_ref_num    :  
    read_count      :
    """
    num_regs = len(data)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    protocol_id = 0     #tcp
    
    modbus_header = struct.pack('>HHHBBHHHHB', trans_id, protocol_id, 11+num_regs*2, unit_id, 0x17, read_ref_num, read_count, write_ref_num, num_regs, num_regs*2) # 这里默认按照每个data item为short类型计算长度
    modbus_data = struct.pack(f'>{num_regs}H', *data)
    modbus_payload =  modbus_header + modbus_data
    
    sock.send(modbus_payload)    
    
    # 正常返回，返回数据偏移8位置为read的数据长度，之后为read的数据
    
    return sock.recv(1024)
    

host = "10.51.43.111"
port = 502
trans_id = 1
unit_id = 1
ref_num = 0

# # 写多个寄存器
# write_data = [0x100, 0x200, 0x300]
# modbus_write_registers(host,port,trans_id, unit_id,  ref_num, write_data)

# # 写单个寄存器
# write_data = 0x10
# modbus_write_single_register(host,port,trans_id, unit_id, ref_num, write_data)


# # 写单个线圈， data只能是0xff 或者0x0
# write_data = 0xff
# modbus_write_single_coin(host,port,trans_id, unit_id, ref_num, write_data)


# # 写多个线圈

# write_data = [0x1, 0x3, 0x3]     # 设置 0x0 0x8 0x9 0x10 0x11地址的coin status 为 on
# modbus_write_multi_coins(host,port,trans_id, unit_id,  ref_num, 20,write_data)


# 读写多个寄存器
write_data = [0x100, 0x200, 0x200,0x200,0x300]
modbus_read_write_multi_registers(host,port,trans_id, unit_id, 0,6,8, write_data)