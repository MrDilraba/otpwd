## One-time password
One-time password, discord bot.

## Usage
```bash
# install service
$ sudo cp otpwd.service /etc/systemd/system/
$ sudo systemctl enable otpwd.service
$ sudo systemctl restart otpwd.service

# discord command
/otpwd

# api example
curl 'https://127.0.0.1:1800/?account=<user>&otpassword=<otpwd>'
```
