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
    # BUG FIX #6: Missing dependency
    # PROBLEM: The 'tabulate' package is imported and used in update_expand.py (line 2)
    #          for displaying MFR tables, but it was not listed in install_requires.
    # IMPACT: When installing mfrpy, tabulate would not be installed automatically,
    #         causing ImportError when trying to use the prime() function with verbose=True.
    # SOLUTION: Added "tabulate" to install_requires to ensure it's installed with the package.
    install_requires=[
        "python-igraph",
        "sympy",
        "tabulate"
    ],
    py_modules=["mfrpy"]
)
