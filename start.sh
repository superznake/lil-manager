#!/bin/bash
screen -d -m -S pixelmon
cd /home/mine/tst/PokehaanCraft2-2.10.0-ServerFiles/
java -Djava.net.preferIPv4Stack=true -Xmx5G -Xms3G -jar forge-*.jar nogui