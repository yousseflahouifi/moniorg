import requests
import os
import sys
from termcolor import colored
import difflib
import json
import argparse
from config import *

def banner():
    print("""
                         ,--
,--,--,--. ,---. ,--,--, `--' ,---. ,--.--. ,---.
|        || .-. ||      \,--.| .-. ||  .--'| .-. |
|  |  |  |' '-' '|  ||  ||  |' '-' '|  |   ' '-' '
`--`--`--' `---' `--''--'`--' `---' `--'   .`-  /
                                           `---'
     By Youssef Lahouifi
    """)

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a','--add',help="Add organization name to monitoring list", type=str)
    parser.add_argument('-g','--get',help="Get a list of domains based on orgname field", type=str)
    parser.add_argument('-l','--list',help="List organization names you are monitoring", action='store_true')
    parser.add_argument('-m','--monitor',help="Show new domains", type=str)
    parser.add_argument('-v','--vps',help="Send notification to slack, you should use this option with -m argument",action='store_true')
    return parser.parse_args()

def get_crtsh_domain(orgname):
    domains=[]
    url="https://crt.sh/?output=json&O="+orgname
    user_agent="Moniorg"
    try:
        r=requests.get(url,headers={'User-Agent': user_agent}, timeout=50)
    except requests.exceptions.Timeout:
        print("Timeout occurred")
        os.system("sed -i 's|{}||g' orgname.txt".format(orgname))
    try:
        if r.status_code == 200:
            jsonn=r.json()
    #json=json.loads(r)
            for i in jsonn:
                domains.append(str(i["common_name"]).replace("*.",""))
            return domains
        else:
            print("error, crt.sh doesnt return valid response...")
            exit()
    except Exception as e:
        print("error, retry please")
        exit()

def get_crtsh_domain_m(orgname):
    domains=[]
    url="https://crt.sh/?output=json&O="+orgname
    user_agent="Moniorg"
    try:
        r=requests.get(url,headers={'User-Agent': user_agent}, timeout=50)
    except requests.exceptions.Timeout:
        print("Timeout occurred")
    try:
        if r.status_code == 200:
            jsonn=r.json()
    #json=json.loads(r)
            for i in jsonn:
                domains.append(str(i["common_name"]).replace("*.",""))
            return domains
        else:
            print("error, crt.sh doesnt return valid response...")
            exit()
    except Exception as e:
        print("error, retry please")
        exit()
	
	
def add_new_company(company):
    company.replace(" ","+")
    if not os.path.isfile('./orgname.txt'):
        os.system("touch orgname.txt")
    else: pass
    with open("orgname.txt", "r+") as orgnams:
        for line in orgnams:
            if line.replace("\n","") == company:
                print(colored("Copany is already monitored","yellow"))
                sys.exit(1)
        orgnams.write(company+"\n")
    #get domains
    response=get_crtsh_domain(company)
    if response:
        with open("./out/"+company+".txt","a") as domains:
            for domain in response:
                domains.write(domain+"\n")

def list_companies():
    print(colored("[+] below is the list of monitored orgname ... ","yellow"))
    with open("orgname.txt", "r") as monitored_list:
        for comp in monitored_list:
            print(comp.replace("\n",""))

def minotor_company(company):

    # we gotta check if the needed files exist
    if not os.path.isfile("./out/"+company+".txt"):
        print(colored("The given orgname isn't monitored , you gotta add it","red"))
        sys.exit(1)

    response=get_crtsh_domain_m(company)
    if response:
        with open("./out/"+company+"_temp.txt","a") as domains:
            for domain in response:
                domains.write(domain+"\n")
        file1=open("./out/"+company+".txt",'r')
        file2=open("./out/"+company+"_temp.txt",'r')
        # diff library
        result=[]
        diff=difflib.context_diff(file1.readlines(), file2.readlines())
        changes = [l for l in diff if l.startswith('+ ')]
        for c in changes:
            c=c.replace("+ ","").replace("*","").replace("\n","")
            result.append(c)

# check if domains are new
    new_domains=[]
    if result:
        for j in range(len(result)):
            with open("./out/"+company+".txt","r+") as file:
                contents=file.read()
                if result[j] in contents:
                    pass
                else:
                    new_domains.append(result[j])

    #add domains to new file
    if result:
        i=len(result)
        while i>0:
            with open("./out/"+company+".txt","r+") as file:
                file_data=file.read()
                file.seek(0, 0)
                file.write(result[i-1]+"\n"+file_data)
                i=i-1

    # we should delete the temp file before returning resultt
    os.remove("./out/"+company+"_temp.txt")

    return new_domains

def send_notification(domains):
    if isinstance(domains, list):
        webhook_url = posting_webhook
        str="\n"
        data=str.join(domains)

        slack_data = {'text': data}
        response = requests.post(
            webhook_url,
            data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
        #error = "Request to slack returned an error {}, the response is:\n{}".format(response.status_code, response.text)
            print("there was an error sending data to slack !")
        #print(response.text)
        else:
            exit()
    else:
        webhook_url = posting_webhook
        slack_data={'text':domains}
        response = requests.post(
            webhook_url,
            data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
        #error = "Request to slack returned an error {}, the response is:\n{}".format(response.stat>
            print("there was an error sending data to slack !")
        #print(response.text)
        else:
            exit()


def list_domains(company):
    print(colored("[+] below is the list of domains of the company ... ","yellow"))
    with open("out/"+company+".txt", "r") as domains:
        for comp in domains:
            print(comp.replace("\n",""))



if __name__ == '__main__':
	banner()
	if args().list:
		list_companies()

	if args().add:
		add_new_company(args().add)

	if args().monitor:
		domains=minotor_company(args().monitor)
		if domains:
			if args().vps:
				send_notification(domains)
			else:
				for domain in domains:
                                    print(domain)
		else:
			if args().vps:
				send_notification("No new domains found !")
			else:
				print("Got Nothing !")

	if args().get:
		list_domains(args().get)



#	if args().get:
#		domains=get_crtsh_domain(args().get)
#		for i in domains:
#			print(i)
