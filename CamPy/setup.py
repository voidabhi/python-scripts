from setuptools import setup

setup(
    name='campy',
    version='0.1',
    py_modules=['campy'],
	packages=['campy'],
	description='Command line camera!',
	author_email='void.aby@gmail.com',
	author='Abhijeet Mohan',
	license='MIT',
    include_package_data=True,
    install_requires=[
        'cv',
	'curses',
	'signal',
    ]
  )
