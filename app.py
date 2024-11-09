from flask import Flask, render_template

def create_app():
    
    app = Flask(__name__)
    @app.route('/', methods=['GET','POST'])
    def index():
        return render_template('index.html')

    if __name__ == '__main__':
        app.run(debug=True)

    return app