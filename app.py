from flask import Flask, render_template
import data_manager
app = Flask(__name__)


@app.route('/')
def index():
    headers = data_manager.LIST_OF_QUESTIONS[0].keys()
    questions = data_manager.LIST_OF_QUESTIONS
    return render_template("index.html", headers=headers, questions=questions)


if __name__ == '__main__':
    app.run()
