from distutils.core import setup

setup(
    name='mfrpy',
    version='0.1.0',
    author='Igor Sokolov and Cory Brunson',
    author_email='jason.brunson@medicine.ufl.edu',
    scripts=[],
    url='',
    license='LICENSE.txt',
    description='Graph expansion and computations of minimal functional routes',
    long_description=open('README.md').read(),
    install_requires=[
        "python-igraph",
        "sympy"
    ],
    py_modules=["mfrpy"]
)
