from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/secret')


@app.route('/flag')
def flag():
    return render_template('capybara.html')

@app.route('/secret', methods=['GET', 'POST'])
def secret():
    return render_template('secret.html')

if __name__ == "__main__":
    app.run()