import time
import random
import http.server
import interactions
import threading

# settings
HTTP_HOST = '0.0.0.0'
HTTP_PORT = 1180
BOT_TOEKN = '<token>'

# global vars
GPWD = ''
GBOT = None

@interactions.listen()
async def on_ready():
    global GBOT
    print(f'Bot online: {GBOT.app.name}')

@interactions.slash_command(
    name='otpwd',
    description='Generate one-time password',
)
async def gen_pwd(ctx):
    global GPWD
    pwd = random.sample('0123456789', 6)
    GPWD = ''.join(pwd)
    rsp = f'Gen one-time password: {GPWD}'
    await ctx.respond(rsp)
    print(rsp)

class otpwd_web_handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        global GPWD
        pwd = GPWD
        GPWD = ''
        self.wfile.write(bytes(pwd, 'utf-8'))
        if pwd == '':
            pwd = "''"
        print(f'Got one-time password: {pwd}')

def otpwd_bot():
    global GBOT
    intents = interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT
    GBOT = interactions.Client(intents=intents)
    GBOT.start(BOT_TOEKN)

def otpwd_web():
    global HTTP_HOST, HTTP_PORT
    print(f'OTP api listen: {HTTP_HOST}:{HTTP_PORT}')
    server = http.server.ThreadingHTTPServer((HTTP_HOST, HTTP_PORT), otpwd_web_handler)
    server.serve_forever()

t1 = threading.Thread(target=otpwd_bot)
t2 = threading.Thread(target=otpwd_web)
t1.start()
t2.start()
t1.join()
t2.join()

