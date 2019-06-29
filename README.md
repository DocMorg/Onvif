# onvif_tester

## Installation
```bash
git clone https://github.com/ArtemyMagarin/onvif_tester.git
cd onvif_tester
virtualenv -p /usr/bin/python env
source env/bin/activate
pip install -r requirements.txt
ln -s `pwd`/env/wsdl `pwd`/env/lib/python2.7/site-packages/wsdl
python server.py
```

Enjoy!
