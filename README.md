# Assignment - Building Robust Software Summative Assignment

This project will try to address the following requirements while working on a COVID-19 dataset from Kaggle and after the analysis, 
generate a COVID-19 plot for `Confirmed Cases` vs `Deaths` and save the plot with the filename  `covid_cases_Canada.png`

## Requirements

- The deliverable, your package:

  The package is called `nightlock` accessible at the URL : https://github.com/amikkuma/nightlock

- Must be hosted on a GitHub repository.

  The package is hosted as github repository : https://github.com/amikkuma/nightlock
  
- Must be installable using pip: pip install git+https://github.com/user/yourteamrepo

  The package is installable using the following command
  ```
  pip install git+https://github.com/amikkuma/nightlock
  ```
  
- Must include a module named `Analysis`

  The package includes a module called `Analysis` and can be accesed by the following import command
  ```
  from nightlock.Analysis import Analysis
  ```
  
- Must include a README.md, LICENSE, and CONDUCT.md file

  The package includes the following files with appropriate content
  1. README.md - This file
  2. LICENCE - Includes MIT license
  3. CONDUCT.md - Inlcudes a `CONDUCT.md`
     
- Must include unit tests, as appropriate

  1. The package includes a `tests` directory and includes a file `test_Analysis.py` which has all the `unittest` with `assertions`.
  2. A python package `pytest-mock` is required to be installed for the tests to work. This is included as dependency in the `setup.py`
    
- Must include a TESTS.md file detailing in point-form the non-automated tests to be performed, as appropriate

 `kaggle` API is used to connect to `Kaggle` and download the dataset live during the tests. So `.kaggle/kaggle.json` needs to be present for this to run.
  Please follow the `Authentication` section from https://www.kaggle.com/docs/api regarding the crednetials requirement.

- Must use the logging library to output debug, info, and error messages as appropriate

The `logging` library is used to create a log file called `analysis.log` where all the `INFO` and `ERROR` messages are logged

- Must be documented using Python docstrings in the numpy style

The `class` and each of the `functions` contained in the module `analysis.py` are well documented in `numpy` style.

- Must use try/except to handle errors, must raise useful error messages, and must include at least one assertion
  Hint: We can't analyze data that has not yet been loaded! And consider incorrect configuration parameters!

  There are `try` and `except` blocks included along with `assertions` wherever required and appropriate.
  
- During development, your team must:

Because of time constraints in schedule, Development has not been done in a team. However `issues` were created to keep track of things and updated as if worked in a team.
Hope that is not a problem and acceptable.

Track features using GitHub issues
Each constituent function of the Analysis module should be one or more issues
Each issue should be assigned to a member of your team
Your team should distribute workload evenly
Make changes to the repository by forking the main repository, updating your fork, and merging your changes using pull requests
