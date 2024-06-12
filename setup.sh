git clone https://github.com/fgcz/bfabricPy.git && cd bfabricPy
git checkout bfabric12 
cd bfabricPy
python3 setup.py sdist && pip3 install dist/bfabric-0.13.*.tar.gz
cd ..
