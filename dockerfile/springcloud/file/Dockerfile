FROM bellsoft/liberica-runtime-container:jre-21-slim-glibc
ADD file.jar /app/
ADD start.sh /
WORKDIR /app
RUN chmod +x /start.sh
EXPOSE 8800
ENV CONSUL_HOST=127.0.0.1
ENV CONSUL_PORT=8500
ENV MINIO_HOST=127.0.0.1
ENV MINIO_PORT=9000
ENV MINIO_ACCESS_KEY=""
ENV MINIO_SECRET_KEY=""
ENV MINIO_BUCKET="wps-file"
CMD ["/start.sh"]