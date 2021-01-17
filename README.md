# insta-pic-api
The backend of the InstaPic test.

# Steps to set up backend
```
Setting up on a development machine
1. clone this repo
2. run 'pip install pipenv' (if pipenv is unavailable)
3. run 'pipenv install'
4. set up environment variables in .env (db connection string, secret keys)
5. run 'flask db init'
6. run 'flask db migrate -m 'message''
7. run 'flask db upgrade'
8. run 'flask run'
```
```
Setting up on a production machine (assuming ubuntu instance)
1. clone this repo
2. install python3 and pip
3. install pipenv
4. install SQL database of your choice
4. set up environment variables in .env (db connection string, secret keys)
5. run 'flask db init'
6. run 'flask db migrate -m 'message''
7. run 'flask db upgrade'
8. set up nginx
9. run 'gunicorn -i localhost:8000 -w 4 wsgi:app
```

# nginx config
```
server {
    # listen on port 80 (http)
    listen 80;
    server_name _;
    location ~ ^/api/ {
	proxy_pass http://127.0.0.1:8000;
	proxy_redirect off;
    }
    location / {
	root /var/www/html/insta-pic-vue/dist;
	try_files $uri $uri/ /index.html;
    }
    location /swaggerui/ {
        proxy_pass http://localhost:8000;
    	proxy_set_header  Host $host;
    	proxy_set_header  X-Real-IP $remote_addr;
    	proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for;
    	proxy_set_header  X-Forwarded-Host $server_name;
    }
    location /swagger.json {
	proxy_pass http://localhost:8000;
	proxy_set_header Host $host;
	proxy_set_header X-Real-IP $remote_addr;
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	proxy_set_header X-Forwarded-Host $server_name;
     }
}
```
