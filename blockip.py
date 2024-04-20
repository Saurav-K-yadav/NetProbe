import subprocess    
def blockip(ip_addresses):
    if(len(ip_addresses)==0):
    	print('Server is safe')
    	return
    # Generate a list of deny from directives for each IP address
    deny_directives = "\n".join(f"        deny from {ip}" for ip in ip_addresses)

    new_conf_content = f"""
    <VirtualHost *:80>
        ServerAdmin webmaster@localhost
        ServerName netprob
        ServerAlias www.netprob 
        DocumentRoot /var/www/netprob
        ErrorLog ${{APACHE_LOG_DIR}}/error.log
        CustomLog ${{APACHE_LOG_DIR}}/access.log combined
        <Directory /var/www/netprob>
            Options Indexes FollowSymLinks MultiViews
            AllowOverride All
            Order allow,deny 
            allow from all
	    {deny_directives}
        </Directory>    
    </VirtualHost>
    """

    conf_file_path = '/etc/apache2/sites-available/netprob.conf'

    with open(conf_file_path, 'w') as file:
        file.write(new_conf_content)
    print("netprob.conf file rewritten successfully.")
    if(len(ip_addresses)!=0):
    	for ip in ip_addresses:
        	subprocess.run(['sudo', 'ufw','insert','1', 'deny', 'from',ip,'to','any'])
    print('Firewall activated')
    # Restart Apache server
    subprocess.run(['sudo', 'service', 'apache2', 'restart'])
    print("Apache server restarted.")
