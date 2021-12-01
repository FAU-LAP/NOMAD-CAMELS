cd /home/epics/IOCs
mkdir $1
cd $1
makeBaseApp.pl -t ioc $1
echo | makeBaseApp.pl -i -t ioc $1
mkdir $1Sup
cd iocBoot/ioc$1
chmod u+x st.cmd

