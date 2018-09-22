import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask-gcp-log-groups",
    version="0.0.1",
    author="Sal Rashid",
    author_email="salrashid123@gmail.com",
    description="Python Flask logging handler to group messages on Google Cloud Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
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