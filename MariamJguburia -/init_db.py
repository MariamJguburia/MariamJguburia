from ext import app, db
from models import Place, Review, User

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(username="admin", role="Admin")
    admin.password_set("adminpass")
    admin.create()

    place1 = Place(
        title="Fraunkirche",
        known_since= 1726,
        description="Famous church in Munich",
        image="1.Frauenkirche.jpg"
    )
    place1.create()

    place2 = Place(
        title="Victoria Falls",
        known_since= 1855,
        description= "",
        image="Victoria Falls.jpg"
    )
    place2.create()

    place3 = Place(
        title="Rapa Nui",
        known_since= 1722,
        description= "Isolated statues",
        image="3.Rapa-nui.jpg"
    )
    place3.create()

    place4 = Place(
        title="Masazir lake",
        known_since= 1813,
        description= "Pink lake",
        image="4.Masazir-lake.jpg"
    )
    place4.create()