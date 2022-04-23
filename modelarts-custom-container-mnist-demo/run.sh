# /bin/bash
# when using from ModelArts container then have to use following command: 
# env && bash /home/work/run_train.sh python /home/work/user-job-dir/mnist/kerastrain.py --data_url /home/work/user-job-dir/mnist/mnist_data  --train_dir /home/work/user-job-dir/mnist/mnist_data_out
docker run --env AWS_ACCESS_KEY_ID --env AWS_SECRET_ACCESS_KEY --env S3_ENDPOINT -it modelarts/mnist /bin/bash
