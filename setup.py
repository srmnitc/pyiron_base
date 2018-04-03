"""
Setuptools based setup module
"""
from setuptools import setup, find_packages


setup(
    name='pyiron_vasp',
    version='0.0.9',
    description='pyiron IDE plugin for VASP',
    long_description='https://www.vasp.at',

    url='https://github.com/pyiron/pyiron_vasp',
    author='Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department',
    author_email='janssen@mpie.de',
    license='BSD',

    classifiers=[

        'Development Status :: 4 - Beta',
        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
    ],

    keywords='pyiron',
    packages=find_packages(exclude=["*tests*"]),
    install_requires=['lxml',
                      'pyiron_atomistics',
                      'pyiron_dft',
                      'six']
    )
