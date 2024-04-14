bind = "0.0.0.0:8080"

workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 310
keepalive = 325

errorlog = "-"
loglevel = "info"
accesslog = "-"
access_log_format = (
    '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({x-request-id}o)s"'
)
