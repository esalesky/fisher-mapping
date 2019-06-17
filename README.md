# fisher-mapping

This repository contains a script to map (concatenate) Fisher speech features to match reference translations. 
When initially collected, the translations concatenated certain utterances from the speech corpus to make more meaningful segments for translation. 
For more information on this, please see [here](https://github.com/joshua-decoder/fisher-callhome-corpus).

This requires [kaldi_io](https://github.com/vesis84/kaldi-io-for-python) as a prerequisite and should support both Python 2 & 3. 

## Quick Start

1. Clone the repo:
  ```
  https://github.com/esalesky/fisher-mapping.git
  cd ./fisher-mapping
  ```
2. Install requirements:
  ```
  pip install -r requirements.txt
  git clone https://github.com/vesis84/kaldi-io-for-python.git <kaldi-io-dir>
  python setup.py install
  export PYTHONPATH=${PYTHONPATH}:<kaldi-io-dir> in $HOME/.bashrc
  ```
3. Run mapping script:
  ```
  python scripts/map_ark_utts.py -i ./fisher_cmvn_fbank40_test.ark -m maps/fisher_test
  ```
  

## Additional Information
  
As input, this script expects speech features in kaldi ark format, either binary or text. This consists of pairs of key and feature , e.g. 
  ```
  20051028_180633_356_fsp-A-000025-000121 [-4.7815437 -5.236125  -6.6157    ... -5.27584   -5.1979303 -4.0553055]  
  ```
The script requires an input ark and mapping file. 
Optionally you may specify if the input ark is binary or text (default=binary), and the desired output format (default=npz, or binary ark or text ark). 

Arguments:
  ```
  [-h --help]  help
  -i --input   path to input ark file
  -m --map     path to corresponding map file, e.g. maps/fisher_dev
  -a --arktype [bin|text] type of input ark file (binary or text). default is binary.
  -o --output  [npz|bin|text] output type (npz, binary ark, or text ark). default is npz.
  ```
