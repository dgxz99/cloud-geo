FROM bellsoft/liberica-runtime-container:jre-21-slim-glibc
ADD gateway.jar /app/
ADD start.sh /
WORKDIR /app
RUN chmod +x /start.sh
EXPOSE 9000
ENV CONSUL_HOST=127.0.0.1
ENV CONSUL_PORT=8500
CMD ["/start.sh"]