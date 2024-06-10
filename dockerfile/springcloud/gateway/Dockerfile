FROM azul/zulu-openjdk-alpine:21-jre-headless-latest
ADD gateway.jar /app/
ADD start.sh /
WORKDIR /app
RUN chmod +x /start.sh
EXPOSE 9000
ENV CONSUL_HOST=127.0.0.1
ENV CONSUL_PORT=8500
CMD ["/start.sh"]