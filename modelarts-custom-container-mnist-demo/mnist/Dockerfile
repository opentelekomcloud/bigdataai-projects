FROM swr.cn-north-1.myhuaweicloud.com/eiwizard/custom-gpu-cuda9-inner-moxing-cp36:1.2
# FROM swr.cn-north-1.myhuaweicloud.com/eiwizard/custom-cpu-base:1.2

ENV BUILD_PATH /root/work

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG S3_ENDPOINT


ENV AWS_ACCESS_KEY_ID ${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY ${AWS_SECRET_ACCESS_KEY}
ENV S3_ENDPOINT ${S3_ENDPOINT}


RUN rm -rf ~/.pip && \
  mkdir -p ~/.pip

RUN pip install --upgrade pip

RUN  pip --no-cache-dir install tensorflow==1.15.2 && \
     echo success
RUN pip install flask scikit-image
RUN pip install keras==2.1
RUN pip install h5py==2.10.0
RUN pip install scipy==1.1.0

COPY . /home/work
RUN chmod +x /home/work/boot.sh
ENV BUILD_PATH /home/work
WORKDIR /home/work


#ENTRYPOINT ["/bin/bash"]

CMD ["/bin/bash","+x","boot.sh"]


