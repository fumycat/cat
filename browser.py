import dialogs

from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/<user_id>")
def messages(user_id):
    return user_id  # render_template("message_history.html")


@app.route("/")
def dialog_list():
    data = dialogs.last_dialogs(7)
    # print(data)
    return render_template("dialog_list.html", items=data)

if __name__ == "__main__":
    app.run()
