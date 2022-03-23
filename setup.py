from setuptools import setup

setup(
    name='mfrpy',
    version='0.1.0',
    author='Luis Sordo Vieira and Cory Brunson',
    author_email='l.sordovieira@gmail.com',
    scripts=[],
    url='',
    license='LICENSE.txt',
    description='Computations of minimal functional routes',
    long_description=open('README.txt').read(),
    install_requires=[
        "python-igraph",
        "cvxpy",
        "numpy",
    ],
)
