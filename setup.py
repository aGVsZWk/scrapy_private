"""
项目目录的安装
在项目目录同级的文件夹下copy此文件
安装方式:在此目录下 python3 setup.py install
安装之后,pip3 freeze 就能看到模块名称和版本了
目录下会多出
build/lib,我们的代码就放在这里了
dict,压缩包,包含我们之前的代码
scrapy_plus.egg-info,其它的一些信息
"""

from os.path import dirname, join
# from pip.req import parse_requirements

from setuptools import (
    find_packages,
    setup,
)


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


with open(join(dirname(__file__), './VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name='scrapy-plus',  # 模块名称
    version=version,
    description='A mini spider framework, like Scrapy',  # 描述
    packages=find_packages(exclude=[]),
    author='luke',
    author_email='qq905713813@163.com',
    license='Apache License v2',
    package_data={'': ['*.*']},
    url='#',
    install_requires=parse_requirements("requirements.txt"),  # 所需的运行环境
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)