import pyshark

def extract_identification_field(pcap_file, start_packet, end_packet):
    # Load pcap file
    cap = pyshark.FileCapture(pcap_file)

    # Initialize packet counter
    packet_number = 0

    # Iterate through all packets and selectively process
    ids = []
    for packet in cap:
        packet_number += 1

        # Process packets only in the desired range
        if start_packet <= packet_number <= end_packet:
            try:
                # Access the IP layer and print the Identification field
                ip_layer = packet.ip
                # print(f"Packet Number {packet_number}: Identification = {ip_layer.id}")
                ids.append(ip_layer.id)
            except AttributeError:
                # If there is no IP layer in the packet
                print(f"Packet Number {packet_number}: No IP layer available.")

        # Break the loop once past the end packet
        if packet_number > end_packet:
            break

    # Close the capture file properly
    cap.close()

    return ids


if __name__ == "__main__":
    pcap_file = 'chall.pcapng'
    start_packet = 265
    end_packet = 305
    ids = extract_identification_field(pcap_file, start_packet, end_packet)

    # each encoded message is a number n * k where k is 2 digits and n is the original message
    # brute force approach to find a k where k divides n for every n in message
    for i in range(99, 10, -1):
        out = ""
        for id in ids:
            id = int(id, 16)
            if id % i != 0:
                break
            out += chr(id // i)
        else:
            if 'csawctf' in out:
                print(out) # csawctf{licen$e_t0_tr@nsmit_c0vertTCP$$$}

