
### Prerequisites

```
apt-get install git python3 python3-venv
```

### Prepare and Build docker image from latest git
```
bash install.sh
```

### Create Config


### Start docker container

```
docker-compose up --build -d
```


### Prerequisites - Download Samples
```
python3 -m venv venv
source ./venv/bin/activate
pip install requests
```

### Download Datasets
```
python download_srtm.py <url-list filename>
```
