import os

from app import create_app, create_database, set_key

create_database('development')
set_key('development')

app=create_app('development')
port = int(os.environ.get('PORT', 5000))

app.run(host='0.0.0.0',port=port)