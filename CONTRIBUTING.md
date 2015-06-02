# Contributing to pybotgram!

If you are reading this, is because you want to help in the development of this project, and for that, we love you!

In this file you will find some helpful guidelines if you want to understand how a plugin works, the posibilities, and more things! :-)

## Topics

* [Previous considerations.](#previous-considerations)
* [Installation.](#installation)
* [Structure of a plugin.](#structure-of-a-plugin)
* [Using the utils module.](#using-the-utils-module)
* [Using the settings module.](#using-the-settings-module)


## Previous considerations

The first thing that you need to know, is that the project and all the plugins have to be writed for `python 3.4`, there is no need to compatibility in your plugins with 2.7 :)

Some operating systems have python3 as default python, like ArchLinux, but the majority still have python 2.7 as default, so, in the project we take some precautions.

When you follow the [installation](#installation) instructions, you will install python3, pip3 and virtualenv3, this is necesary, because the installation also creates a python3 local environment.

Virtualenv is a really great tool to have projects with their own dependencies isolated of the system and other projects, if you want to know more about this, check [virtualenv page](https://virtualenv.pypa.io/en/latest/)

The only thing that you need to know, is that if you are going to develop, and not only execute `./launch.sh` for use the plugin, you will have to activate the environment while you are developing.

After the installation, you need to have a directory called `env`. This is your environment! To activate it, type in the terminal:

```
source env/bin/activate
```

This will activate the environment in that terminal. Some shells give some hint to let you know if you are in a environment, for example, [zsh](http://www.zsh.org/) with [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh) give you this hint:

IN DEVELOPMENT

## Installation

First you will need to install succesfully the project, follow the instructions in the [Installation section of README.md](https://github.com/rockneurotiko/pybotgram#installation).

## Structure of a plugin

IN DEVELOPMENT

## Using the utils module

IN DEVELOPMENT

## Using the settings module
