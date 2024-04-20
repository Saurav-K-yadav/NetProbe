# NetProbe: Deep Learning-based DDoS Detection and Mitigation
![Gemini_Generated_Image_ny0t7dny0t7dny0t](https://github.com/Saurav-K-yadav/Netprobe/assets/89384618/3335c9fd-9a41-4c27-9bf5-1f0b966dc314)


## Overview
NetProbe investigates the application of deep learning for network intrusion detection, explicitly focusing on Distributed Denial-of-Service (DDoS) attacks. This project explores the efficacy of Bidirectional LSTMs with attention layers for accurate traffic classification. The models are trained on established benchmark datasets like ```CICDDoS2017``` and ```CICDDoS2019```, providing a foundation for identifying malicious patterns. We trained our model using the described architecture, applying transfer learning and an Expert model approach through ensemble modelling techniques. We optimized its performance on the ```CICDDoS2019``` dataset. NetProbe aims to contribute to the field of network security by demonstrating the effectiveness of deep learning in mitigating DoS/DDoS attacks and ensuring network service availability.
## Key Features
- ### Advanced Deep Learning Model
  NetProbe leverages cutting-edge deep learning models, specifically Bidirectional LSTMs with attention layers. These architectures offer significant advantages over traditional methods by capturing long-term dependencies in network traffic data and focusing on the most relevant features for attack identification. This enables NetProbe to effectively detect and classify various types of DDoS attacks with high accuracy, including potentially unseen attack variations.
- ### Customized Dataset for Testing and Demonstration
  For the demonstration of the project, we created a customized dataset that includes attacks like Goldeneye, Very Short Intermittent(VSI), Slow-Http and normal network requests. This comprehensive training data enables our models to differentiate between malicious and legitimate traffic effectively.
- ### Controlled Environment Evaluation
  A controlled environment was established to assess the effectiveness of NetProbe's deep learning models in real-world scenarios. This environment utilized an Apache server to simulate various DoS attacks, including Goldeneye, Very Short Intermittent (VSI), and Slow-HTTP attacks. NetProbe's performance was evaluated in realtime, allowing us to monitor its ability to detect and classify these attacks accurately. The successful detection of simulated attacks in this controlled setting provides promising evidence for NetProbe's potential to safeguard networks against real-world DDoS threats.
- ### Automated IP-based Attack Response
  NetProbe integrates with Apache2 firewall and UFW to implement an automated attack mitigation strategy. This integration empowers NetProbe to extract attacker IPs directly from captured network packets and swiftly configure UFW to block them. This real-time response minimizes the potential disruption caused by the DDoS attack.
## Testbed Setup :hammer:	
-   Install ubuntu(preferred Ubuntu 20.04.6 LTS) and kali linux for simulating attacks
-   setup [apache2](https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-20-04) <br>
       ```
       sudo apt update
       sudo apt install apache2
       sudo ufw app list
       sudo ufw allow 'Apache'
       sudo mkdir /var/www/your_domain
       sudo chown -R $USER:$USER /var/www/your_domain
       sudo chmod -R 755 /var/www/your_domain
       sudo nano /var/www/your_domain/index.html
    ```
       - add the following lines <br>
       ```
          <html>
          <head>
              <title>Welcome to Your_domain!</title>
          </head>
          <body>
                 <h1>Success!  The your_domain virtual host is working!</h1>
          </body>
         </html>
       ```
       - check status with ```sudo systemctl status apache2```<br>
       ``` sudo nano /etc/apache2/sites-available/your_domain.conf```
       -   add following lines
         <br>
    ```
          <VirtualHost *:80>
                ServerAdmin webmaster@localhost
                ServerName your_domain
                ServerAlias www.your_domain
                DocumentRoot /var/www/your_domain
                ErrorLog ${APACHE_LOG_DIR}/error.log
                CustomLog ${APACHE_LOG_DIR}/access.log combined
            </VirtualHost>
   ```

   
   sudo a2ensite your_domain.conf
   sudo a2dissite 000-default.conf
   sudo apache2ctl configtest
   sudo systemctl restart apache2
   
   ```
   - The websites content is added at ```/var/www/html```. Do ```sudo systemctl restart apache2``` after changing it
       
## Requirements For Demonstration :toolbox:

- create virtual environment using Python 3.10.14 as venv for predictions
  - ```python3 -m venv ${NAME OF VIRTUAL ENV}```
  - ```pip install -r requirements_main.text```
  
- create virtual environment using Python 3.8.10 as venv for running cicflowmeter
   - ```python3 -m venv ($NAME OF CIC VIRTUAL ENV)```
   - ```pip install -r requirements_cicflowmeter.text```

## Installation :hammer_and_wrench:	
   ### Cicflowmeter
   -  Activate virtual env using ```source ${CIC VIRTUAL ENV}/bin/activate```
      -   Navigate to cicflowmeter directory
      -   run ```python3 setup.py```

## Firewall(UFW) Setup Before Simulation :shield:
-     sudo ufw enable
-     sudo ufw allow http
-  To see ufw status
-     sudo ufw status verbose 
- To reset the previous rules
- ``` 
      sudo ufw reset
      sudo ufw enable
      sudo ufw allow http
- To see the ipaddress which are already blocked for outgoing traffic by apache2 navigate to ```/etc/apache2/sites-available/${domain name example netprobe}.conf``` and deny from list if not present then all ips are allowed
  
## Simulation :gear:
- activate virtual environment using source ($NAME OF VIRTUAL ENV)/bin/activate
- python3 main.py

## Attack Simulation :crossed_swords:
- VSI-DOS using slowloris
     - Install slowloris from [here](https://github.com/gkbrk/slowloris)
     - we will tweak slowloris to simulate VSI-DOS using<br>
                ``` python3 slowloris.py -i ${Target Ip} -p ${Target port} -s 10000 ```
- slowhttptest<br>
       ```slowhttptest -c 10000  -i 1 -r 1000 -s 8192 -t GET -u http://${target ip}:${target port}/```
- GoldenEye<br>
     - Install goldenEye from [here](https://github.com/jseidl/GoldenEye)
     - simulate attack using command <br>
            ```./goldeneye.py http://${target ip}:${target port} -w ${Number of concurrent workers} -s ${ Number of concurrent sockets }```
> [!WARNING]
> DDoS attack simulations require controlled environments and proper authorization. Unauthorized attempts may result in legal repercussions.

___

> :warning: **Caution:** 
This research project is conducted for academic and research purposes only. While the proposed methodology demonstrates promising results, its efficacy in real-world deployments may vary depending on specific network configurations and attack scenarios. Users are encouraged to conduct thorough evaluations and validations in their respective environments before implementation.
___

   











