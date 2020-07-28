## Synthetic test utilizing NMAP and python

This is a very simple script that will execute tests against hosts specified in test_hosts.json file
Config for grafana should be in spectrum_config.py, however you can easily put it elsewhere.

Please note, this is hastly put together from bits and pieces with barely any testing. It lacks lots of things (i.e. multithreading) and may not work, but hopefully will give you at least some head start.