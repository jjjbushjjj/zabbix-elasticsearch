# zabbix-elasticsearch
Elasticsearch monitoring loadable module for zabbix agent

How to install:

1. Install on all nodes in your elasticsearch cluster and configure zabbix agents 
See https://github.com/vulogov/zlm-python for instructions and sources. 
   Many thanks to Mr. vulogov for this module

2. Put zbx_el.py in pymodules
Notes:
        You will need some non standart python modules to install
        * http://elasticsearch-py.readthedocs.org
        Great module for dealing with elasticsearch from python 

How to use:

module receives 2 parameters
1 - (cluster|health|node) Indicates what stats we are looking in
2 - (metric) Metric we are looking for (see Example).

Example
  Look at output of general cluster stats

  {
   "cluster_name": "bigbadcluster", 
   "timestamp": 1446029160604, 
   "nodes": {
      "count": {
         "data_only": 0, 
         "master_data": 1, 
         "total": 2, 
         "master_only": 1, 
         "client": 0
      }, 
      "fs": {
         "total_in_bytes": 914810855424, 
         "disk_read_size_in_bytes": 7183722496, 
         "free_in_bytes": 830806925312, 
         "disk_reads": 424671, 
         "disk_write_size_in_bytes": 1729414492160, 
         "disk_io_size_in_bytes": 1736598214656, 
         "disk_queue": "0", 
         "disk_service_time": "0", 
         "disk_io_op": 136863243, 
         "disk_writes": 136438572, 
         "available_in_bytes": 784731512832
      }, 
      "versions": [
         "1.5.2"
      ], 
      "process": {

      etc...

    If we want get value for disk_reads, we could pass this parameter as metric to program
    nodes.fs.disk_reads or just cluster_name to get cluster name.


Create new template for your el nodes
Add items,triggers,etc (see Zabbix documentation how to do this)

Item keys should look like:
py["zbx_el","cluster","nodes.fs.total_in_bytes"]
py["zbx_el","health","status"]

I don't provide template because I simply don't have it

While constructing your items you can test them before putting into template
Like this:
    zabbix_get -s <monitored host> -k py["zbx_el","cluster","nodes.fs.total_in_bytes"]

      

