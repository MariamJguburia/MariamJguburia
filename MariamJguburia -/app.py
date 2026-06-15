from ext import app, db
from models import Place, Review, User

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    from routes import *
    app.run(debug=True)