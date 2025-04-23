git submodule update --init --recursive

python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt

# no pad experiment

cd aioquic
git apply ../UnpaddedExperiment/nopad.patch
python -m pip install .
cd ../UnpaddedExperiment
python unpadded_connection.py

