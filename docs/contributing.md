# Developer's Guide

## Installation

1. Navigate to your preferred installation location
2. Fork LandBOSSE
3. Clone your fork

    ```bash
    git clone https://github.com/<your-user-name>/LandBOSSE.git
    ```

4. Enter the directory and locally install an editable version with the testing and documentation
   building dependencies.

    ```bash
    cd LandBOSSE
    pip install -e .[test, docs]
    ```

## Testing the Code

Run LandBOSSE's testing suite using the following command. Please note the tests are not
particularly robust at this time, so passing tests after modifying the codeshould be viewed with
caution.

```bash
pytest landbosse
```

## Building the documentation

LandBOSSE uses Jupyter Book (v1) for its documentation site, which can be recreated locally with
the following command from the top-level directory.

```bash
jupyter book build docs/
```

Once complete, there will be a callout to "paste this line directly into your browser bar" with the
next line in the form of `file:///path/to/LandBOSSE/docs/_build/html/index.html`, which should be
pasted into the browser bar like a URL. You should now be able to peruse the documentation.
