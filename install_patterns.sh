#!/bin/sh

mkdir -p patterns
cd patterns
curl https://www.conwaylife.com/patterns/all.zip > tmp.zip \
	&& unzip tmp.zip && rm tmp.zip
cd ..
