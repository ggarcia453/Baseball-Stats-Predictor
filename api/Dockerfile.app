FROM golang:1.22.4
WORKDIR /app
COPY go.mod ./
COPY go.sum ./

RUN go mod download
COPY . ./
RUN CGO_ENABLED=0 GOOS=linux go build -v -o /app/docker-gs-ping
RUN chmod +x /app/docker-gs-ping

EXPOSE 8080

CMD ["/app/docker-gs-ping"]