from setuptools import setup, find_packages

setup(
    name='blackjack',
    version='0.1',
    url='https://github.com/mkuja/jokujuttu',
    license='BSD',
    author='Mikko Kujala',
    author_email='m.kujala@live.com',
    description='Blackjack game and HTTP API for it.',
    packages=find_packages(),
    install_requires=[
        'python-dotenv>=0.13',
        'Flask>=1.1',
        'Flask-RESTful>=0.3.8',
        'Flask-JWT-Extended>=3.24',
        'psycopg2-binary>=2.8.5',
        'pip>=20.1.1'
    ]
)
