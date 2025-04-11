sudo apt install python3-netfilterqueue
git submodule update --init --recursive

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# no pad experiment

cd aioquic
git apply ../patches/nopad.patch
pip install .
cd ..
python doq.py
git apply -R ../patches/nopad.patch

# no reply experiment

cd aioquic
git apply ../patches/retry.patch
pip install .
cd ..
python doq.py & 
python packetmeasure.py
git apply -R ../patches/retry.patch
