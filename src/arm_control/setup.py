from setuptools import find_packages, setup

package_name = "arm_control"

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
    description="Trajectory publisher and control nodes for robotic_arm",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "trajectory_node = arm_control.trajectory_node:main",
            "slider_trajectory_gui = arm_control.slider_trajectory_gui:main",
            "trajectory_to_gz_bridge = arm_control.trajectory_to_gz_bridge:main",
        ],
    },
)
