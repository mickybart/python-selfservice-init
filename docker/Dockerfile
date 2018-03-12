FROM python:3
EXPOSE 5000

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    curl -L https://storage.googleapis.com/kubernetes-release/release/v1.8.4/bin/linux/amd64/kubectl -o /bin/kubectl && chmod +x /bin/kubectl

COPY . .

CMD [ "python", "-u", "./run.py" ]
