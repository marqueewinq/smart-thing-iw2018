build:
	docker build -t flask-sample-one:latest .

run: build
	docker run -p 0.0.0.0:5000:5000 -e SECRET_KEY="smarty-thing-development-ou8n1982ndf8901ffi0f90" -e DATABASE="/db.sqlite" -e TOKEN="faeffakca91" -v `pwd`:/src/ -it flask-sample-one /bin/bash -c "python /src/wowhead/main.py  && /bin/bash"