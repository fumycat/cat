import dialogs
import history

from flask import Flask
from flask import render_template, jsonify, request
app = Flask(__name__)


@app.route("/<int:user_id>")
@app.route("/<int:user_id>/<int:offset>")
def messages(user_id, offset=0):
    data = reversed(list(history.history_generator(200, user_id, offset * 200)))
    return render_template("message_history.html", items=data)


@app.route("/")
@app.route("/dialogs/<int:offset>")
def dialog_list(offset=0):
    data = dialogs.last_dialogs(40)
    return render_template("dialog_list.html", items=data)


@app.route("/local")
@app.route("/local/dialogs/<int:offset>")
def local_dialog_list(offset=0):
    data = dialogs.local_dialogs()
    return render_template("dialog_list.html", items=data)


@app.route("/local/<int:user_id>")
@app.route("/local/<int:user_id>/<int:offset>")
def local_messages(user_id, offset=0):
    data = reversed(list(history.history_generator(200, user_id, offset * 200, True)))
    return render_template("message_history.html", items=data)


if __name__ == "__main__":
    app.run()
