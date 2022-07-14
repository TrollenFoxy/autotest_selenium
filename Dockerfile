FROM docker-repo.infra.b-pl.pro/common/python:3.9

# Создаем рабочие директории образа
WORKDIR /app
COPY . ./


# устанавливаем наши сертификаты(БП)
RUN curl http://ipa-1-cr.idm.balance-pl.ru/ipa/config/ca.crt >> /usr/local/share/ca-certificates/cacert.idm.balance-pl.ru.crt && \
    update-ca-certificates
ENV REQUESTS_CA_BUNDLE /usr/local/share/ca-certificates/cacert.idm.balance-pl.ru.crt


# устанавливаем библиотеки необходимые для работы проекта (виртуальное окружение)
RUN pip install --upgrade pip && \
    pip install -r requirements.txt


## если нужна определенная версия связки хром + драйвер, запускаем этот код
########################################################################################################################
#RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
#RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
#
## Update the package list and install chrome
#RUN apt-get update -y
#RUN apt-get install -y google-chrome-stable
#
## Set up Chromedriver Environment variables
#ENV CHROMEDRIVER_VERSION 100.0.4896.60
#ENV CHROMEDRIVER_DIR /chromedriver
#RUN mkdir $CHROMEDRIVER_DIR
#
## Download and install Chromedriver
#RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
#RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR
#
## Put Chromedriver into the PATH
#ENV PATH $CHROMEDRIVER_DIR:$PATH
########################################################################################################################


# если нужна просто последняя версия связки хром + драйвер, запускаем этот код
########################################################################################################################
# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -  && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get -y update  && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# install chromedriver
RUN apt-get install -yqq unzip && \
    rm -rf /var/lib/apt/lists/* && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip  && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
########################################################################################################################


# устанавливаем номер выхода монитора
ENV DISPLAY=:99
