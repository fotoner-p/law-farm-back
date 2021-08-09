FROM python:3.8.5
MAINTAINER Fotone <jaemuon5582@gmail.com>

ENV MECAB_VERSION mecab-0.996-ko-0.9.2
ENV MECAB_DICT_VERSION mecab-ko-dic-2.1.1-20180720
ENV MECAB_PYTHON_VERSION mecab-python-0.996

#EXPOSE 80

RUN mkdir -p /app
WORKDIR /app

ADD ./ ./

RUN apt-get clean
RUN apt-get update -y && apt-get install -y openjdk-11-jdk g++

RUN pip install --upgrade pip && pip install -r requirements.txt

# Install Mecab
RUN set -ex \
    && curl -LO https://bitbucket.org/eunjeon/mecab-ko/downloads/${MECAB_VERSION}.tar.gz \
    && tar zxvf ${MECAB_VERSION}.tar.gz \
    && cd ${MECAB_VERSION} \
    && ./configure \
    && make \
    && make check \
    && make install \
    && ldconfig

# Install Mecab Dictionay
RUN set -ex \
    && curl -LO https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/${MECAB_DICT_VERSION}.tar.gz \
    && tar zxvf ${MECAB_DICT_VERSION}.tar.gz \
#    && mv -f nnp.csv ${MECAB_DICT_VERSION}/user-dic \
    && cd ${MECAB_DICT_VERSION} \
    && ./autogen.sh \
    && ./configure \
    && make \
    && ./tools/add-userdic.sh \
    && make install \
    && ldconfig

# Install mecab-python
RUN set -ex \
    && git clone https://bitbucket.org/eunjeon/${MECAB_PYTHON_VERSION}.git \
    && cd ${MECAB_PYTHON_VERSION} \
    && python setup.py build \
    && python setup.py install


CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8000", "--reload"]
