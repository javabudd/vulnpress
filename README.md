┌∩┐(◣_◢)┌∩┐

# Dependencies

- [Python >= 3.4](https://www.python.org/downloads)

- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc) `pip install beautifulsoup4`

- [Tornado](http://www.tornadoweb.org/en/stable) `pip install tornado`

- [SQLAlchemy](http://www.sqlalchemy.org) `pip install sqlalchemy`

# Usage
```
python vulnpress.py
```

# [Vagrant](https://www.vagrantup.com/docs/cli)
```
vagrant up
vagrant reload
vagrant halt
vagrant provision
```

# [Docker](https://www.docker.com)
```
docker build -t vulnpress/webserver .
docker run -p 80:80 -p 3306:3306 -d vulnpress/webserver
```
