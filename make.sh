#!/bin/bash
sudo -H easy_install pip
sudo -H pip install virtualenv
virtualenv .ve
.ve/bin/pip install jinja2
