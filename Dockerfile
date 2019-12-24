FROM node:12.13.1

run npm install gitbook-cli -g

COPY ["./","/root/notes/"]

run cd /root/notes && gitbook install 

CMD "cd /root/notes && gitbook serve"
