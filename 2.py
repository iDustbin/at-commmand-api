docker run --name squid_proxy -d \
  --restart=always \
  --publish 8080:8080 -p 22:22 \
  --volume /var/spool/squid \
  thelebster/docker-squid-simple-proxy


ssh -R 8080:83.78.2.174:8080 root@10.165.42.249

# not working
ssh -R 8080:localhost:8080 root@10.165.42.249

ssh -C -o ServerAliveInterval=150 -L -R 8080:proxy:8080 root@10.165.42.249

83.78.2.174

83.78.2.174
curl -x "http://83.78.2.174:22" "http://httpbin.org/ip"



curl https://ipinfo.io/ -x 83.78.2.174:8080



ssh -L 8090:localhost:8090 root@10.165.42.249