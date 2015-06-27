PicUp It
========

Installation
------------

I suggest to use virtualenv. Below is my installation script with project checkouted in ~/repo/


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

