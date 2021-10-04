#!/bin/bash

cp models/basic.py tutorial/basic.py
mkdir tutorial/props
cp models/props/segregation.props.json tutorial/props/segregation.props.json

# start changing names
# replace basic with segregation
sed -i s/basic/segregation/g tutorial/basic.py
sed -i s/Basic/Segregation/g tutorial/basic.py