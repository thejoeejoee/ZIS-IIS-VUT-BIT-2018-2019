deploy:
	make deploy-app
	make restart

.ONESHELL:
deploy-app:
	test -d dist || rm -rf dist/*
	rm -rf ziscz/static/*
	npm run build
	.venv/bin/python setup.py sdist
	ssh josefkolar.cz mkdir -p /tmp/deploy/
	ssh josefkolar.cz rm -rf /tmp/deploy/*
	scp dist/* josefkolar.cz:/tmp/deploy/
	ssh josefkolar.cz /home/ziscz/.venv/bin/pip uninstall -y ziscz
	ssh josefkolar.cz /home/ziscz/.venv/bin/pip install /tmp/deploy/zis*
	ssh josefkolar.cz PYTHONPATH=/home/ziscz/ /home/ziscz/.venv/bin/ziscz-manage collectstatic --noinput

	scp conf/ziscz.gunicorn.service josefkolar.cz:/etc/systemd/system/
	ssh josefkolar.cz systemctl daemon-reload;

	scp conf/zis.josefkolar.cz.conf josefkolar.cz:/etc/nginx/sites-available/
	ssh josefkolar.cz chown www-data:www-data -R /home/ziscz/

restart:
	ssh josefkolar.cz systemctl restart ziscz.gunicorn.service;
	ssh josefkolar.cz service nginx restart;


pack:
	zip -r xkavan05.zip ziscz/ doc/ webpack.config.js package.json package-lock.json setup.py settings.py.template