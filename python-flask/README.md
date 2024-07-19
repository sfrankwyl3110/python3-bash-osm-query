#### Install python3 packages

##### Bash (assuming python is python3):
```
python -m venv venv
source venv/bin/activate
pip install flask[async] flask-sqlalchemy pymysql requests
```

#### On MySQL (MariaDB)-Server 
```
CREATE DATABASE location_app;
```

##### Access From everywhere ( WARN: Please secure with Firewall or other security mechanism for public use )
```
GRANT ALL PRIVILEGES ON location_app.* TO 'loc_user'@'%' IDENTIFIED BY 'loc_pass' WITH GRANT OPTION;
```

##### Localhost Only
```
GRANT ALL PRIVILEGES ON location_app.* TO 'loc_user'@'localhost' IDENTIFIED BY 'loc_pass' WITH GRANT OPTION;
```

#### RUN - simple
```
python get_elevations.py
```

#### RUN - Flask
```
python -m flask --app get_elevations:app run --port 5005 --debug
```

###### TODO:
 - Docker-Compose
