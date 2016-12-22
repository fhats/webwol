.PHONY: clean test

dist: deb rpm

deb:
	fpm -s dir -t deb \
		-n "python-$$(python setup.py --name)" \
		-v "$$(python setup.py --version)" \
		--depends 'python >= 2.6' \
		-a all \
		--license MIT \
		-m "Fred Hatfull <webwol@admiralfred.com>" \
		--url $$(python setup.py --url) \
		--description "$$(python setup.py --description)" \
		--deb-changelog CHANGELOG.md \
		--vendor None \
		--prefix=/usr/bin \
		webwol.py

rpm:
	fpm -s dir -t rpm \
		-n "python-$$(python setup.py --name)" \
		-v "$$(python setup.py --version)" \
		--depends 'python >= 2.6' \
		-a all \
		--license MIT \
		-m "Fred Hatfull <webwol@admiralfred.com>" \
		--url $$(python setup.py --url) \
		--description "$$(python setup.py --description)" \
		--deb-changelog CHANGELOG.md \
		--vendor None \
		--prefix=/usr/bin \
		webwol.py

clean:
	rm -rf *.pyc
	rm -f *.deb

test:
	tox
