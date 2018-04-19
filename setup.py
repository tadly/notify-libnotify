from setuptools import setup

setup(
    name='Notify',
    version='0.0.3',
    description='libnotify client to be used with the android Notify app.',
    author='linuxwhatelse',
    author_email='info@linuxwhatelse.de',
    license='GPLv3',
    install_requires = [
        'lwe-mapper',
        'lwe-mjs',
    ],
    classifiers=[
        'Development Status :: 4 - Beta'
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords='notify android',
    py_modules = [
        'notify_libnotify'
    ],
    entry_points={
        'console_scripts' : [
            'notify-libnotify = notify_libnotify:main'
        ]
    },
    data_files=[
        ('/usr/lib/systemd/user', ['notify-libnotify.service'])
    ],
)
