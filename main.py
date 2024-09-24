import http.server
from jinja2 import Environment, PackageLoader, select_autoescape
import json
import os


def load_personal():
    if os.path.exists('./data/personal.json'):
        with open('./data/personal.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    return []


def send_answer(answer):
    with open('./data/answer.json', 'w', encoding='utf-8') as file:
        json.dump({"answer": answer}, file, indent=4, ensure_ascii=False)


class MySiteHandler(http.server.SimpleHTTPRequestHandler):
    env = Environment(
        loader = PackageLoader("main"),
        autoescape = select_autoescape(),
    )


    def do_GET(self):
        if self.path == '/':
            self.render_index()
        elif self.path == '/location':
            self.render_location()
        elif self.path == '/team':
            self.render_team()
        elif self.path == '/contacts':
            self.render_contacts()
        elif self.path == '/price':
            self.render_price()
        elif self.path.startswith('/media/'):
            super().do_GET()
        else:
            self.render_404()


    def do_POST(self):
        if self.path == '/send_form':
            content_length = int(self.headers['Content-Length'])
            post_data_bytes = self.rfile.read(content_length)
            post_data_string = post_data_bytes.decode('utf-8')
            list_of_post_data = post_data_string.split('\r\n')

            post_data_dict = {}

            for item in list_of_post_data:
                if item != '':
                    key, value = item.split('=')
                    post_data_dict[key] = value

            send_answer(post_data_dict)
            self.render_contacts()


    def render_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('<h1>Not Found</h1>'.encode('utf-8'))


    def render_index(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        body = self.env.get_template('index.html').render()
        self.wfile.write(body.encode('utf-8'))


    def render_location(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        body = self.env.get_template('location.html').render(header='Локации')
        self.wfile.write(body.encode('utf-8'))


    def render_team(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        print(load_personal())
        body = self.env.get_template('team.html').render(header='Наша команда', personal=load_personal())
        self.wfile.write(body.encode('utf-8'))


    def render_contacts(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        body = self.env.get_template('contacts.html').render(header='Контакты')
        self.wfile.write(body.encode('utf-8'))


    def render_price(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        body = self.env.get_template('price.html').render(header='Прайс-лист')
        self.wfile.write(body.encode('utf-8'))


def run():
    httpd = http.server.HTTPServer(('', 8000), MySiteHandler)
    print('Server start...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()