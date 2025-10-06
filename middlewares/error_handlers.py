from flask import url_for

def register_error_handlers(app):
    @app.errorhandler(401)
    def handle_401_unauthorized(error):
        message = error.description if error.description != "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required." else "Ongeldige inloggegevens"
        return {
            "success": False,
            "message": message,
            "redirect": url_for("authorization.login")
        }, 401

    @app.errorhandler(403)
    def handle_403_forbidden(error):
        return {
            "success": False,
            "message": error.description,
            "redirect": url_for("authorization.login")
        }, 403

    @app.errorhandler(404)
    def handle_404_not_found(error):
        message = error.description if error.description != "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again." else "Geen resultaten gevonden"
        return {
            "success": False,
            "message": message
        }, 404

    @app.errorhandler(405)
    def handle_405_method_not_allowed(error):
        message = error.description if error.description != "The method is not allowed for the requested URL." else "Methode niet toegestaan"
        return {
            "success": False,
            "message": message
        }, 405

    @app.errorhandler(500)
    def handle_500_server_error(error):
        message = error.description if error.description != "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application." else "Server error"
        return {
            "success": False,
            "message": message
        }, 500