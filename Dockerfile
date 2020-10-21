FROM l4t:latest

# Definition of a Device & Service
ENV POSITION=Runtime \
    SERVICE=select-picture-sequentially \
    AION_HOME=/var/lib/aion

# Setup Directoties
RUN mkdir -p ${AION_HOME}/$POSITION/$SERVICE
WORKDIR ${AION_HOME}/$POSITION/$SERVICE/

ADD main.py .

CMD ["python3", "-u", "main.py"]