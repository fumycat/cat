import dialogs
import history

from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/<user_id>")
def messages(user_id):
    data = history.history_generator(200, user_id, 0)
    return render_template("message_history.html", items=data)


@app.route("/")
def dialog_list():
    data = dialogs.last_dialogs(7)
    return render_template("dialog_list.html", items=data)

if __name__ == "__main__":
    app.run()
