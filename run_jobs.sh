#!/bin/bash
#mkdir -p /output/$jName/$fileName/$jNumber
CN=$((fileName*1000))
FN="pythia8_Geant4_10.0_withCharmandBeauty${CN}_mu.root"
#source $(alienv printenv FairShip/latest)
alienv -w /sw setenv  FairShip/latest  -c /bin/bash  -c "python \$FAIRSHIP/macro/run_simScript.py   --MuonBack --sameSeed 1 --seed 1 -f /sample/$FN  --nEvents $nEvents  --firstEvent $mfirstEvent --output /tmp/$jName/$fileName/$jNumber  --muShieldDesign $muShieldDesign"
alienv -w /sw setenv  FairShip/latest  -c /bin/bash -c "python \$FAIRSHIP/macro/ShipReco.py -g /tmp/$jName/$fileName/$jNumber/geofile_full.conical.MuonBack-TGeant4.root -f /tmp/$jName/$fileName/$jNumber/ship.conical.MuonBack-TGeant4.root"
mv ship.conical.MuonBack-TGeant4_rec.root /tmp/$jName/$fileName/$jNumber/
cp /tmp/$jName/$fileName/$jNumber/*  /output #/$jName/$fileName/$jNumber/
