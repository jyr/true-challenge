cd /code/ && \
virtualenv env && \
. env/bin/activate && \
pip install -r requirements.txt && \
pip install git+https://github.com/bahoo/Zappa.git#egg=zappa

python /code/manage.py runserver 0.0.0.0:8000  --settings=realstate.settings.development
