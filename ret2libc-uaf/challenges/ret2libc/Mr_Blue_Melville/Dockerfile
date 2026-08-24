FROM debian:12-slim

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

RUN useradd -m blue
WORKDIR /home/blue

COPY chall /home/blue/chall
COPY flag.txt /home/blue/flag.txt

RUN chown -R root:root  /home/blue
RUN chmod -R 555        /home/blue

USER blue

EXPOSE 4920
ENTRYPOINT ["socat", "TCP-LISTEN:4920,reuseaddr,fork", "EXEC:/home/blue/chall,stderr"]
