from setuptools import setup

setup(
    name='snapify',
    version='0.1',
    py_modules=['snapify'],
	packages=['snapify'],
	description='Command line tool for taking snapshots of webpage',
	author_email='void.aby@gmail.com',
	author='Abhijeet Mohan',
	license='MIT',
    include_package_data=True,
    install_requires=[
        'click',
	'unirest',
	'pyperclip',
    ],
    entry_points='''
	[console_scripts]
    snapify=snapify:snapify
    '''
  )
