from setuptools import setup, find_packages

setup(
    name='nightlock',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    package_data={
        'nightlock': ['configs/*.yml'], 
    },
    license='MIT',
    description='A python package that analyzes data on COVID-19',
    long_description=open('README.md').read(),
    install_requires=['numpy', 'requests', 'pyyaml', 'matplotlib', 'kaggle', 'typing', 'pytest','pytest-mock'],
    url='https://github.com/amikkuma/nightlock',
    author='Amit Kumar',
    author_email='amkumar.ca@gmail.com'
)
