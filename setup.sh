sudo apt install python3-netfilterqueue
git submodule update --init --recursive

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# no pad experiment

cd aioquic
git apply ../nopad.patch
pip install .
cd ..
python doq.py
