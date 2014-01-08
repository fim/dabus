Dabus - A Gentoo Build Bot
==========================

Inspired by pourdriere

This is a build bot designed for use on Gentoo systems. Currently, you can
create/destroy chroot environments, build packages inside these environments
and also pack the environments to create stage4 images. This software is still
in very early stages of development so use at your own risk.

Requirements
-------------

 * Python 2.X (tested with 2.7)

Installation
-------------

Either clone locally by running:

```sh
git clone https://github.com/fim/dabus
```

and then install if necessary:

```sh
python setup.py build
python setup.py install
```

Or simply run:

```sh
pip install https://github.com/fim/dabus/tarball/master
```

Usage
-----
Create an environment:

```sh
> dabus create -a i686 x86lamp
```

List existing environments:

```sh
> dabus list
```

Build world with --emptytree:

```sh
> dabus build -e x86lamp -E @world
```

Build apache/mysql/php:

```sh
> dabus build -e x86lamp apache php mysql
```

Delete environment:

```sh
> dabus delete x86lamp
```

Create stage4:

```sh
> dabus pack x86lamp
```
