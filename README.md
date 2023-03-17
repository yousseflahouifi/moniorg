# moniorg

## Description

By looking through CT logs an attacker can gather a lot of information about organization's infrastructure i.e. internal domains,email addresses in a completly passive manner.  
moniorg leverage certificate transparency logs to monitor for newly issued domains based on organization field in their SSL certificate .

## Installation 

```
git clone https://github.com/yousseflahouifi/moniorg.git
```

## Requirements

- Python version used : Python 3.x.  
- moniorg depends on few modules to run:
```
pip install os sys termcolor difflib json argparse
```
- To run the tool in VPS mode and continiously keep monitoring the organization you need free slack workspace , once you get it add the Incoming Webhook URL to the config.py file in the variable named posting_webhook .  
[Set up incoming webhooks for slack](https://slack.com/help/articles/115005265063-Incoming-webhooks-for-Slack)


## Usage

```
usage: moniorg.py [-h] [-a ADD] [-g GET] [-l] [-m MONITOR] [-v] orgname
```
| Short form | Long form | Description |
| :---         |  :---         |  :---         |
| -h   | --help     | Show help message and exit    |
| -a    | --add       | Add organization name to be monitored      |
| -m     | --monitor       | Monitor and see newly added domains      |
| -g     | --get       | Get a list of domains based on orgname that you are monitoring      |
| -l     | --list       | List organization names you are monitoring      |
| -v     | --vps       | Running moniorg in vps mode and send slack notification whenever a new domain is found (this option should be used along with -m)      |


## Examples :

Adding an organization name to the monitoring list :
```
python3 moniorg.py -a "VK LLC"

                         ,--
,--,--,--. ,---. ,--,--, `--' ,---. ,--.--. ,---.
|        || .-. ||      \,--.| .-. ||  .--'| .-. |
|  |  |  |' '-' '|  ||  ||  |' '-' '|  |   ' '-' '
`--`--`--' `---' `--''--'`--' `---' `--'   .`-  /
                                           `---'
     By Youssef Lahouifi
```
To see the domains gathered :

```
python3 moniorg.py -g "VK LLC"

                         ,--
,--,--,--. ,---. ,--,--, `--' ,---. ,--.--. ,---.
|        || .-. ||      \,--.| .-. ||  .--'| .-. |
|  |  |  |' '-' '|  ||  ||  |' '-' '|  |   ' '-' '
`--`--`--' `---' `--''--'`--' `---' `--'   .`-  /
                                           `---'
     By Youssef Lahouifi

[+] below is the list of domains of the company ...
gmrk.mail.ru
relap.org
relap.ru
test.mail.ru
```

To see if new domain is added :

```
python3 moniorg.py -m "VK LLC"

                         ,--
,--,--,--. ,---. ,--,--, `--' ,---. ,--.--. ,---.
|        || .-. ||      \,--.| .-. ||  .--'| .-. |
|  |  |  |' '-' '|  ||  ||  |' '-' '|  |   ' '-' '
`--`--`--' `---' `--''--'`--' `---' `--'   .`-  /
                                           `---'
     By Youssef Lahouifi

Got Nothing !
```

## Limitations 

moniorg depends on crt.sh website to find new domains and sometimes crt.sh looks like is timing out when the list of domain is huge . You just have to retry .

## Read more

[Discovering domains like never before](https://medium.com/@youssefla/discovering-domains-like-never-before-moniorg-c609b38343b5)

[Subdomain enumeration is cool , How about domain enumeration ? Part I](https://yousseflahouifi.github.io/posts/domain-enumeration/)  
[Subdomain enumeration is cool , How about domain enumeration ? Part II](https://yousseflahouifi.github.io/posts/domain-enumeration-2/)

## Feedback and issues?
If you have a feedback or issue feel free to open it in the issues section .
