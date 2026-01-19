def init_routes(app):
    
    @app.route('/')
    def index():
        return "Welcome to the School Portal!"

    @app.route('/students')
    def list_students():
        return "List of students will go here."
