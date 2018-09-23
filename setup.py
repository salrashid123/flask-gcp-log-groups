import setuptools
import io
import os


package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, 'README.rst')
with io.open(readme_filename, encoding='utf-8') as readme_file:
    readme = readme_file.read()


setuptools.setup(
    name="flask-gcp-log-groups",
    version="0.0.8",
    author="Sal Rashid",
    author_email="salrashid123@gmail.com",
    description="Python Flask logging handler to group messages on Google Cloud Platform",
    long_description=readme,
    url="https://github.com/salrashid123/flask-gcp-log-groups",
    install_requires=[
          'google-cloud-logging',
          'flask'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',

        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",

        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
    ],
)
