#!/bin/bash
zero=0
sat=3DIMG_
date=01
month=JUL2014_
hour=00
min=00
level=_L1C_ASIA_MER
ext=.h5

# ftp folder path
url1=ftp://ftp.mosdac.gov.in/Order/Feb18_038896/

	# for 31 days of a month
while [ $date -lt 32 ]; do
	str=$sat$date$month$hour$min$level$ext
	url=$url1$str
	# downloading the file		
	wget --user ranendu --password ashoka@1957 $url		

	#if [ `expr $min` == 00 ];then
	#	min=30
	#else 
	#	min=00

	# increasing the hour
	hour=$((10#$hour+1))
	if [ `expr $hour` -lt 10 ];then
		hour=$zero$hour		
	fi	
	#fi
	echo $hour
	# changing the day after 24 hour	
	if [ `expr $hour` != 00 ] && [ `expr $hour` == 24 ];then
		date=$((10#$date+1))
		if [ `expr $date` -lt 10 ];then
			date=$zero$date		
		fi
		#min=00
		hour=00
	fi 
done

#EOF

