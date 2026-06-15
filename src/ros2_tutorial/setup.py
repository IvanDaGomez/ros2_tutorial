from setuptools import find_packages, setup

package_name = 'ros2_tutorial'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='ubuntu@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'service_node = ros2_tutorial.service_node:main',
            'client_service_node = ros2_tutorial.client_service_node:main',
            'action_service_node = ros2_tutorial.action_service_node:main',
            'action_client_node = ros2_tutorial.action_client_node:main',
        ],
    },
)
