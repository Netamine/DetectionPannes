# Utiliser une image légère de Debian
FROM debian:latest

# Définir le répertoire de travail
WORKDIR /monitoring

# Installer wget et autres utilitaires nécessaires
RUN apt-get update && apt-get install -y \
    wget \
    tar \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Installer Prometheus
RUN wget https://github.com/prometheus/prometheus/releases/download/v2.46.0/prometheus-2.46.0.linux-amd64.tar.gz && \
    tar xvfz prometheus-2.46.0.linux-amd64.tar.gz && \
    mv prometheus-2.46.0.linux-amd64 /prometheus && \
    rm prometheus-2.46.0.linux-amd64.tar.gz

# Installer Grafana
RUN wget https://dl.grafana.com/enterprise/release/grafana-enterprise-10.0.3.linux-amd64.tar.gz && \
    tar -zxvf grafana-enterprise-10.0.3.linux-amd64.tar.gz && \
    mv grafana-10.0.3 /grafana && \
    rm grafana-enterprise-10.0.3.linux-amd64.tar.gz

# Ajouter un volume pour Grafana
VOLUME /grafana/data

# Copier les fichiers de configuration
COPY prometheus.yml /prometheus/prometheus.yml
COPY grafana.ini /grafana/conf/grafana.ini
COPY grafana/provisioning /grafana/provisioning

# Exposer les ports pour Prometheus et Grafana
EXPOSE 9090 3000

# Lancer les services Grafana et Prometheus
CMD ["/bin/sh", "-c", "/prometheus/prometheus --config.file=/prometheus/prometheus.yml & /grafana/bin/grafana-server --homepath=/grafana --config /grafana/conf/grafana.ini"]
