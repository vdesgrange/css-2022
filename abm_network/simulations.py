import mesa
from .model import VirusOnNetwork
from .parameters import analysis_params_a

def experiment_a():
    results = mesa.batch_run(
        VirusOnNetwork,
        parameters=analysis_params_a,
        iterations=100,
        max_steps=200,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )

    return results

def simulations():
    experiment_a()
