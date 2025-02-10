from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    package_data={
        'conscience_service': [
            'src/**/*',
            'src/*/migrations/*',
            'src/*/templates/*',
            'src/*/static/*',
            'src/requirements.txt',
            'src/manage.py',
        ],
    },
    include_package_data=True,
) 