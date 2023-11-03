# Building image
FROM python:3.11.6-slim-bullseye as compile-image
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Work image
FROM python:3.11.6-slim-bullseye
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN mkdir -p /opt/app
WORKDIR /opt
COPY app /opt/app
COPY run.py /opt
CMD python /opt/run.py