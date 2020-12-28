FROM telegraf:1.16.2 AS builder


# RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
#    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends iputils-ping snmp procps lm-sensors mtr-tiny && \
#    rm -rf /var/lib/apt/lists/*

RUN apt-get update \
     && apt-get --no-install-recommends -y install \
         python3 python3-requests python3-pycryptodome


#FROM python
#CMD [ "pip", "install", "pycryptodome==3.3" ]

#RUN apk add --no-cache --virtual .build-deps python3

EXPOSE 8125/udp 8092/udp 8094

ENTRYPOINT ["/entrypoint.sh"]
CMD ["telegraf"]

# and our very own config-file
COPY telegraf.conf /etc/telegraf/telegraf.conf

# Kostal API read script
COPY readKostal.py /readKostal.py
