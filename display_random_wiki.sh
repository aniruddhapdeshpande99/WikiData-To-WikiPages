#!/bin/bash

cd Source
python3 generate_template_wikipages.py
python generate_NLG_wikipages.py
python3 create_final_wikipage.py
cd ../Data/Films
rm temp*

echo " "
echo " "
echo "=========================================================="
echo " "
echo " Please Open index.html "
echo " "
echo "=========================================================="
echo " "
echo " "
