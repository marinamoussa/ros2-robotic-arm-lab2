from setuptools import find_packages, setup

package_name = "arm_hardware_bridge"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="marina-hany",
    maintainer_email="marina.hanymoussa@gmail.com",
    description="Serial PWM hardware bridge for servo joints on robotic_arm",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "servo_bridge_node = arm_hardware_bridge.servo_bridge_node:main",
        ],
    },
)
