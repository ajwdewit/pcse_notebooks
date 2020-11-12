.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/ajwdewit/pcse_notebooks/HEAD

A collection of PCSE notebooks
==============================

This repository provides a set of notebooks that demonstrates various aspects of PCSE models. 

The notebooks include introductory examples:

- **01 Getting Started with PCSE.ipynb** provides an impression of how PCSE works and what you can do with it
- **02 Running with custom input data.ipynb** shows how you can run a model using your own input data instead of the demonstration data.
- **03 running_LINTUL3.ipynb** a similar example, but instead using the LINTUL3 model instead of WOFOST.
- **04 Running PCSE in batch mode.ipynb** demonstrates how to run PCSE simulation in batch for a series of crops and year
  
Some more advanced features of PCSE are demonstrated in:
 
- **05 Using PCSE WOFOST with a CGMS8 database.ipynb** this shows how to retrieve data from a CGMS database and run crop model simulations with WOFOST using that data.
- **06_advanced_agromanagement_with_PCSE.ipynb** demonstrates advanced aspects of the agromanagement definitions including scheduling events based on date and state variables.
- **07 Running crop rotations.ipynb** provides insight on how to run crop rotations with PCSE models.
 
Finally, highly advanced subjects are treated that require quite some background knowledge and python programming skills:

- **08_data_assimilation_with_the_EnKF.ipynb** provides an introduction to data assimilation with the ensemble Kalman filter.
- **09 Optimizing parameters in a PCSE model.ipynb** demonstrates how to do parameter optimizations in PCSE.

Dependencies
------------

Using these notebooks generally require a python environment that includes the following packages:

- PCSE and its dependencies
- pandas, matplotlib and for notebook 09 the NLOPT optimization library.
