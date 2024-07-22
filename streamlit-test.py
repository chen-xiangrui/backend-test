import streamlit as st
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import socket

def find_free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

def main():
    st.title("Streamlit JSON Response")

    # Create a dictionary with your data
    data = {
        "message": "Hello, world"
    }

    # Convert the dictionary to a JSON string
    json_data = json.dumps(data)

    # Display the JSON data in the Streamlit app
    st.text(json_data)

    # Print the JSON data to the console for debugging
    print(f"JSON data: {json_data}")

@st.cache_data
def get_json_data():
    return {
        "message": "Hello, world"
    }

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/json_data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Add this line for CORS
            self.end_headers()
            self.wfile.write(json.dumps(get_json_data()).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port):
    server = HTTPServer(('localhost', port), RequestHandler)
    print(f"Starting server on port {port}...")
    server.serve_forever()

if __name__ == "__main__":
    port = find_free_port()
    server_thread = Thread(target=run_server, args=(port,))
    server_thread.daemon = True
    server_thread.start()

    main()




# import streamlit as st
# from flask import Flask, jsonify
# from flask_cors import CORS

# @st.cache(allow_output_mutation=True)
# def get_json_data():
#     return {
#         "message": "Hello, world"
#     }

# if __name__ == "__main__":
#     st.title("Streamlit JSON Response")

#     # Handle CORS for development purposes
#     app = Flask(__name__)
#     CORS(app)

#     @app.route('/json_data', methods=['GET'])
#     def json_data():
#         return jsonify(get_json_data())

#     app.run(port=8501)

