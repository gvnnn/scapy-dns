FROM registry.access.redhat.com/ubi8/ubi-minimal:8.10

RUN microdnf install python3 && pip3 install scapy

COPY entrypoint.py .

USER 0

ENTRYPOINT ["./entrypoint.py"]

