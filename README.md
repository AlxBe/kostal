# telegraf-kostal-plenticore

Read data from Kostals Plenticore hybrid inverter and make it available as a Grafana dashboard.

credits:
netzkind: https://github.com/netzkind/telegraf-kostal-modbus


## Running

To run the project as is, you will need to have a running Docker-setup available. If you do not already have one,
please check www.docker.com on how to get started.

Once you have Docker, starting this project is as simple as `docker-compose up`.

### cherry-picking

If you don't want to run this project and only want to cherry-pick configurations:

#### Telegraf + Modbus for Kostal

Please see the folder `telegraf-kostal-plenticore` for the:
* `Dockerfile` on how to create a running telegraf with an API based collection of Kostal inverter measurements
* `readKostal.py` on how to read the values from the Kostal Plenticore device
* `telegraf.conf` on how to configure telegraf for reading measurements from the Kostal Plenticore inverter

#### Grafana-Dashboard for Kostal

Please see the folder `grafana/dashboards` for a JSON-file containing a dashboard for the above telegraf configuration.
To have a graph for the sun altitude in the diagramm install the "sun and moon" datasource in grafana (https://grafana.com/grafana/plugins/fetzerch-sunandmoon-datasource)

## Configuration

If you choose to run the project as-is, you can do all of the configuration in `docker-compose.yaml`.
* Please edit the line `- "plenticore.local:10.0.3.150"` so the IP matches the IP of your Plenticore
* Edit the PASSWD="xxx" in telegraf-kostal-api\readKostal.py to your user password of the Plenticore (test the Python script directly - it shoul read the values from the Kostal Plenticore
* Please edit the two lines with `- INFLUXDB_ADMIN_PASSWORD=secret` to change the admin-password for influxdb

### Configuring the dashboard

Once Grafana is up and running, you can reach it at Port 3000 on the IP of your Docker node (When running with Docker
Toolbox on Windows, thats http://192.168.99.100:3000).

After accessing Grafana, you can also edit the contained Dashboard ("Kostal Plenticore"). To do so, please log into
Grafana with the user "admin" and the password from the docker-compose.yaml line "GF_SECURITY_ADMIN_PASSWORD=secret".

### Open
* Backup influxdb
* general beautifying
