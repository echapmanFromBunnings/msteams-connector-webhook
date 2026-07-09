FROM python:3.12-alpine

RUN pip install --no-cache-dir requests

COPY send_adaptive_card.py /send_adaptive_card.py
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh /send_adaptive_card.py

ENTRYPOINT ["/entrypoint.sh"]
