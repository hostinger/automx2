"""
Configuration generator for Mozilla XML DOM.
See https://wiki.mozilla.org/Thunderbird:Autoconfiguration:ConfigFileFormat
"""
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import tostring

from automx2 import IDENTIFIER
from automx2 import log
from automx2.model import Domain
from automx2.model import Provider
from automx2.model import Server

type_direction_map = {
    'imap': 'incoming',
    'smtp': 'outgoing',
}


def server_element(parent: Element, server: Server) -> Element:
    direction = type_direction_map[server.type]
    element = SubElement(parent, f'{direction}Server', attrib={'type': server.type})
    SubElement(element, 'hostname').text = server.name
    SubElement(element, 'port').text = str(server.port)
    SubElement(element, 'socketType').text = server.socket_type
    SubElement(element, 'username').text = server.user_name
    SubElement(element, 'authentication').text = server.authentication
    return element


def client_config(domain_name: str) -> object:
    root = Element('clientConfig', attrib={'version': '1.1'})
    domain: Domain = Domain.query.filter_by(name=domain_name).first()
    if domain:
        provider: Provider = domain.provider
        id_attribute = f'{IDENTIFIER}-{provider.id}'
        provider_element = SubElement(root, 'emailProvider', attrib={'id': id_attribute})
        SubElement(provider_element, 'identity')  # Deliberately left empty
        for provider_domain in provider.domains:
            SubElement(provider_element, 'domain').text = provider_domain.name
        SubElement(provider_element, 'displayName').text = provider.name
        SubElement(provider_element, 'displayShortName').text = provider.short_name
        for server in domain.servers:
            if server.type in type_direction_map:
                server_element(provider_element, server)
            else:
                log.error(f'Unexpected server type "{server.type}"')
    else:
        log.error(f'No provider for domain "{domain_name}"')
    data = tostring(root, 'UTF-8')
    return data