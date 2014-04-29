from setuptools import setup

setup(
    name='snappy',
    version='0.1',
    py_modules=['snappy'],
    include_package_data=True,
    install_requires=[
        'click',
		'unirest',
		'pyperclip',
    ],
    entry_points='''
	[console_scripts]
    snappy=snappy:snappy
    ''',
)
