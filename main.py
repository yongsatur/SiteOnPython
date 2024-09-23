from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, PackageLoader, select_autoescape

personal = [
    {
        "name": "Андрей Зинченко",
        "position": "Директор, фотограф",
        "image": "1.jpg"
    },
    {
        "name": "Анастасия Кузнецова",
        "position": "Штатный фотограф",
        "image": "2.jpg"
    },
    {
        "name": "Виктория Грушецкая",
        "position": "Штатный фотограф",
        "image": "3.jpg"
    },
    {
        "name": "Тамара Кузнецова",
        "position": "Администратор",
        "image": "4.jpg"
    }
]


class MySiteHandler(SimpleHTTPRequestHandler):
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
        body = self.env.get_template('team.html').render(header='Наша команда', personal=personal)
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
    httpd = HTTPServer(('', 8000), MySiteHandler)
    print('Server start...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()