# simpleiptomap
A simple tool to show an ip list on map

### Steps
1. Put all your ip adresses in the file 'iplist.txt', one ip by line
2. Run resolver.py (need python 2.7)
3. Open visualiser.html

### Exemple gen ip list from nginx logs
```bash
#!/bin/bash
cat /var/log/nginx/*.log | grep -oE '(^[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3})' > allip.txt
```
