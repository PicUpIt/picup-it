PicUp It [![Build Status](https://drone.io/github.com/PicUpIt/picup-it/status.png)](https://drone.io/github.com/PicUpIt/picup-it/latest)
========

Introduction
------------
Sources for https://picup.it/ image sharing platform.

Installation
------------

I suggest to use virtualenv. Below is my installation script with a project
checkouted in ~/repo/


```bash
mkdir -p ~/repo
virtualenv ~/repo/python-pickup/
cd ~/repo/
git clone [[REPLACE_HERE]]
~/repo/bin/pip install -r picup/requirements.txt
cd picup/picupwebapp/
~/repo/python-pickup/bin/python manage.py syncdb
~/repo/python-pickup/bin/python manage.py runserver
```

