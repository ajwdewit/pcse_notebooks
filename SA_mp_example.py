"""Example code demonstrating how how to use the multiprocessing package to run WOFOST in parallel in order to speed up sensitivity analysis.

This code basically replicated notebook 10 but much of the code in individual cells has been
turned into functions because we can decorate those with the LRU cache which speeds up even 
further.

Allard de Wit (allard.dewit@wur.nl), September 2023
"""

import sys, os.path
from functools import partial, lru_cache
from collections import namedtuple
import multiprocessing as mp

import yaml
import numpy as np
from tqdm import tqdm
from SALib.sample import saltelli
from SALib.analyze import sobol

import pcse
from pcse.models import Wofost72_PP
from pcse.base import ParameterProvider
from pcse.db import NASAPowerWeatherDataProvider
from pcse.fileinput import YAMLCropDataProvider
from pcse.util import WOFOST72SiteDataProvider, DummySoilDataProvider


# Define a named tuple to hold all details of this run
RunDetails = namedtuple("RunDetails", ['latitude', 'longitude', 'crop_name', 'variety_name', 'campaign_start_date', 
                                       'emergence_date', 'harvest_date', 'max_duration'])


@lru_cache
def define_agromanagement(run_details):
    # Here we define the agromanagement for sugar beet

    agro_yaml = """
    - {campaign_start_date}:
        CropCalendar:
            crop_name: {crop_name}
            variety_name: {variety_name}
            crop_start_date: {emergence_date}
            crop_start_type: emergence
            crop_end_date: {harvest_date}
            crop_end_type: harvest
            max_duration: {max_duration}
        TimedEvents: null
        StateEvents: null
    """.format(**run_details._asdict())
    agro = yaml.safe_load(agro_yaml)
    return agro, agro_yaml


@lru_cache
def get_weatherdata(run_details):
    # Weather data for Netherlands from NASA Power
    wdp = NASAPowerWeatherDataProvider(latitude=run_details.latitude, longitude=run_details.longitude)
    return wdp


@lru_cache
def get_modelparameters(run_details):
    # Parameter sets for crop, soil and site
    # Standard crop parameter library
    cropd = YAMLCropDataProvider(force_reload=True)
    # We don't need soil for potential production, so we use dummy values
    soild = DummySoilDataProvider()
    # Some site parameters
    sited = WOFOST72SiteDataProvider(WAV=50)

    # Retrieve all parameters in the form of a single object. 
    # In order to see all parameters for the selected crop already, we
    # synchronise data provider cropd with the crop/variety: 
    cropd.set_active_crop(run_details.crop_name, run_details.variety_name)

    params = ParameterProvider(cropdata=cropd, sitedata=sited, soildata=soild)

    return params


def run_wofost_simulation(paramset, run_details, problem, target_variable):
    agro, agro_yaml = define_agromanagement(run_details)
    wdp = get_weatherdata(run_details)
    params = get_modelparameters(run_details)

    params.clear_override()
    for name, value in zip(problem["names"], paramset):
        params.set_override(name, value)
    wofost = Wofost72_PP(params, wdp, agro)
    wofost.run_till_terminate()
    r = wofost.get_summary_output()
    target_result = r[0][target_variable]
    if target_result is None:
        print("Target variable is not available in summary output!")
    return target_result
    


def main():
    # Define location, crop and season
    d = dict(
        latitude = 52.0,
        longitude = 5.0,
        crop_name = 'sugarbeet',
        variety_name = 'Sugarbeet_601',
        campaign_start_date = '2006-01-01',
        emergence_date = "2006-03-31",
        harvest_date = "2006-10-20",
        max_duration = 300
    )
    run_details = RunDetails(**d)

    # Define the target variable
    target_variable = "TWSO"

    # For each scalar parameter, determine a sensible interval 
    problem_yaml = """
        num_vars: 5
        names: 
        - TSUM1
        - TSUM2
        - SPAN
        - Q10
        - TDWI
        bounds:
        - [500, 800]
        - [1200, 1600]
        - [28, 37]
        - [1.8, 2.2]
        - [0.4, 0.6]
    """
    problem = yaml.safe_load(problem_yaml)

    calc_second_order = True
    nsamples = 50
    paramsets = saltelli.sample(problem, nsamples, calc_second_order=calc_second_order)

    # create a partial functions that pre-defines the target_variable, problem and run_details in run_wofost_simulation()
    # because they are static for each function call in the loop. Only the paramset changes.
    run_wofost_partial = partial(run_wofost_simulation, target_variable=target_variable, run_details=run_details,
                                 problem=problem)

    # Loop over the samples of the parameter values and run WOFOST for each of the samples
    print("starting processing on single CPU")
    target_results = []
    with tqdm(total=len(paramsets)) as pbar:
        for paramset in paramsets:
            target_result = run_wofost_partial(paramset)
            target_results.append(target_result)
            pbar.update()

    target_results_sp = np.array(target_results)


    # Loop over the samples of the parameter values and run WOFOST for each of the samples
    print("starting processing on multiple CPUs")
    target_results = []
    with tqdm(total=len(paramsets)) as pbar:
        with mp.Pool(mp.cpu_count()) as pool:
            for result in pool.imap(run_wofost_partial, paramsets):
                target_results.append(result)
                pbar.update()

    target_results_mp = np.array(target_results)
    
    r = np.all(target_results_mp == target_results_sp)
    print(f"Results from single vs multiple processing are the same is {r}")


if __name__ == "__main__":
    main()