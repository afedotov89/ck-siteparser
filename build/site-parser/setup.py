import setuptools

setuptools.setup(
    name="site-parser",
    version="0.1.0",
    url="https://github.com/borntyping/cookiecutter-pypackage-minimal",

    author="Alexander Fedotov",
    author_email="a_fedotov89@mail.ru",

    description="Simple parser for sites",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=['feedparser', 'requests', 'lxml', 'validators'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
