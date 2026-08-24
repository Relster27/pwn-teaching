FROM debian:12-slim

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf
WORKDIR /home/ctf

COPY double_trouble /home/ctf/double_trouble
COPY flag.txt /home/ctf/flag.txt

RUN chown -R root:root  /home/ctf
RUN chmod -R 555        /home/ctf

USER ctf

EXPOSE 4919
ENTRYPOINT ["socat", "TCP-LISTEN:4919,reuseaddr,fork", "EXEC:/home/ctf/double_trouble,stderr"]
