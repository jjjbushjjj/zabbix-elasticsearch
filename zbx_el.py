#!/usr/bin/env python
""" Get metrics from elasticsearch cluster, custerwide or node """

try:
    from elasticsearch import Elasticsearch, RequestsHttpConnection
except:
    raise ImportError("You do not have required elasticsearch module")


def zbx_fail():
    print "ZBX_NOTSUPPORTED"


def xpath_get(mydict, path):
    """ Xpath like query for nested python dictionaries """
    elem = mydict
    try:
        for x in path.split("."):
            elem = elem.get(x)
    except:
        pass
    return elem


class ElMetric:
    def __init__(self,
                 hosts=['localhost'],
                 http_auth=(),
                 port=9200,
                 use_ssl=False,
                 verify_certs=False,
                 ca_certs=None,
                 client_cert=()):
        """ Make connection to elasticsearch with provided params """

        self.es = Elasticsearch(connection_class=RequestsHttpConnection,
                                hosts=hosts,
                                http_auth=http_auth,
                                port=int(port),
                                use_ssl=use_ssl,
                                verify_certs=verify_certs,
                                ca_certs=ca_certs,
                                client_cert=client_cert)

    def getMetric(self, stat=None, metric=None):
        """ Search val for metric and return it """
        if stat == 'cluster':
            """ Clusterwide stats """
            rez = self.es.cluster.stats()
        elif stat == 'node':
            """ Node stat Return info only for node we are connecting to """
            rez = self.es.nodes.info('_local')
            # for every zabbix item just construct proper items appending
            # nodes.<nodename> in front of our metric
            metric = 'nodes.' + rez['nodes'].keys()[0] + "." + metric
        elif stat == 'health':
            rez = self.es.cluster.health()
        else:
            """ Unknown param, must be cluster health or node """
            zbx_fail()

        try:
            if metric:
                a = xpath_get(rez, metric)
                return a
            else:
                return rez
        except Exception:
            """ can't find specified metric """
            zbx_fail()


def main(*args):

    # If you have some security for protection your elasticsearch nodes
    # you can configure parameters here

    client_certs = ()
    ca_bundle = ""
    server = 'localhost'
    port = 9200
    user = ''
    password = ''

    el_metric = ElMetric(hosts=[server], http_auth=(user, password),
                         port=port, use_ssl=False, verify_certs=False,
                         ca_certs=ca_bundle,
                         client_cert=client_certs)
    m = el_metric.getMetric(stat=args[1], metric=args[2])
    return str(m)
