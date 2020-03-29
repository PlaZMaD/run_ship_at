FROM olantwin/ship-base:191114
RUN git clone   https://github.com/ShipSoft/FairShip.git && cd FairShip && git checkout 662e3f851389b613f4dd23097ff6e29b11925e18 && cd /
RUN aliBuild -c shipdist/ --defaults fairship build FairShip --no-local ROOT
COPY run_jobs.sh /scripts/run_jobs.sh
COPY azcopy /bin/azcopy
RUN chmod +x /bin/azcopy
ENTRYPOINT mkdir -p /tmp/$jName/$fileName/$jNumber && /scripts/run_jobs.sh | tee /tmp/$jName/$fileName/$jNumber/logs
#RUN mkdir /sw/slc7_x86-64/FairRoot/latest/include/source && cp /sw/slc7_x86-64/FairRoot/latest/include/*.h /sw/slc7_x86-64/FairRoot/latest/include/source && mkdir /sw/slc7_x86-64/FairRoot/latest/include/steer && cp /sw/slc7_x86-64/FairRoot/latest/include/*.h /sw/slc7_x86-64/FairRoot/latest/include/steer && mkdir /sw/slc7_x86-64/FairRoot/latest/include/sim && cp /sw/slc7_x86-64/FairRoot/latest/include/*.h /sw/slc7_x86-64/FairRoot/latest/include/sim && mkdir /sw/slc7_x86-64/FairRoot/latest/include/field && cp /sw/slc7_x86-64/FairRoot/latest/include/*.h /sw/slc7_x86-64/FairRoot/latest/include/field && mkdir /sw/slc7_x86-64/FairRoot/latest/include/event && cp /sw/slc7_x86-64/FairRoot/latest/include/*.h /sw/slc7_x86-64/FairRoot/latest/include/event

