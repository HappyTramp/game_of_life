#!/bin/sh

mkdir patterns
curl www.conwaylife.com/patterns/all.zip > patterns/tmp.zip
cd patterns
unzip tmp.zip
rm tmp.zip

