.PHONY: test clean release

clean:
	rm -rf build dist django_bootstrap.egg-info

release:
	python setup.py sdist bdist_wheel upload
