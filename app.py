from flask import Flask
import views.index


app = Flask(__name__)
app.register_blueprint(views.index.app)
app.secret_key = b'\xe9)i\x1f\xea\xe4\xdc\xc6\xf2\xe1\xe8\xd2\xaa0\x1c\x83\x19f\x00\xab\x1c\xa0V\xd4'
