# Mozilla Load-Tester
FROM alpine:3.7

# deps
RUN apk add --update python3; \
    apk add --update python3-dev; \
    apk add --update openssl-dev; \
    apk add --update libffi-dev; \
    apk add --update build-base; \
    apk add --update git; \
    pip3 install --upgrade pip; \
    pip3 install molotov; \
    pip3 install git+https://github.com/loads/mozlotov.git; \
    pip3 install PyFxa;

WORKDIR /molotov
ADD . /molotov

# run the test
CMD URL_SERVER=$URL_SERVER molotov -c -v -d 60 api_tests.py
