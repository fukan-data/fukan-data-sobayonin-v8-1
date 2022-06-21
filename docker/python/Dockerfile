FROM python:3.8-alpine

WORKDIR /app

RUN apk update \
    && apk add --no-cache --virtual \
        autoconf \
        bash \
        bison \
        boost-dev \
        build-base \
        cmake \
        flex \
        g++ \
        gcc \
        git \
        musl-dev \
        libressl-dev \
        linux-headers \
        jpeg-dev \
        zlib-dev \
        mariadb-dev \
        libffi-dev \
        # Add chromium and dependences
        udev \
        ttf-freefont \
        chromium \
        chromium-chromedriver \
        zlib-dev \
        mysql-client \
        mysql-dev \
    # Add Japanese font
    && mkdir noto \
    && wget -P /app/noto https://noto-website.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip \
    && unzip /app/noto/NotoSansCJKjp-hinted.zip -d /app/noto \
    && mkdir -p /usr/share/fonts/noto \
    && cp /app/noto/*.otf /usr/share/fonts/noto \
    && chmod 644 -R /usr/share/fonts/noto/ \
    && fc-cache -fv \
    && rm -rf /app/noto

RUN pip install --no-cache-dir six pytest numpy cython
RUN pip install --no-cache-dir pandas

ARG ARROW_VERSION=3.0.0
ARG ARROW_SHA1=c1fed962cddfab1966a0e03461376ebb28cf17d3
ARG ARROW_BUILD_TYPE=release

ENV ARROW_HOME=/usr/local \
    PARQUET_HOME=/usr/local

#Download and build apache-arrow
RUN mkdir /arrow \
    && wget -q https://github.com/apache/arrow/archive/apache-arrow-${ARROW_VERSION}.tar.gz -O /tmp/apache-arrow.tar.gz \
    && echo "${ARROW_SHA1} *apache-arrow.tar.gz" | sha1sum /tmp/apache-arrow.tar.gz \
    && tar -xvf /tmp/apache-arrow.tar.gz -C /arrow --strip-components 1 \
    && mkdir -p /arrow/cpp/build \
    && cd /arrow/cpp/build \
    && cmake -DCMAKE_BUILD_TYPE=$ARROW_BUILD_TYPE \
        -DOPENSSL_ROOT_DIR=/usr/local/ssl \
        -DCMAKE_INSTALL_LIBDIR=lib \
        -DCMAKE_INSTALL_PREFIX=$ARROW_HOME \
        -DARROW_WITH_BZ2=ON \
        -DARROW_WITH_ZLIB=ON \
        -DARROW_WITH_ZSTD=ON \
        -DARROW_WITH_LZ4=ON \
        -DARROW_WITH_SNAPPY=ON \
        -DARROW_PARQUET=ON \
        -DARROW_PYTHON=ON \
        -DARROW_PLASMA=ON \
        -DARROW_BUILD_TESTS=OFF \
        .. \
    && make -j$(nproc) \
    && make install \
    && cd /arrow/python \
    && python setup.py build_ext --build-type=$ARROW_BUILD_TYPE --with-parquet \
    && python setup.py install \
    && rm -rf /arrow /tmp/apache-arrow.tar.gz

# install pypi packages
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN rm /usr/bin/mysql*
COPY uwsgi.ini /app/uwsgi.ini
COPY env/develop.env /app/env/develop.env
COPY env/production.env /app/env/production.env
RUN pip freeze > newreqs.txt

CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]
