from canari.maltego.transform import Transform

from yetigo.transforms.entities import Hostname, Ip
from yetigo.transforms.utils import run_oneshot, do_pdns_pt, do_get_malware_pt


class PTPassiveDNSByDomain(Transform):

    input_type = Hostname
    display_name = '[YT] PT Passive DNS by Domain'

    def do_transform(self, request, response, config):
        entity = request.entity
        res = run_oneshot('PassiveTotal Passive DNS', request, config)
        return do_pdns_pt(res, entity, response)


class PTPassiveDNSByIP(Transform):

    input_type = Ip
    display_name = '[YT] PT Passive DNS by IP'

    def do_transform(self, request, response, config):
        entity = request.entity
        res = run_oneshot('PassiveTotal Passive DNS', request, config)
        return do_pdns_pt(res, entity, response)


class PTReverseNS(Transform):
    input_type = Hostname
    display_name = '[YT] PT Reverse NS'

    def do_transform(self, request, response, config):
        entity = request.entity
        res = run_oneshot('PassiveTotal Passive DNS', request, config)
        for item in res['nodes']:
            entity_add = Ip(item['value'])
            entity_add.link_label = 'Server NS'
            response += entity_add
        return response


class PTGetMalwareByHostname(Transform):
    input_type = Hostname
    display_name = '[YT] PT Get Malware by Hostname'

    def do_transform(self, request, response, config):
        entity = request.entity
        res = run_oneshot('Get Malware', request, config)
        return do_get_malware_pt(res, entity, response)


class PTGetMalwareByIP(Transform):
    input_type = Ip
    display_name = '[YT] PT Get Malware by IP'

    def do_transform(self, request, response, config):
        entity = request.entity
        res = run_oneshot('Get Malware', request, config)
        return do_get_malware_pt(res, entity, response)


class PTGetSubdomains(Transform):
    input_type = Hostname
    display_name = '[YT] PT Get Subdomains'

    def do_transform(self, request, response, config):
        entity = request.entity
        res = run_oneshot('Get Subdomains', request, config)

        for item in res['nodes']:
            if entity.value != item['value']:
                h = Hostname(item['value'])
                h.link_label = 'PT Subdomains'
                response += h
        return response
