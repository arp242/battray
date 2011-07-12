# 
# Juts a simple Makefile for installing / deinstalling. Guess I could also
# using Python setuptools but I can't be bothered to figure out how that
# works.
# 
# Please note how we are using ?= and not =, so you can easily override these
# variables. For examle with ``make PREFIX=/whatever''
#

PROGNAME?=	battray
PREFIX?=	/usr/local

BINDIR?=	${PREFIX}/bin
DATADIR?=	${PREFIX}/share/${PROGNAME}
MANDIR?=	${PREFIX}/man/man1

PYTHON?=	python
INSTALL_DATA?=	install
INSTALL_PROG?=	install
MKDIR?=		mkdir -p
RM?=		rm
RMDIR?=		rmdir
TRUE?=		true
LN?=		ln
SED?=		sed

all: build
build:
	@${TRUE}

install:
	${MKDIR} ${BINDIR} ${MANDIR} ${DATADIR}
	${INSTALL_PROG} battray.py ${BINDIR}/${PROGNAME}
	${INSTALL_DATA} battray.1 ${MANDIR}/${PROGNAME}.1
	
	${MKDIR} ${DATADIR}/icons ${DATADIR}/platforms
	${INSTALL_DATA} \
		icons/battery.png \
		icons/charging.png \
		icons/connected.png \
		icons/error.png \
		icons/green.png \
		icons/red.png \
		icons/yellow.png \
			${DATADIR}/icons/
	${INSTALL_DATA} \
		platforms/freebsd.py \
		platforms/openbsd.py \
		platforms/linux.py \
			${DATADIR}/platforms
	${INSTALL_DATA} \
		heartmonitor.wav \
		battrayrc.py \
			${DATADIR}/
	${SED} 's|%%DATADIR%%|${DATADIR}:' ${DATADIR}/battrayrc.py
	
deinstall:
	${RM} ${BINDIR}/${PROGNAME} ${MANDIR}/${PROGNAME}.1
	${RM} ${DATADIR}/icons/battery.png \
		${DATADIR}/icons/charging.png \
		${DATADIR}/icons/connected.png \
		${DATADIR}/icons/error.png \
		${DATADIR}/icons/green.png \
		${DATADIR}/icons/red.png \
		${DATADIR}/icons/yellow.png \
		${DATADIR}/heartmonitor.wav

	${RM} \
		${DATADIR}/platforms/freebsd.py \
		${DATADIR}/platforms/openbsd.py \
		${DATADIR}/platforms/linux.py

	${RM} -f \
		${DATADIR}/platforms/freebsd.pyc \
		${DATADIR}/platforms/openbsd.pyc \
		${DATADIR}/platforms/linux.pyc

	${RMDIR} ${DATADIR}/icons ${DATADIR}/platforms ${DATADIR}
