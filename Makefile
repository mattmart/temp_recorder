init:
	pip3 install -r requirements.txt

test:
	nosetests tests

install:
	cp temp_recorder.service /etc/systemd/system/temp_recorder.service
	mkdir -p /var/lib/temp_recorder
	cp temp_recorder/temp_recorder.py /var/lib/temp_recorder/temp_recorder.py
	chmod +x /var/lib/temp_recorder/temp_recorder.py
	systemctl daemon-reload
faketest:
	mkdir -p /tmp/sys/bus/w1/devices
	mkdir -p /tmp/sys/devices/w1_bus_master1/
	mkdir -p /tmp/sys/devices/w1_bus_master1/28-0000054823e9
	ln -s ../../../devices/w1_bus_master1  /tmp/sys/bus/w1/devices/w1_bus_master1
	ln -s ../../../devices/w1_bus_master1/28-0000054823e9 /tmp/sys/bus/w1/devices/28-0000054823e9
	echo "4e 01 4b 46 7f ff 02 10 d9 : crc=d9 YES\n4e 01 4b 46 7f ff 02 10 d9 t=20875\n" >  /tmp/sys/devices/w1_bus_master1/28-0000054823e9/w1_slave

