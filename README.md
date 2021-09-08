# ICU-Dash

SDI Project, Porti & Donike  
  
# Server
Currently running under [www.icu-dashboard.donike.net]
Data paths of files are relative, this repo can therefore be cloned. Bu it needs to be run in the right environment.

  
Screenshot:  
![example_image](https://www.donike.net/wp-content/uploads/screencapture-icu-dashboard-donike-net-2021-06-26-17_30_17.jpg "Screenshot")


# Relevance of ICU Occupancy Rates  
Intensive Care Units (ICUs) are hospitals’ departments that host patients in critical condition. These units are crucial in managing the COVID-19 pandemic, since patients in critical condition need to be ventilated. Additionally to the COVID-19 incident rate, the ICU occupancy rate provides important insights about how the COVID-19 health crisis is developing and being managed. If a nation's health system is reaching it's limit and cannot take care of patients according to their condition, many preventable deaths will be the result.
The map shows the current ICU Occupancy percentage per federal state, while the graphs show the development of the absolute and relative numbers since the beginning of the pandemic. Hovering over the map with the mouse will automatically update the graphs to show the according data.
## General Information  
The ICU-Dash is a dashboard, aggregating and visualizing data of the ICU occupancy numbers and percentages from the Austrian states. The Dashboard is live and accessible.  
The Dashboard has also been published on the Open Data Austria Portal. 
![image](https://www.donike.net/wp-content/uploads/screencapture-icu-dashboard-donike-net-2021-06-26-17_30_17.jpg "image")
 
## Data Source  
The [Source](data) is scraped from the data.gov.at data provider as a *.csv* file.
## Workflow
Within the documentation folder of the repository, the *pdf* gives a detailed overview of the workflow or alternatively, the [Workflow](Workflow) page in this wiki
### Frontend
The [frontend](Frontend) is completed in Plotly Dash.  
### Backend
The [Backend](Backend) consits of an Ubuntu Server which runs an Apache Webserver. The data is scraped and manipulated via python scripts and saved in an external Postgres database hosted privately. The University-Geoserver then accesses this Database and publishes the Geoservices.



# Backend
On a Ubuntu server, a scraper gets *.csv* source file every day. The data is the manipulated and a variety of metrics calculated.  
Using a python script, a Postgres server is updated. One table containing the original csv and the calculated metrics is updated, the other table includes the geometries of the federal states of austria and the occupancy percentages for said states.  
This DB table is then accessed by the Geoserver, which publishes the OGC formats based on the database.
![WhatsApp_Image_2021-06-22_at_18.48.52](uploads/2083b522f35bcaad0a0a82db2507fad3/WhatsApp_Image_2021-06-22_at_18.48.52.jpeg)
  
The takes the following route:  
After being scraped from the open Data Portal to the server, it is manipulated and then transfered to the Postgres server. From there, the geoserver accesses it and publishes the data as a WFS. The website application itself accesses the current ICU occupancy rate of the states from the Geoserver. Since the Geoserver is the only piece not under our control, if the fetching of the data fails the website can still access the data directly, since it has passed via the server before.
![WhatsApp_Image_2021-06-22_at_19.12.50](uploads/afca644506ce3d98cb3e197d5bc0b439/WhatsApp_Image_2021-06-22_at_19.12.50.jpeg)
## Flask installation
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install apache2 mysql-client mysql-server
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6 python3.6-dev
curl https://bootstrap.pypa.io/get-pip.py | sudo python3.6
sudo apt-get install apache2 apache2-dev
pip3.6 install mod_wsgi
mod_wsgi-express module-config

returns:
LoadModule wsgi_module "/usr/local/lib/python3.6/dist-packages/mod_wsgi/server/mod_wsgi-py36.cpython-36m-x86_64-linux-gnu.so"
WSGIPythonHome "/usr"

paste return in:
nano /etc/apache2/mods-available/wsgi.load

a2enmod wsgi
service apache2 restart
pip3.6 install Flask

#paste server info into
nano /etc/apache2/sites-available/FlaskApp.conf

Paste this into nano
<VirtualHost *:80>
                ServerName 192.168.0.1 # Server IP or Domain Name here
                ServerAdmin youremail@email.com
                WSGIScriptAlias / /var/www/FlaskApp/FlaskApp.wsgi
                <Directory /var/www/FlaskApp/FlaskApp/>
                        Order allow,deny
                        Allow from all
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/FlaskApp-error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/FlaskApp-access.log combined
</VirtualHost>

sudo a2ensite FlaskApp
service apache2 reload

mkdir /var/www/FlaskApp
cd /var/www/FlaskApp
nano FlaskApp.wsgi

 Paste dummy app into nano
!/usr/bin/python3.6
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")


from FlaskApp import app as application

mkdir FlaskApp cd FlaskApp
nano __init__.py

from flask import Flask
import sys

app = Flask(__name__)

@app.route('/')
def homepage():
    return "Hi there, how ya doin?"

if __name__ == "__main__":
    app.run()


service apache2 reload 

## Python Env
 
attrs==21.2.0
Brotli==1.0.9
certifi==2020.12.5
chardet==4.0.0
click==7.1.2
click-plugins==1.1.1
cligj==0.7.1
dash==1.20.0
dash-core-components==1.16.0
dash-html-components==1.1.3
dash-renderer==1.9.1
dash-table==4.11.3
dataclasses==0.8
DateTime==4.3
Fiona==1.8.19
Flask==2.0.0
Flask-Compress==1.9.0
future==0.18.2
geojson==2.5.0
geopandas==0.9.0
idna==2.10
itsdangerous==2.0.0
Jinja2==3.0.0
lxml==4.6.3
MarkupSafe==2.0.0
mod-wsgi==4.7.1
munch==2.5.0
numpy==1.19.5
pandas==1.1.5
pandas-datareader==0.9.0
plotly==4.14.3
pycurl==7.43.0
pygobject==3.20.0
pyproj==3.0.1
python-apt==1.1.0b1+ubuntu0.16.4.11
python-dateutil==2.8.1
pytz==2021.1
requests==2.25.1
retrying==1.3.3
Shapely==1.7.1
six==1.16.0
unattended-upgrades==0.1
urllib3==1.26.4

# Source
The Austrian Open Data Portal provides a *csv*, containing the ICU and testing Information of the federal states of Austria. The data is formated as a time-series, with one entry per date and state.  
[Source](https://covid19-dashboard.ages.at/data/CovidFallzahlen)
## Data Structure
In this example, the ICU total number of ICU beds as well as the occupancy percentage are already calculated and appended to the dataframe. Additionally, the date has already been transformed to the *DateTime* format in python.
![image](https://www.donike.net/wp-content/uploads/ICU-Dash_data_mockupstructure_v2312.jpg "image")

# Frontend

The frontend consits of a Python flask application, that runs on WSGI and an Apache Webserver. Flask runs the Plotly Dash file, which is an open Source Library to create dashboards using Python. 

## Kibana Server IP & Port  
icu-dashboard.donike.net




