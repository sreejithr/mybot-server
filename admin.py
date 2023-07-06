from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from server import Bot, Note, db

app = Flask(__name__)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='MyBots', template_mode='bootstrap3')
# Add administrative views here
admin.add_view(ModelView(Bot, db.session))
admin.add_view(ModelView(Note, db.session))

app.run()