from setuptools import find_packages, setup

setup(
    name='netbox-object-storage',
    version='1.0.0',
    description='Netbox Plugin for Manage S3',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'netbox_object_storage': ['templates/*'],
    },
    zip_safe=False,
    entry_points={
        'netbox_plugins': [
            'netbox_object_storage = netbox_object_storage:Plugin',
        ],
    },
)