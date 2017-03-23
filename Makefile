.PHONY: test clean release

clean:
	rm -rf build dist django_bootstrap_components.egg-info

release:
	python setup.py sdist bdist_wheel upload
