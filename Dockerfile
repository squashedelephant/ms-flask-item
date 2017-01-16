FROM squashedelephant/service_base:develop

ADD . /src/
ADD config /config/
RUN yes | pip3 install -r /config/requirements.txt

EXPOSE 80
CMD ["/usr/local/bin/dumb-init", "/usr/local/bin/start.sh"]
