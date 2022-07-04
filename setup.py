from setuptools import setup, find_packages

setup(
        name='Fichier setup',
        version='1.0',
        packages=find_packages('src'),
        package_dir={'': 'src'},
        license='UNLICENSE',
        author='Exyloss',
        description='lecteur de bases de données keepass basé sur pykeepass.'
)
