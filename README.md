# Garfield

![Garfield](http://www.threemoviebuffs.com/static/images/movieposters/garfield.jpg)

Garfield is and open source framework for scanning and exploiting Distributed Configuration Management Systems.
With rise of distributed configuration management systems (DCMS) or products simulating the same, we thought that this tool could help and find vulnerable instances.
The framework currently being in it's beta stage has support for Apache Zookeeper, HashiCorp Consul & Sirf, CoreOS Etcd.


Installation
============================
- Install Pip, sudo apt-get install python-setuptools;easy_install pip
- pip install -r requirements.txt 
- python garfield.py -h (For Help Options)

Sample Usage
============================
- garfield.py -ip localhost -discover consul 
- garfield.py -ip localhost -attack consul


Bugs or Queries
============================
Plse report any bugs or queries @

  - helofrancis@gmail.com [@torque59](https://twitter.com/torque59)
  - bharadwaj.machiraju@gmail.com [tunnelshade](https://twitter.com/torque59)
