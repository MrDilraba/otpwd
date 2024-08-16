import random
import http.server
import interactions
import threading
from urllib.parse import urlparse, parse_qs

# settings
HTTP_HOST = '0.0.0.0'
HTTP_PORT = 1180
OTP_TIMEOUT = 30
BOT_TOEKN = '<token>'

# global vars
GPWD = {}
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
    pwd = ''.join(random.sample('0123456789', 6))
    name = ctx.user.username
    GPWD[name] = pwd
    rsp = f'Gen one-time password done, login account: {name}@{pwd}'
    await ctx.send(rsp, ephemeral=True, delete_after=OTP_TIMEOUT)
    await ctx.channel.send(rsp.replace(pwd, '\*\*\*\*\*\*'), silent=True)
    print(rsp)

class otpwd_web_handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        query = parse_qs(urlparse(self.path).query)
        account = query.get('account', [''])[0]
        otpassword = query.get('otpassword', [''])[0]

        global GPWD
        pwd = ''
        if account != '' and account in GPWD:
            pwd = GPWD[account]
        if otpassword != '' and otpassword == pwd:
            GPWD[account] = None
            print(f'Got one-time password: {pwd}')
        else:
            pwd = ''
            print(f"Got one-time password: ''")
        self.wfile.write(bytes(pwd, 'utf-8'))

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

