from app import create_app, db

app = create_app()  # Call the create_app function to get the app instance

with app.app_context():
    db.create_all()

print("Base de datos inicializada correctamente")
