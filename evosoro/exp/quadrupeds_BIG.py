import random
import os
import sys
import numpy as np
import subprocess as sub

from evosoro.base import Sim, Env, ObjectiveDict
from evosoro.networks import CPPN, DirectEncoding
from evosoro.softbot import Genotype, Phenotype, Population
from evosoro.tools.algorithms import ParetoOptimization
from evosoro.tools.checkpointing import continue_from_checkpoint
from evosoro.tools.utils import one_muscle, quadruped


sub.call("cp ../_voxcad/voxelyzeMain/voxelyze .", shell=True)
sub.call("chmod 755 voxelyze", shell=True)

SEED = int(sys.argv[1])
MAX_TIME = float(sys.argv[2])

IND_SIZE = (6, 6, 5)
MIN_PERCENT_FULL = 0.2
STIFFNESS = 1e7
GROWTH_AMPLITUDE = 1

POP_SIZE = 50
MAX_GENS = 5000
NUM_RANDOM_INDS = 1

INIT_TIME = 0.40
SIM_TIME = 4 + INIT_TIME  # 2 + INIT_TIME  # includes init time
TEMP_AMP = 39.4714242553  # 50% volumetric change with temp_base=25: (1+0.01*(39.4714242553-25))**3-1=0.5
FREQ = 5.0

DT_FRAC = 0.9  # 0.3

TIME_TO_TRY_AGAIN = 25
MAX_EVAL_TIME = 61

SAVE_VXA_EVERY = MAX_GENS + 1
SAVE_LINEAGES = False
CHECKPOINT_EVERY = 1
EXTRA_GENS = 0

RUN_DIR = "run_{}".format(SEED)
RUN_NAME = "Quadrupeds"


class MyGenotype(Genotype):
    def __init__(self):
        Genotype.__init__(self, orig_size_xyz=IND_SIZE)

        self.add_network(CPPN(output_node_names=["phase_offset"]))
        self.to_phenotype_mapping.add_map(name="phase_offset", tag="<PhaseOffset>", logging_stats=None)

        self.add_network(DirectEncoding(output_node_name="material_present", orig_size_xyz=IND_SIZE), freeze=True)
        self.to_phenotype_mapping.add_map(name="material_present", tag="<Data>", output_type=int, logging_stats=None)

        self.add_network(DirectEncoding(output_node_name="init_size", orig_size_xyz=IND_SIZE), freeze=True)
        self.to_phenotype_mapping.add_map(name="init_size", tag="<InitialVoxelSize>", logging_stats=None)


my_quad = quadruped(IND_SIZE)
size = np.ones_like(my_quad, dtype=float)
MyGenotype.NET_DICT = {'material_present': my_quad, 'init_size': size}


if not os.path.isfile("./" + RUN_DIR + "/pickledPops/Gen_0.pickle"):

    random.seed(SEED)
    np.random.seed(SEED)

    my_sim = Sim(dt_frac=DT_FRAC, simulation_time=SIM_TIME, fitness_eval_init_time=INIT_TIME)

    my_env = Env(temp_amp=TEMP_AMP, frequency=FREQ, muscle_stiffness=STIFFNESS, growth_amp=GROWTH_AMPLITUDE)

    my_objective_dict = ObjectiveDict()
    my_objective_dict.add_objective(name="fitness", maximize=True, tag="<normAbsoluteDisplacement>")
    my_objective_dict.add_objective(name="age", maximize=False, tag=None)

    my_pop = Population(my_objective_dict, MyGenotype, Phenotype, pop_size=POP_SIZE)

    my_optimization = ParetoOptimization(my_sim, my_env, my_pop)
    my_optimization.run(max_hours_runtime=MAX_TIME, max_gens=MAX_GENS, num_random_individuals=NUM_RANDOM_INDS,
                        directory=RUN_DIR, name=RUN_NAME, max_eval_time=MAX_EVAL_TIME,
                        time_to_try_again=TIME_TO_TRY_AGAIN, checkpoint_every=CHECKPOINT_EVERY,
                        save_vxa_every=SAVE_VXA_EVERY, save_lineages=SAVE_LINEAGES)

else:
    continue_from_checkpoint(directory=RUN_DIR, additional_gens=EXTRA_GENS, max_hours_runtime=MAX_TIME,
                             max_eval_time=MAX_EVAL_TIME, time_to_try_again=TIME_TO_TRY_AGAIN,
                             checkpoint_every=CHECKPOINT_EVERY, save_vxa_every=SAVE_VXA_EVERY,
                             save_lineages=SAVE_LINEAGES)

