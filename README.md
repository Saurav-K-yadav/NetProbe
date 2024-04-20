# DoS-Detection-using-BLSTM
## TESTBED SETUP :hammer:	
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
   - The websites content is added at /var/www/html. Do sudo systemctl restart apache2 after changing it
       
## REQUIREMENTS FOR DEMONSTRATION :toolbox:

- create virtual environment using Python 3.10.14 as venv for predictions
  - python3 -m venv ${NAME OF VIRTUAL ENV}
  - pip install -r requirements_main.text
  
- create virtual environment using Python 3.8.10 as venv for running cicflowmeter
   - python3 -m venv ($NAME OF CIC VIRTUAL ENV)
   - pip install -r requirements_cicflowmeter.text

## INSTALLATION :hammer_and_wrench:	
   ### Cicflowmeter
   -  Activate virtual env using ```source ${CIC VIRTUAL ENV}/bin/activate```
      -   Navigate to cicflowmeter directory
      -   run ```python3 setup.py```

## TO SIMULATE :gear:
- activate virtual environment using source ($NAME OF VIRTUAL ENV)/bin/activate
- python3 main.py
  
## FIREWALL(UFW) SETUP BEFORE SIMULATION :shield:
- sudo ufw enable
- sudo ufw allow http
- sudo ufw status verbose( To see ufw status)
- To reset the previous rules
     - sudo ufw reset
     - sudo ufw enable
     - sudo ufw allow http
- To see the ipaddress which are already blocked for outgoing traffic by apache2 navigate to /etc/apache2/sites-available/${domain name example netprobe}.conf and deny from list if not present then all ips are allowed
  
## ATTACK SIMULATION :crossed_swords:
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
> Simulate attacks only in controlled environments with proper authorization, as unauthorized use may have severe legal consequences

   











