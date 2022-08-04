#strace -f -e trace=network,file,process -ttt -T -o strace.log pip install --quiet $2
#. venv/bin/activate && python3 main.py --dynamic $1 $2
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
python3 main.py --dynamic $1 $2
