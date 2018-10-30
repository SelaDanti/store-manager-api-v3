import os

from app import create_app, create_database, set_key

create_database()
set_key()

app=create_app()
port = int(os.environ.get('PORT', 5000))

app.run(host='0.0.0.0',port=port)