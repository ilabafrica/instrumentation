#/usr/bin/env python

#Supposed mapping of sysmex KX-21 results output http://www.medelexis.ch/plugins_doc/2.1.7/Sysmex_Laborger%C3%A4teanbindung/KX-21N%20Interface.pdf

import serial
import datetime

#variables
port='/dev/ttyS0';
baudrate='9600';
bytesize=serial.EIGHTBITS; #EIGHT BITS
parity=serial.PARITY_NONE; # ODD
stopbits=serial.STOPBITS_ONE; # 2 STOP BITS
filename = '/var/www/sysmex/sysmex.dump';

#Items and their position + length
PYear	 = [4,4]
PMonth	 = [8,2]
PSampleID = [13,15]
PWBC	 = [35,4]
PFRBC	 = [40,4]
PHGB	 = [45,4]
PHCT	 = [50,4]
PMCV	 = [55,4]
PMCH	 = [60,4]
PMCHC	 = [65,4]
PPLT	 = [70,4]
PLYM	 = [75,4]
PMXD	 = [80,4]
PNEUT	 = [85,4]
PLYM1	 = [90,4]
PMXD1	 = [95,4]
PNEUT1	 = [100,4]
PRDWSD	 = [105,4]
PRDWCV	 = [110,4]
PPDW	 = [115,4]
PMPV	 = [120,4]
PPLCR	 = [125,4]


serialPort = serial.Serial(port, baudrate, bytesize, parity, stopbits); #should be open
serialPort.open();

def readloop(bytebuffer):
	while True:
		cc = serialPort.read()
		bytebuffer.extend(cc);
		if cc.encode('hex') == '\03'.encode('hex'): #end of text
			mapresults(bytebuffer)
			break;

def dumpresults(content):
	f = open(filename, 'w');
	f.write(content)
	f.close()
	bytebuffer = []
	readloop(bytebuffer)

def mapresults(results):
	Year = results[PYear[0]:PYear[0]+PYear[1]];
	Month = results[PMonth[0]:PMonth[0]+PMonth[1]];
	SampleID = results[PSampleID[0]:PSampleID[0]+PSampleID[1]];
	WBC = results[PWBC[0]:PWBC[0]+PWBC[1]];
	FRBC = results[PFRBC[0]:PFRBC[0]+PFRBC[1]];
	HGB = results[PHGB[0]:PHGB[0]+PHGB[1]];
	HCT = results[PHCT[0]:PHCT[0]+PHCT[1]];
	MCV = results[PMCV[0]:PMCV[0]+PMCV[1]];
	MCH = results[PMCH[0]:PMCH[0]+PMCH[1]];
	MCHC = results[PMCHC[0]:PMCHC[0]+PMCHC[1]];
	PLT = results[PPLT[0]:PPLT[0]+PPLT[1]];
	LYM = results[PLYM[0]:PLYM[0]+PLYM[1]];
	MXD = results[PMXD[0]:PMXD[0]+PMXD[1]];
	NEUT = results[PNEUT[0]:PNEUT[0]+PNEUT[1]];
	LYM1 = results[PLYM1[0]:PLYM1[0]+PLYM1[1]];
	MXD1 = results[PMXD1[0]:PMXD1[0]+PMXD1[1]];
	NEUT1 = results[PNEUT1[0]:PNEUT1[0]+PNEUT1[1]];
	RDWSD = results[PRDWSD[0]:PRDWSD[0]+PRDWSD[1]];
	RDWCV = results[PRDWCV[0]:PRDWCV[0]+PRDWCV[1]];
	PDW = results[PPDW[0]:PPDW[0]+PPDW[1]];
	MPV = results[PMPV[0]:PMPV[0]+PMPV[1]];
	PLCR = results[PPLCR[0]:PPLCR[0]+PPLCR[1]];

	WBC.insert(3, '.');
	FRBC.insert(2, '.');
	HGB.insert(3, '.');
	HCT.insert(3, '.');
	MCV.insert(3, '.');
	MCH.insert(3, '.');
	MCHC.insert(3, '.');
	LYM.insert(3, '.');
	MXD.insert(3, '.');
	NEUT.insert(3, '.');
	LYM1.insert(3, '.');
	MXD1.insert(3, '.');
	NEUT1.insert(3, '.');
	RDWSD.insert(3, '.');
	RDWCV.insert(3, '.');
	PDW.insert(3, '.');
	MPV.insert(3, '.');
	PLCR.insert(3, '.');
	
	LYM1 = ''.join(LYM1).lstrip('0')
	if LYM1.startswith('.'):
		LYM1 = '0'+LYM1
	
	MXD1 = ''.join(MXD1).lstrip('0')
	if MXD1.startswith('.'):
		MXD1 = '0'+ MXD1	

	NEUT1 = ''.join(NEUT1).lstrip('0')
	if NEUT1.startswith('.'):
		NEUT1 = '0'+NEUT1

	content = ''.join(
	"WBC=" + ''.join(WBC).lstrip('0')+"\n"+
	"RBC=" + ''.join(FRBC).lstrip('0')+"\n"+
	"HGB=" + ''.join(HGB).lstrip('0')+"\n"+
	"HCT=" + ''.join(HCT).lstrip('0')+"\n"+
	"MCV=" + ''.join(MCV).lstrip('0')+"\n"+
	"MCH=" + ''.join(MCH).lstrip('0')+"\n"+
	"MCHC=" + ''.join(MCHC).lstrip('0')+"\n"+
	"PLT=" + ''.join(PLT).lstrip('0')+"\n"+
	"LYM%=" + ''.join(LYM).lstrip('0')+"\n"+
	"MXD%=" + ''.join(MXD).lstrip('0')+"\n"+
	"NEUT%=" + ''.join(NEUT).lstrip('0')+"\n"+
	"LYM#=" + LYM1 +"\n"+
	"MXD#=" + MXD1 +"\n"+
	"NEUT#=" + NEUT1 +"\n"+
	"RDW_SD=" + ''.join(RDWSD).lstrip('0')+"\n"+
	"RDW_CV=" + ''.join(RDWCV).lstrip('0')+"\n"
	)
	print content;
	dumpresults(content)

bytebuffer = []
readloop(bytebuffer)

