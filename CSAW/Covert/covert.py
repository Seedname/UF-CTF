from scapy.all import IP, TCP, send

key = 12
dst_ip = "142.250.64.142"
dst_port = 22
src_ip = "10.136.203.199"
src_port = 22

def encode_message(message):
    for letter in message:
        ip = IP(dst=dst_ip, src=src_ip, id=ord(letter) * key)
        tcp = TCP(sport=src_port, dport=dst_port)
        send(ip / tcp)

encode_message("hello")