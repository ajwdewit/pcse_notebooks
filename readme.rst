.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/ajwdewit/pcse_notebooks/HEAD

A collection of PCSE notebooks
==============================

This repository provides a set of notebooks that demonstrates various aspects of PCSE models. 

The notebooks include introductory examples:

- **01 Getting Started with PCSE** provides an impression of how PCSE works and what you can do with it
- **02 Running with custom input data** shows how you can run a model using your own input data instead of the demonstration data.
- **03 Running LINTUL3** a similar example, but instead using the LINTUL3 model instead of WOFOST.
- **04 Running PCSE in batch mode** demonstrates how to run PCSE simulation in batch for a series of crops and year
- **13 Simulating grassland productivity with LINGRA** demonstrates the LINGRA model for simulating productivity of grasslands

Some more advanced features of PCSE are demonstrated in:
 
- **05 Using PCSE WOFOST with a CGMS8 database** this shows how to retrieve data from a CGMS database and run crop model simulations with WOFOST using that data.
- **06 Advanced agromanagement with PCSE** demonstrates advanced aspects of the agromanagement definitions including scheduling events based on date and state variables.
- **07 Running crop rotations** provides insight on how to run crop rotations with PCSE models.
 
Finally, highly advanced subjects are treated that require quite some background knowledge and python programming skills:

- **08a Data assimilation with the EnKF** provides an introduction to data assimilation with the ensemble Kalman filter.
- **08b Data assimilation with the EnKF multistate** demonstrates how to effectively load multiple states into the EnKF state vector.
- **09 Optimizing parameters in a PCSE model** demonstrates how to do parameter optimizations in PCSE.
- **10 Sensitivity analysis of WOFOST** demonstrates how to use SAlib for sensitivity analysis

Dependencies
------------

Using these notebooks generally require a python environment that includes the following packages:

- PCSE and its dependencies
- matplotlib
- The NLOPT optimization library (notebooks 09, 11)
- The SAlib library (notebook 10)
