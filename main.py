from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def render_index() -> str:
    return render_template('index.html')


@app.route('/registration.html')
def render_registration() -> str:
    return render_template('registration.html')


if __name__ == '__main__':
    app.run()
