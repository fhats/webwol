#!/usr/bin/env python
"""
webwol

Generates wake-on-lan packets via a web interface. Useful for WOL when you're on
a different subnet, over a VPN, via an HTTP interface etc.

A secondary goal of this tool is to minimize external dependencies required, so
that deployment is trivial and can happen anywhere that Python can run. As a
result, some of this code is nasty (see: HTML templating via string interpolation,
manual response code generation, etc). This tradeoff is intentional, as the
interface for this tool is designed to be as simple as possible and therefore
can be a bit of a mess to create in the name of packaging and deployment
simplicity.
"""
import argparse
try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import codecs
import json
import logging
import re
import socket
import sys
try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote


# python3-compatible shim for checking if a thing is a string
try:
    basestring
except NameError:
    basestring = str


HTML_TEMPLATE = """
<html>
    <head>
        <title>WebWol - One-touch Wake-On-Lan Interface</title>
        <style>
            body {
                margin: 0;
                padding: 1em;
                font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
            }

            a, a:visited, a:hover {
                color: #33f;
                text-decoration: none;
            }

            .flash {
                border: 2px #fff solid;
                border-radius: 4px;
                color: #191919;
                display: inline-block;
                padding: 0.5em;
                white-space: pre-wrap;
            }

            .flash code {
                color: #39393A;
                font-size: larger;
            }

            .success {
                background-color: #0d1;
                border-color: #0a0;
            }

            .warning {
                background-color: #f0ad4e;
                border-color: #c08d1e;
            }

            .error {
                background-color: #d10;
                border-color: #a10;
            }

            .mac {
                color: #666;
                margin-left: 0.50em;
            }
        </style>
    </head>
    <body>
        <h1>WebWol</h1>
        %s
    </body>
</html>


"""


def build_webwol_request_handler(wol_config):
    class WebWolHTTPRequestHandler(BaseHTTPRequestHandler):
        wol_hosts = wol_config

        def write_response(self, response):
            self.wfile.write((HTML_TEMPLATE % response).encode('UTF-8'))

        def generate_wol_list(self):
            wol_idx = "\n".join([
                "<li><a href='/%s'>%s</a><code class='mac'>[%s]</code></li>" % (host, host, mac)
                for (host, mac) in self.wol_hosts.items()])
            return "<ul>\n%s\n</ul>" % wol_idx

        def do_GET(self):
            response = ""
            wol_host = unquote(self.path[1:])

            if self.path != "/" and wol_host in self.wol_hosts:
                # send a WOL request
                wol_mac = self.wol_hosts[wol_host]
                try:
                    send_wol(self.wol_hosts[wol_host])
                except Exception as e:
                    self.send_response(500)
                    response += "<div class='flash error'>"
                    response += "There was an error sending a wake-on-lan packet "
                    response += "to <code>%s (%s)</code>. " % (wol_host, wol_mac)
                    response += "Please try again or check the webwol "
                    response += "logs for errors."
                    response += "</div>"
                    logging.error(e)
                else:
                    self.send_response(200)
                    response += "<div class='flash success'>"
                    response += "Successfully sent wake-on-lan packet "
                    response += "to <code>%s (%s)</code>. " % (wol_host, wol_mac)
                    response += "</div>"
            elif self.path != "/":
                # Return a 404 and let the user know we couldn't find that host,
                # then write the index
                self.send_response(404)
                response += "<div class='flash warning'>"
                response += "Could not find configuration for host <code>%s</code>. " % wol_host
                response += "Choose one from the list below."
                response += "</div>"
            else:
                # Write out the index
                self.send_response(200)

            self.send_header("Content-type", "text/html")
            self.end_headers()

            response += "<p>Click a host below to send a Wake-On-Lan request.</p>"
            response += self.generate_wol_list()

            self.write_response(response)

    return WebWolHTTPRequestHandler


def format_wol(mac):
    mac = "".join(mac.split(":"))

    msg = ("FFFFFFFFFFFF%s" % (mac*16)).encode('ascii')
    raw_msg = codecs.decode(msg, "hex_codec")

    return raw_msg


def send_wol(mac):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    wol_msg = format_wol(mac)
    logging.info("Sending magic packet to 255.255.255.255 for %s" % mac)
    s.sendto(wol_msg, ("255.255.255.255", 9))


def build_http_server(args, wol_config):
    server_address = (args.bind_address, args.port)
    request_handler = build_webwol_request_handler(wol_config)
    server = HTTPServer(server_address, request_handler)
    return server


def build_arg_parser():
    description = "Presents a web interface for sending one-click wake-on-lan packets to pre-defined targets"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("config_file",
                        help="The configuration file to read wake-on-lan targets from")
    parser.add_argument("-b", "--bind-address",
                        dest="bind_address",
                        default="0.0.0.0",
                        help="The address to bind to. Default: %(default)s")
    parser.add_argument("-p", "--port",
                        dest="port",
                        type=int,
                        default=10080,
                        help="The port to listen on. Default: %(default)s")
    parser.add_argument('-v', '--verbose',
                        dest="loglevel",
                        action="store_const", const=logging.DEBUG,
                        default=logging.INFO,
                        help="Verbose output")
    return parser


def load_config(config_path):
    logging.debug("Reading configuration from %s" % config_path)
    with open(config_path) as f:
        config_contents = f.read()
        return json.loads(config_contents)


def reject_config(config):
    mac_re = re.compile("([0-9a-f]{2}:){5}[0-9a-f]{2}")
    reasons = []

    if not all((isinstance(v, basestring) for v in config.values())):
        reasons.append("""Please specify configuration as a key:value pairs of strings, like:
{
    "moonbase": "fa:ce:de:ed:01:23",
    "sadcow": "de:ad:be:ef:de:ef"
}""")
    else:
        for mac in config.values():
            if not mac_re.match(mac):
                reasons.append("""I'm bad at parsing MAC addresses and "%s" did not look like a MAC address to me.
    Please format MAC addresses like 12:34:56:78:90:ab.""" % mac)

    return reasons


if __name__ == "__main__":
    parser = build_arg_parser()
    args = parser.parse_args()

    log_format = ""
    logging.basicConfig(level=args.loglevel, format=log_format)

    wol_config = load_config(args.config_file)

    reject_reasons = reject_config(wol_config)
    if reject_reasons:
        logging.error("Failed to parse config from %s" % args.config_file)
        for reason in reject_reasons:
            logging.error(reason)
        sys.exit(1)

    server = build_http_server(args, wol_config)

    server.serve_forever()

