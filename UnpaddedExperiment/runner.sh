git submodule update --init --recursive

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# no pad experiment

cd ../aioquic
git apply ../UnpaddedExperiment/nopad.patch
pip install .
cd ..
python unpaddedConnection.py
git apply -R ../UnpaddedExperiment/nopad.patch

