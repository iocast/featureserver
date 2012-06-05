#!/bin/sh

VERSION=$1

DIR="featureserver-$VERSION"

rm -rf $DIR 
rm -rf $DIR.tar.gz 
mkdir $DIR
mkdir $DIR/doc
cp doc/*  $DIR/doc
cp *.py  $DIR
cp *.cgi  $DIR
cp *.fcgi  $DIR
cp featureserver.cfg $DIR

mkdir $DIR/template
cp template/*  $DIR/template

cp -r FeatureServer $DIR

cp index.html $DIR/index.html
cp json.html $DIR/json.html
cp json.js $DIR/json.js
cp kml.html $DIR/kml.html
cp LICENSE.txt $DIR/LICENSE.txt
cp CHANGELOG.txt $DIR/CHANGELOG.txt

find $DIR -name .svn | xargs rm -rf
find $DIR -name *.pyc | xargs rm -rf

tar -cvzf $DIR.tar.gz $DIR
zip -r $DIR.zip $DIR


wget -c http://cheeseshop.python.org/packages/source/P/Paste/Paste-1.3.tar.gz
tar -zvxf Paste-1.3.tar.gz
cp -r Paste-1.3/paste $DIR

wget -c http://cheeseshop.python.org/packages/source/s/simplejson/simplejson-1.7.1.tar.gz 
tar -zvxf simplejson-1.7.1.tar.gz
cp -r simplejson-1.7.1/simplejson $DIR
rm -rf $DIR/simplejson/tests

wget -c http://cheeseshop.python.org/packages/source/w/wsgiref/wsgiref-0.1.2.zip 
unzip wsgiref-0.1.2.zip
cp -r wsgiref-0.1.2/wsgiref $DIR

mkdir $DIR/licenses
cp simplejson-1.7.1/LICENSE.txt $DIR/licenses/mit-license.txt
cp featureserver/LICENSE.txt $DIR/licenses/featureserver-license.txt
cp license-list.txt $DIR/LICENSE.txt

tar -cvzf $DIR-full.tar.gz $DIR
zip -r $DIR-full.zip $DIR
