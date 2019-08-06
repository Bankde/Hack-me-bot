# Hack-me-bot
Vulnerable Line bot for demonstration and education

1. Create new LINE project.  

2. Fork this repo and deploy via Heroku  

3. Set Heroku environment as follows:  

ACCESS_TOKEN -> `{Your LINE channel access token}`  
FLAG -> `{Your flag}`  
SERVER_INFO -> 
```
Python: 3.7.1
Flask: 1.0.2
requests: 2.20.1
Server: Ubuntu 4.4.0 x86_64
Host: {Your_server_URL_here}
```

4. Set your LINE callback to your server URL  

5. Try typing `!help` to your own bot. It should work. Then start hacking from there.
