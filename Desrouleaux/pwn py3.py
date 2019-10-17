from pwn import *
import collections
import json
from pprint import pprint

def main():

    with open("incidents.json", "r") as json_file:
        incident = json.load(json_file)
    # print(json.dumps(incident, indent = 2,sort_keys=True))
    tickets = incident["tickets"]
    # pprint(tickets)
    socket = remote("2018shell.picoctf.com", "54782")
    for line in socket.recvlines(timeout=2):
        print(line.decode("utf-8"))
    # Question 1:
    sources = []
    for ticket in tickets:
        sources.append(ticket["src_ip"])
    # pprint(sources)
    common_src_id = collections.Counter(sources).most_common(1)[0]
    print(common_src_id)

    socket.send(common_src_id[0] + "\n")
    regex_result = []
    for line in socket.recvlines(timeout=2):
        regex_result = re.findall('[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+',line.decode("utf-8"))
        print(line.decode("utf-8"))

    # Question 2:
    dests_of_common_src = set()
    for ticket in tickets:
        if ticket["src_ip"] == regex_result[0]:
            dests_of_common_src.add(ticket["dst_ip"])
    print(len(dests_of_common_src))
    socket.send(str(len(dests_of_common_src)) + "\n")
    for line in socket.recvlines(timeout=2):
        print(line.decode("utf-8"))

    # Question 3:
    dst_per_files = {}
    count_unique_dst = 0
    for ticket in tickets:
        dst_per_files[ticket["file_hash"]] = []
    for ticket in tickets:
        if ticket["dst_ip"] not in dst_per_files[ticket["file_hash"]]:
            dst_per_files[ticket["file_hash"]].append(ticket["dst_ip"])
            count_unique_dst += 1

    average = format(count_unique_dst/len(dst_per_files),'.2f')
    pprint(dst_per_files)
    # print(str(average))
    socket.send(str(average) + "\n")
    print(socket.recvline_contains("}").decode("utf-8"))




if __name__ == "__main__":
    main()

