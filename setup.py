from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


extras_require = {
    'aws': ['boto']
}


install_requires = [
    'Flask>=0.7'
]


setup(
    name='Flask-Rest3',
    version='0.0.1',
    description='Flask S3 RestAPI extension',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='flask s3 json rest api bucket library',
    url='https://github.com/kmjbyrne/flask-rest3',
    author='Keith Byrne',
    author_email='keithmbyrne@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=install_requires,
    extras_require=extras_require,
    test_suite='pytest',
    tests_require=['coverage'],
    include_package_data=True,
    zip_safe=False
)