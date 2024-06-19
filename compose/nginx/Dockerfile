ARG IMAGE_TAG
FROM nginx:${IMAGE_TAG}

ARG INCOMING_PORT
ARG DOMAIN
ARG FULLCHAIN
ARG PRIVKEY
ARG DHPARAM
ARG CERTS_DIR

# Copy the default configuration file to a temporary location
COPY ./config/nginx/default.conf /tmp/default.conf

# Update the configuration file with the certificate and key
RUN sed -i "s|listen 443 ssl;|listen ${INCOMING_PORT} ssl;|g" /tmp/default.conf && \
    sed -i "s|server_name domain.example.com;|server_name ${DOMAIN};|g" /tmp/default.conf && \
    sed -i "s|ssl_certificate .*;|ssl_certificate ${CERTS_DIR}/${FULLCHAIN};|g" /tmp/default.conf && \
    sed -i "s|ssl_certificate_key .*;|ssl_certificate_key ${CERTS_DIR}/${PRIVKEY};|g" /tmp/default.conf && \
    sed -i "s|ssl_dhparam .*;|ssl_dhparam ${CERTS_DIR}/${DHPARAM};|g" /tmp/default.conf

# Move the updated configuration file to the correct location
RUN mv /tmp/default.conf /etc/nginx/conf.d/
