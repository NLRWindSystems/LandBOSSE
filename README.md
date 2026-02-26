# LandBOSSE

[![PyPI version](https://badge.fury.io/py/NREL-landbosse.svg)](https://badge.fury.io/py/NREL-landbosse)
[![Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![image](https://img.shields.io/pypi/pyversions/NREL-landbosse.svg)](https://pypi.python.org/pypi/NREL-landbosse)
[![Jupyter Book](https://jupyterbook.org/badge.svg)](https://nlrwindsystems.github.io/NREL-landbosse)

## Welcome to LandBOSSE!

The Land-based Balance-of-System Systems Engineering (LandBOSSE) model is a systems engineering tool that estimates the balance-of-system (BOS) costs associated with installing utility scale wind plants (10, 1.5 MW turbines or larger). It can execute on macOS and Windows. At this time, for both platforms, it is a command line tool that needs to be accessed from the command line.

The methods used to develop this model (specifically, LandBOSSE Version 2.1.0) are described in greater detail the following report:

Eberle, Annika, Owen Roberts, Alicia Key, Parangat Bhaskar, and Katherine Dykes.
2019. NREL’s Balance-of-System Cost Model for Land-Based Wind. Golden, CO:
National Renewable Energy Laboratory. NREL/TP-6A20-72201.
https://www.nrel.gov/docs/fy19osti/72201.pdf.

## Installation

For any installation, users should use a virtual environment. We recommend Miniconda or Anaconda,
but any supporting PyPI or source installations are possible. Here, we'll work with conda for
compatibility with other NREL tools.

In the below, you can replace the name "landbosse" with any name you choose, and the Python version
can be any that you prefer as long as it's supported by LandBOSSE.

```bash
conda create -n landbosse python=3.13 -y
```

### PyPI

```bash
pip install NREL-landbosse
```

### Source

1. Navigate to your preferred installation location
2. Clone the repo (or fork and clone your fork, if preferred).

    ```bash
    git clone https://github.com/NLRWindSystems/LandBOSSE.git
    ```

3. Enter the directory and install the local version

    ```bash
    cd LandBOSSE
    pip install .
    ```

    Optional: `pip install -e .` for editable installations if you plan to modify the code itself.

## User Guides

### First time running teh model

At its most basic, the following setup is required, though the provided input data in `project_inpute_template`
can be used to test out the model and view results before diving into configuring custom scenarios.

1. Create an "input" and "output" folder for LandBOSSE to access. If you are using a source
   installation, then ensure the folders are not located inside the local copy of the repository.
2. Create a `project_list.xlsx` like `LandBOSSE/project_list.xlsx` and a subfolder called
   `project_data` inside of `inputs`.
3. Each project in `project_list.xlsx` should have a corresponding Excel file in `project_data`
   similar to the examples in `LandBOSSE/project_input_template/project_data`.


### Running the model 

Once the initial steps (above) are followed, we can run the model:

1. Activate your virtual environment: `conda activate landbosse
2. Navigate to the top-level `LandBOSSE` folder
3. Run the model: `python main.py -i input-folder-path -o output-folder-path` (be sure to replace
   "input-folder-path" and "output-folder-path" with your respective input and output folders).

All together

```bash
conda activate landbosse
cd /path/to/LandBOSSE
python main.py -i /path/to/inputs -o /path/to/outputs
conda deactivate
```

4. View your results in the output folder.


### Integrating LandBOSSE into your code

While LandBOSSE was originally designed as a CLI tool powered by Excel workbooks, an API also exists
to run the model within another application.

Further documentation coming soon
