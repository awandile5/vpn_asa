import sys
import os
import netmiko
from netmiko import ConnectHandler
from datetime import datetime
import telnetlib
host = "100.100.100.10"
cisco_asa1 = {
    'device_type': 'cisco_asa',
    'host': '100.100.100.10',
    'username': 'amol',
    'password': 'amol',
    'secret': '',
}
cisco_asa2 = {
    'device_type': 'cisco_asa',
    'host': '100.100.100.12',
    'username': 'amol',
    'password': 'amol',
    'secret': '',
}

'#asa1 configuration 10.0.0.1'
net_connect = ConnectHandler(**cisco_asa1)
net_connect.find_prompt()
output = net_connect.send_command("show ip add")
print(output)
config_commands = [
    'terminal width 511 \n',
    'terminal pager 2000 \n'
    ]
output0 = net_connect.send_config_set(config_commands)
print(output0)

config_commands = [
    'interface gigabitEthernet 0/2 \n',
    'ip add 10.0.0.1 255.255.255.0 \n',
    'nameif OUTSIDE \n',
    'no shut \n'
    ]
output1 = net_connect.send_config_set(config_commands)
print(output1)

config_commands = [
    'interface gigabitEthernet 0/1 \n',
    'ip add 192.168.1.1 255.255.255.0 \n',
    'nameif INSIDE \n',
    'no shut \n'
    ]
output2 = net_connect.send_config_set(config_commands)
print(output2)
config_commands = [
    'clear Console-output \n'
    ]
output3 = net_connect.send_config_set(config_commands)
print(output3)

config_commands = [
'object network obj_local \n',
'subnet 192.168.1.0 255.255.255.0 \n',
'exit \n',
'object network obj_remote \n ',
'subnet 192.168.2.0 255.255.255.0 \n',
'exit' ]
output3 = net_connect.send_config_set(config_commands)
print(output3)
config_commands = [ 
'access-list inet per ip 192.168.1.0 255.255.255.0 any \n',
'ACCESS-LIST LAN12 EXTENDED PERMIT IP 192.168.1.0 255.255.255.0 192.168.2.0 255.255.255.0 \n'
]
output4 = net_connect.send_config_set(config_commands)
print(output4)
config_commands = [ 
'nat (inside,outside) 100 source dynamic any interface \n',
'nat (INSIDE,OUTSIDE) 1 source static obj_local obj_local destination static obj_remote obj_remote \n',
]
output5 = net_connect.send_config_set(config_commands)
print(output5)

config_commands = [
'CRYPTO IKEV1 POLICY 10 \n',
'HASH md5 \n',
'AUTHENTICATION pre-share \n',
'GROUP 2 \n',
'ENCRYPTION 3des \n',
'exit \n',
'TUNNEL-GROUP 20.0.0.1 type ipsec-l2l \n',
'TUNNEL-GROUP 20.0.0.1 IPSEC-ATTRIBUTES \n',
'IKEV1 PRE-SHARED-KEY cisco \n',
'exit \n',
'CRYPTO IKEV1 ENABLE OUTSIDE \n',
'crypto ipsec ikev1 transform-set tset esp-sha-hmac esp-3des \n ',
'CRYPTO MAP CMAP 10 MATCH Address LAN12 \n ',
'CRYPTO MAP CMAP 10 SET TRANSFORM-SET tset \n ',
'CRYPTO MAP CMAP 10 SET PEER 20.0.0.1 \n ',
'CRYPTO MAP CMAP INTERFACE OUTSIDE '
]
output6 = net_connect.send_config_set(config_commands)
print(output6)

f= open("asa1.txt","w+")
f.write(output0+output1+output2+output3+output4+output5+output6)
f.close()



'asa2'
net_connect = ConnectHandler(**cisco_asa2)
net_connect.find_prompt()
output = net_connect.send_command("show ip add")
print(output)

config_commands = [
'terminal width 511 \n',
'terminal pager 20000 \n',
'interface gigabitEthernet 0/2 \n',
'ip add 20.0.0.1 255.255.255.0 \n',
'nameif OUTSIDE \n',
'no shut \n',
'interface gigabitEthernet 0/1 \n',
'ip add 192.168.2.1 255.255.255.0 \n',
'nameif INSIDE \n',
'no shut \n'
]
output0 = net_connect.send_config_set(config_commands)
print(output0)

config_commands = [
'object network obj_remote \n',
'subnet 192.168.1.0 255.255.255.0 \n',
'exit \n',
'object network obj_local \n ',
'subnet 192.168.2.0 255.255.255.0 \n',
'exit \n'
]
output1 = net_connect.send_config_set(config_commands)
print(output1)

config_commands = [
'access-list inet per ip 192.168.2.0 255.255.255.0 any \n',
'ACCESS-LIST LAN12 EXTENDED PERMIT IP 192.168.2.0 255.255.255.0 192.168.1.0 255.255.255.0 \n '
]
output2 = net_connect.send_config_set(config_commands)
print(output2)

config_commands = [
'nat (inside,outside) 100 source dynamic any interface \n',
'nat (INSIDE,OUTSIDE) 1 source static obj_local obj_local destination static obj_remote obj_remote \n'
]
output3 = net_connect.send_config_set(config_commands)
print(output3)

config_commands = [
'CRYPTO IKEV1 POLICY 10 \n',
'HASH md5 \n',
'AUTHENTICATION pre-share \n',
'GROUP 2 \n',
'ENCRYPTION 3des \n',
'exit \n'
]
output4 = net_connect.send_config_set(config_commands)
print(output4)

config_commands = [
'TUNNEL-GROUP 10.0.0.1 type ipsec-l2l \n',
'TUNNEL-GROUP 10.0.0.1 IPSEC-ATTRIBUTES \n',
'IKEV1 PRE-SHARED-KEY cisco \n',
'exit \n'
]
output5 = net_connect.send_config_set(config_commands)
print(output5)

config_commands = [
'CRYPTO IKEV1 ENABLE OUTSIDE \n',
'crypto ipsec ikev1 transform-set tset esp-sha-hmac esp-3des \n ',
'CRYPTO MAP CMAP 10 MATCH Address LAN12 \n ',
'CRYPTO MAP CMAP 10 SET TRANSFORM-SET tset \n ',
'CRYPTO MAP CMAP 10 SET PEER 10.0.0.1 \n ',
'CRYPTO MAP CMAP INTERFACE OUTSIDE \n'
]

output6 = net_connect.send_config_set(config_commands)
print(output6)

f= open("asa2.txt","w+")
f.write(output0+output1+output2+output3+output4+output5+output6)
f.close()