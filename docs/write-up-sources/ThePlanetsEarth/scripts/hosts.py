#!/bin/python3

import os
import json
import argparse

from rich.console import Console

console = Console()

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--add", action="store_true")
parser.add_argument("-r", "--remove", action="store_true")
parser.add_argument("-l", "--list", action="store_true")
parser.add_argument("-i", "--ip")
parser.add_argument("-c", "--comment", help="new line comment with \\")
parser.add_argument("-d", "--domains", help="comma seperated for multiple")

args = parser.parse_args()

comments = {}

with open("/etc/hosts", "r") as f:
    data = f.read()

parsed_hosts = {}

comment_queue = []

for i in data.splitlines():
    if i.replace(" ", "").startswith("#"):
        comment_queue.append(i)
        continue

    line_split = i.split()
    if line_split:
        ip = line_split[0]
        line_split.pop(0)
        domains = line_split

        if ip not in parsed_hosts:
            parsed_hosts[ip] = {
                "domains": []
            }

        comments[f"{ip} {domains[0]}"] = comment_queue
        comment_queue = []

        parsed_hosts[ip]["domains"].extend(domains)

if args.list:
    for key, value in parsed_hosts.items():
        console.print(f"{key}: {", ".join(value['domains'])}")

    exit()

elif args.add:
    if os.getuid() != 0:
        console.print("Needs to be ran as root or sudo to edit hosts", style="red")
        exit()

    if not args.ip or not args.domains:
        console.print("You need an IP and domain(s)", style="red")
        parser.print_help()
        exit()

    if args.ip not in parsed_hosts:
        parsed_hosts[args.ip] = {
            "domains": []
        }

    domain_split = args.domains.replace(", ", ",").split(",")

    arg_comments_split = args.comment.replace(" \\", "\\").replace("\\ ", "\\").split("\\")
    comment_queue = []

    for comment in arg_comments_split:
        if not comment.replace(" ", "").startswith("#"):
            comment = f"# {comment}"
        comment_queue.append(comment)

    comments[f"{args.ip} {domain_split[0]}"] = comment_queue

    for domain in domain_split:
        parsed_hosts[args.ip]["domains"].append(domain)

elif args.remove:
    if os.getuid() != 0:
        console.print("Needs to be ran as root or sudo to edit hosts", style="red")
        exit()

    if not args.ip:
        console.print("You need an IP atleast.", style="red")
        parser.print_help()
        exit()

    if not args.ip in parsed_hosts:
        console.print("That was already removed :3", style="cyan")
        exit()

    if not args.domains:
        parsed_hosts[args.ip] = None
    else:
        for domain in args.domains.replace(", ", ",").split(","):
            if domain in parsed_hosts[args.ip]["domains"]:
                parsed_hosts[args.ip]["domains"].remove(domain)
else:
    parser.print_help()
    exit()

hosts = []

for key, value in parsed_hosts.items():
    if value:
        for domain in value["domains"]:
            host_line = f"{key} {domain}"
            host_line_comments = comments.get(host_line)
            if host_line_comments:
                if hosts:
                    hosts.append("\n")
                hosts.append(f"{'\n'.join(host_line_comments)}")

            hosts.append(f"{host_line}")
    hosts.append("\n")

pre_hosts_str = "\n".join(hosts)

hosts_str = ""
spliter = pre_hosts_str.splitlines()

for i in range(len(spliter)):
    i_str = spliter[i]
    last_i_str = spliter[i-1]

    if i_str.strip():
        hosts_str += f"{i_str}\n"

    if not i_str.strip() and last_i_str.strip():
        hosts_str += f"{i_str}\n"
        continue

with open("/etc/hosts.bak", "w+") as f:
    f.write(data)

with open("/etc/hosts", "w+") as f:
    #json.dump(hosts, f, indent=4)
    f.write(hosts_str)


console.print("Saved new hosts :3", style="green")