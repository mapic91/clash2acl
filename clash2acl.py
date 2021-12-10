import requests
import re

config = [
    {
        "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/reject.txt",
        "isReject": True
    },
    {
        "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/icloud.txt"
    },
    {
        "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/apple.txt"
    },
    {
        "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/google.txt"
    },
    {
        "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/direct.txt"
    },
    {
        "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/private.txt"
    },
    {
        "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/cncidr.txt"
    },
    {
        "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/lancidr.txt"
    }
]

def add_rule(rules, line):
    if line.startswith("+."):
        rules.append(r"(?:^|\.)" + line[2:].replace(r".", r"\.") + r"$")
    elif re.search(r"/([0-9]+)$", line) is not None:
        rules.append(line)
    else:
        if line.startswith("www."):
            line = line[4:]
        rules.append(r"(?:^|\.)" + line + r"$")

if __name__ == "__main__":
    rejects = []
    directs = []
    for c in config:
        if c.get("isReject", False):
            rejects.append(c["url"])
        else:
            directs.append(c["url"])
    rejects_content = []
    directs_content = []
    for url in rejects:
        print("get:" + url)
        r = requests.get(url)
        if r.status_code == 200:
            rejects_content.append([r[5:-1] for r in r.text.splitlines()[1:]])
    for url in directs:
        print("get:" + url)
        r = requests.get(url)
        if r.status_code == 200:
            directs_content.append([r[5:-1] for r in r.text.splitlines()[1:]])
    bypassACL = []
    rejectACL = []
    for c in directs_content:
        for l in c:
            add_rule(bypassACL, l)
    for c in rejects_content:
        for l in c:
            add_rule(rejectACL, l)
    with open("bypass-lan-china.acl", "w") as of:
        of.write("[proxy_all]\n\n")
        of.write("[bypass_list]\n")
        of.write("\n".join(bypassACL))
    with open("only-ban-ad.acl", "w") as of:
        of.write("[outbound_block_list]\n")
        of.write("\n".join(rejectACL))