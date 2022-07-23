## Core-Lightning Log Monitor + Rotator

Core-Lightning allows for automatic log rotation use `logrotate`.

This repo contains a barebones `lightningd` entry for logrotate. It
rotates log daily. It also calls a prerotation handler which looks for 
"BROKEN" in the logs, and emails you that day's breaks.

### Usage

1. Copy `lightningd` into `/etc/logrotate.d`
2. Update the `lightningd` to point to the correct logfile, where `parselogs.py` is and the PID file location for your lightningd daemon
3. Update `parselogs.py` with your email information (password and email to send/receive from)
4. ???
5. Have your logs rotate automatically and get emailed notifications when things break.

```
/PATH/TO/.lightning/logs/log {
	...
        prerotate
                /PATH/TO/parselogs.py
        endscript
        postrotate
                kill -HUP $(cat /PATH/TO/.lightning/lightning.pid)
	endscript
```

```parselogs.py
mailpwd = ''
send_email = ''
recv_email = ''
default_log_path = '/home/niftynei/.lightning/logs/log'
```

To test w/o executing, call `logrotate -vdf /etc/logrotate.d/lightningd`

To execute, call `logrotate -vf /etc/logrotate.d/lightningd`
