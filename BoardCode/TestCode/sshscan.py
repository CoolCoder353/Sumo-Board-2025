import os
import time

s = time.time()

ip = "10.74.82."
command = "ssh -l orangepi -o ConnectTimeout=1 "
pingcommand = "ping -n 1 -w 750 "
ending = " > nul"
lst = []
for i in range(0, 256):
    print("Trying " + pingcommand + ip + str(i) + "...")
    result = os.system(pingcommand+ip+str(i)+ending)
    if result == 0:
        print("Found " + ip + str(i))
        lst.append(ip+str(i))
    else:
        print("Not found " + ip + str(i))
    print()
print("_"*80)
print(f"Found in {time.time()-s}s")
print("\n".join(lst))
