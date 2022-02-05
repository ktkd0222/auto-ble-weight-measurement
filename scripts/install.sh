#!/bin/bash

echo 'weight measurement install start.'

BASE_DIR=$PWD
INSTALL_DIR=/opt/weight_measurement

# create directory.
mkdir -p ${INSTALL_DIR}

# copy python scripts and executable.
cp ${BASE_DIR}/../*.py ${INSTALL_DIR}
chmod +x ${INSTALL_DIR}/*.py

# service file copy and activate.
cp ${BASE_DIR}/weight.service /etc/systemd/system/weight.service
systemctl daemon-reload
systemctl enable weight

echo 'install success!!'
echo '[usage]'
echo ' - start application  -> $ sudo systemctl start weight'
echo ' - stop application   -> $ sudo systemctl stop weight'
echo ' - application status -> $ sudo systemctl status weight'
echo ' - reference log data -> $ sudo journalctl -u weight'
