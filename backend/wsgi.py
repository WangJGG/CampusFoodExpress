from create_app import create_app, socketio

app = create_app()
"""CORS已经在init.py中配置过，如果还是不行尝试手动加response headers"""
# @app.after_request
# def add_cors_headers(response):
#     response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
#     response.headers['Access-Control-Allow-Credentials'] = 'true'
#     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, HEAD ,DELETE, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
#     # print(response.headers)
#     return response

if __name__ == "__main__":
    # app.run(debug = True)  # debug = True
    socketio.run(app, debug=True)
