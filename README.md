<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

# Introduction
Baler is a tool used to test the feasibility of compressing different types of scientific data using machine learning-based autoencoders.


# Setup <a name="setup"></a>
## If you are using Windows 10/11
* If you are using a Mac on Linux system, skip to the [next section](#linux)
* The best way to run baler on Windows is to do so using the "Windows Subsystem for Linux"
* Install "git for windows": https://github.com/git-for-windows/git/releases/tag/v2.39.1.windows.1
  * For a 64 bit system, probably use this one: https://github.com/git-for-windows/git/releases/download/v2.39.1.windows.1/Git-2.39.1-64-bit.exe
* Go to your windows search bar and search for "powershell". Right-click powerhsell and select "run as administrator"
* Enable Linux subsystem by entering this into the PowerShell and hitting enter: `Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux`
* Go to the windows store and download "Ubuntu 22.04.1 LTS"
* Once downloaded, open it. This will start Ubuntu as a "terminal". After picking a username and password, input the following commands into that terminal. You can copy the commands using ctrl+c or the button to the right of the text. But pasting it into the terminal can only be done by right-clicking anywhere in the terminal window.

Start by updating the Windows Subsystem for Linux
```console
wsl.exe --update
```
Then, synch your clock:
```console
sudo hwclock --hctosys
```
Update your Linux packages
```console
sudo apt-get update
```
Configure git to use tour windows credentials helper, this is necessary for you to authenticate yourself on GitHub.
```console
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager-core.exe"
```
Install pip3 for downloading python packages
```console
sudo apt-get install python3-pip
```
At this point, you have a working Linux environment and you can follow the next section for the Linux setup

## Setup (Linux/Mac or Windows Subsystem for Linux) <a name="linux"></a>
For some Linux users (Ubuntu), disable the KDE keyring
```console
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
```
Install poetry for managing the python environment
```console
pip3 install poetry
```
Add poetry to path in your current session (Maybe not necessary for Mac)
```console
source ~/.profile
```
Clone **your fork** of this  repository
```console
git clone https://github.com/USERNAME/application-baler
```
Move into the Baler directory
```console
cd application-baler
```
Use Poetry to install the project dependencies
```console
poetry install
```
Download the tutorial dataset, this will take a while
```console
wget http://opendata.cern.ch/record/21856/files/assets/cms/mc/RunIIFall15MiniAODv2/ZprimeToTT_M-3000_W-30_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/10000/DAA238E5-29D6-E511-AE59-001E67DBE3EF.root -O data/example/example.root
```
Finally, verify that the download was successful
```console 
md5sum data/example/example.root 
> 28910642bf94e0fa9442bc804830f88b  data/example/example.root
```

# Tutorial Example  <a name="tutorial"></a>
## Create New Project 
Start by creating a new project directory. This will create the standardized directory structure needed, and create a skeleton config, pre-processing script, analysis script, and output directories. In this example, these will live under `./projects/example/`.
```console
poetry run python baler --project=example --mode=new_project
```

## Pre-processing
Baler Currently only supports Pandas dataframes, saved as pickles, as input. Therefore, most data needs to go through some kind of pre-processing before Baler can work on that data.

To run the pre-processing for this specific example dataset, run:
```console
poetry run python baler --project=example --mode=preprocessing
```
The pre-processing was done using the script found at `./projects/example/example_preprocessing.py`

## Training
To train the autoencoder to compress your data, you run the following command. The config file defines the path of the input data, the number of epochs, and all the other parameters.
```console
poetry run python baler --project=example --mode=train
```

## Compressing
To use the derived model for compression, you can now choose ``--mode=compress``, which can be run as
```console
poetry run python baler --project=example --mode=compress
```
This will output a compressed file called "compressed.pickle", and this is the latent space representation of the input dataset. It will also output cleandata_pre_comp.pickle which is just a copy of the original data.

## Decompressing
To decompress the compressed file, we choose ``--mode=decompress`` and run:
```console
poetry run python baler --project=example --mode=decompress
```
This will output ``./projects/example/decompressed_output/decompressed.pickle``. To double-check the file sizes, we can run
```console
poetry run python baler --project=example --mode=info
```
which will print the file sizes of the data we’re compressing, the compressed dataset & the decompressed dataset.

## Evaluating Performance
To evaluate the performance of our compression, we compare our data before the compression to the data after compression+decompression. We do this by plotting the variable distribution before and after, as well as the response distribution R=(before-after)/before.

To run the standard evaluation, we use the following command to generate a .pdf document under ``./projects/example/plotting/evaluation.pdf``

```console
poetry run python baler --project=example --mode=evaluate
```

## Custom analysis
A lot of scientists interested in using Baler wants to see how compression affects their measurements. Therefore, Baler supports users running their own custom analysis as part of Baler to compare their measurements before and after compression.

Custom analyses are defined under ``./projects/example/example_analysis.py``. In our example, the analysis fits the particle mass distribution, and compares the mass derived from the fit before and after compression. You can run the custom analysis using

```console
poetry run python baler --project=example --mode=analysis
```

The results of the analysis comparison is shown in ``./projects/example/plotting/analysis.pdf``
