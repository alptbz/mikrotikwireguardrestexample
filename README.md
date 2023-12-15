# Mikrotik Wireguard REST example

This repository contains an **example** script on how to programmatically add wireguard peers for an existing wireguard interface on [MikroTik RouterOS](https://help.mikrotik.com/docs/display/ROS/WireGuard).

The code is deliberately crafted for readability, ensuring easier comprehension by novice programmers.

## Features
 - [MikroTik REST API](https://help.mikrotik.com/docs/display/ROS/REST+API)
 - Calculates ip addresses for wireguard peers using configured ip address on interface
 - Creates configuration file and stores in file
 - Creates configuration QRCODE and stores it in PNG
 - Creates new wireguard key-pair using mikrotik rest api

## License
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a> and [GNU GENERAL PUBLIC LICENSE version 3](https://www.gnu.org/licenses/gpl-3.0.en.html). If there are any contradictions between the two licenses, the Attribution-NonCommercial-ShareAlike 4.0 International license governs. 