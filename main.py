from flask import Flask, render_template
from graphs import load_graph
app = Flask(__name__)


@app.route('/')
def render_main() -> str:
    load_graph()
    return render_template('index.html')


@app.route('/registration.html')
def render_registration() -> str:
    return render_template('registration.html')


@app.route('/index.html')
def render_index() -> str:
    return render_template('index.html')


@app.route('/graph.html')
def render_graph() -> str:
    return render_template('graph.html')


if __name__ == '__main__':
    app.run()
