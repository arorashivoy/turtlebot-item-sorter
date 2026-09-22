from setuptools import setup

package_name = 'solution'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Shivoy Arora',
    maintainer_email='shivoy1183@gmail.com',
    description='Multi-robot item-sorting controller for TurtleBot3 Waffle Pi in Gazebo.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'controller0 = solution.robot_controller:controller0',
            'controller1 = solution.robot_controller:controller1',
            'controller2 = solution.robot_controller:controller2',
        ],
    },
)
