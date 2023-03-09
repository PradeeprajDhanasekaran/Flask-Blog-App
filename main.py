from flaskblog import create_app

app = create_app()
from flaskblog.models import *
db.create_all()

if __name__ == '__main__':
    app.run()

    