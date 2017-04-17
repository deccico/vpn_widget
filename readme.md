# VPN Widget

Vpn Widget lets you visualize and control the status of your VPN connection from your Ubuntu desktop.
It currently supports only ExpressVPN and Ubuntu 14.04 (although it should work with other Ubuntu versions)
Support for other vpn system should be trivial, provided we have a similar sets of command line utilities.

# Motivation

## On the usage of VPNs

VPN usage is a no brainier nowadays. From people spying on us while connected to a public wifi to avoiding governments
and internet providers to get a complete record of our internet activity. Privacy is a fundamental human right
recognized in the UN Declaration of Human Rights and using a vpn connection allows us to make our connection safer
and more private,

## On this project

Inspired by the 'Get a VPN day' by the EFF, I decided to finally install one. I settled with the ExpressVPN provider.
The results and speed were good but I was missing a visual indicator to tell me whether I was connected to the VPN or
not. My internet connection is flaky sometimes...

ExpressVPN do have a nice visual control for Windows, but just a command line utility for Linux.. With some free time
and inspiration ahead of me I decided to fix that.


# The results

I have to say I'm happy with the outcome. The code is short and sweet and Python and Gtk were all I needed to use.
This is what it looks like after installed: ![screenshot](https://gitlab.com/deccico/status_ubuntu_widget/blob/master/Screenshot.png)


# Installation

An easy way to install this project is to clone it and then follow the instructions here: https://askubuntu.com/questions/48321/how-do-i-start-applications-automatically-on-login
to automatically run it every time you log in.

# Next steps

* Create an automatic installer
* Support other vpn's (but Private Internet Access has something similar...)
* Add menu to setup other ExpressVPN options like country to connect to, protocol, etc.
