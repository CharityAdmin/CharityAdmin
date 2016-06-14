from __future__ import with_statement

import distribute_setup
distribute_setup.use_setuptools()

import os

# disables creation of .DS_Store files inside tarballs on Mac OS X
os.environ['COPY_EXTENDED_ATTRIBUTES_DISABLE'] = 'true'
os.environ['COPYFILE_DISABLE'] = 'true'


def autosetup():
    from setuptools import setup, find_packages
    return setup(
        name="paws-nyc",
        version="1.0",
        include_package_data=True,
        zip_safe=False,
        packages=find_packages('src'),
        package_dir={'': 'src'},
        install_requires=[
        ],
        entry_points={
            'setuptools.file_finders': [
                'git = setuptools_git:gitlsfiles',
            ],
        },
    )

if(__name__ == '__main__'):
    dist = autosetup()

