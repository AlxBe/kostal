# can't use latest due to https://github.com/grafana/grafana/issues/19585
FROM grafana/grafana:7.3.4

COPY ./provisioning /etc/grafana/provisioning
COPY ./dashboards /etc/grafana/dashboards

# ENV GF_AUTH_DISABLE_LOGIN_FORM "true"
# ENV GF_AUTH_ANONYMOUS_ENABLED "true"
# ENV GF_AUTH_ANONYMOUS_ORG_ROLE "Viewer"
# ENV GF_AUTH_ANONYMOUS_ORG_NAME "BB"
