from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/triangulate/<point_set_id>', methods=['GET'])
    def triangulate_endpoint(point_set_id):
        return "Not implemented", 501

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
