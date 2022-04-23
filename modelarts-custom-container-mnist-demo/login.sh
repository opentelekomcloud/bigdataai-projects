export AK=`cat ~/.s3cfg |grep access_key|awk '{ print $NF }'`
export SK=`cat ~/.s3cfg |grep secret_key|awk '{ print $NF }'`

KEY=`printf "$AK" | openssl dgst -binary -sha256 -hmac "$SK" | od -An -vtx1 | sed 's/[ \n]//g' | sed 'N;s/\n//'`
sudo docker login -u eu-de@$AK -p $KEY  100.125.7.25:20202



