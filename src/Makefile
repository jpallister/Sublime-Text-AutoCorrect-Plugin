

all: create_autocorrections
	g++ -I/usr/include/python2.6 SubList.c -lboost_python -lpython2.6 -fPIC -shared -o SubList.so
	cp SubList.so ..


create_autocorrections:
	python create_auto_corrections.py
	cp autocorrections ..
