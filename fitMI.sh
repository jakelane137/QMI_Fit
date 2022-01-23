#/bin/bash
MI --nCores ${NCORES-12} --fitMI true --MILHCbLogFile ${LOGFILE-FitMI.log} --MIBESIIILogFile BESIII${LOGFILE-FitMI.log}.BESIII.log --DataSample ${BESIIISAMPLE-besiii0poly_0.root} --EventType "D0 K0S0 pi- pi+" --BDataSample ${LHCBSAMPLE-lhcb0poly_0.root} ${MODEL-MI.opt} 2>&1 > ${LOGFILE-Fit.log}.stdout