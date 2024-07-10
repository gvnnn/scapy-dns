#!/usr/bin/env python3

from scapy.all import sr1, IP, UDP, DNS, DNSQR
from time import sleep
import logging
import os

dns_address = "172.30.0.10"
domain = "kubernetes.default.svc.cluster.local"
sport = 30042
freq_in_sec = 3
timeout = 1
logger = logging.getLogger(__name__)


def setup_logging():
    log_level = os.environ.get("LOG_LEVEL", "WARN").upper()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S%z'
    )


def main():
    setup_logging()

    logger.info("DNS service: %s" % dns_address)
    logger.info("source port: %d" % sport)

    last_resp_addr = None

    while True:
        ans = sr1(
                IP(dst=dns_address) /
                UDP(sport=sport, dport=53) /
                DNS(
                    rd=1,
                    qd=DNSQR(qname=domain, qtype="A")
                ),
                timeout=timeout, verbose=False
              )
        if ans:
            last_resp_addr = ans.src
            logger.info("Got response '%s' from server %s" % (ans.an.rdata, last_resp_addr))
        else:
            logger.warning("No response after %d seconds, last response was from %s" % (
                timeout,
                last_resp_addr
                ))

        sleep(freq_in_sec)


main()
