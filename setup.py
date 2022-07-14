from setuptools import find_packages, setup

setup(
    name='ads_web_api',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)