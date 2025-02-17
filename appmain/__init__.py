from flask import Flask

app = Flask(__name__)

app.config["SECRET_KEY"] = '62beaa04084137300e31fc24303a3833'

from appmain.routes import main
app.register_blueprint(main)

from appmain.user.routes import user
app.register_blueprint(user)

from appmain.article.routes import article
app.register_blueprint(article)