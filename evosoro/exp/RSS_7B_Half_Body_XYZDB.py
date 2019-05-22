import random
import os
import sys
import cPickle
import numpy as np
import subprocess as sub

from evosoro.base import Sim, Env, ObjectiveDict
from evosoro.networks import DirectEncoding, CPPN, GeneralizedCPPN
from evosoro.softbot import Genotype, Phenotype, Population
from evosoro.tools.algorithms import ParetoOptimization
from evosoro.tools.checkpointing import continue_from_checkpoint
from evosoro.tools.utils import quadruped, count_neighbors


SIMULATOR_DIR = "~/pkg/research_code/evosoro/_voxcad"
PICKLE_DIR = "/users/s/k/skriegma/scratch/quadrupeds"
# SIMULATOR_DIR = "../_voxcad"
# PICKLE_DIR = "/home/sam"

SEED = int(sys.argv[1])
MAX_TIME = float(sys.argv[2])
# SEED = 1
# MAX_TIME = 1

PICKLE_GEN = 1500
PICKLE = "{0}/run_{1}/pickledPops/Gen_{2}.pickle".format(PICKLE_DIR, (SEED-1) % 5 + 1, PICKLE_GEN)

QUAD_SIZE = (6, 6, 5)
IND_SIZE = QUAD_SIZE
STIFFNESS = 1e7

POP_SIZE = 50
MAX_GENS = 5000
NUM_RANDOM_INDS = 1

INIT_TIME = 0.4
SIM_TIME = 4 + INIT_TIME  # includes init time
TEMP_AMP = 39.4714242553  # 50% volumetric change with temp_base=25: (1+0.01*(39.4714242553-25))**3-1=0.5
FREQ = 5.0

DT_FRAC = 0.3
MIN_TEMP_FACT = 0.25

GROWTH_AMPLITUDE = 1

TIME_TO_TRY_AGAIN = 30
MAX_EVAL_TIME = 75

SAVE_VXA_EVERY = MAX_GENS+1  # never
CHECKPOINT_EVERY = 1  # gen(s)

FITNESS_TAG = "normAbsoluteDisplacement"

RUN_DIR = "run_{}".format(SEED)
RUN_NAME = "RegenQuad"

# copy the simulator executable into the working directory
sub.call("cp {}/voxelyzeMain/voxelyze .".format(SIMULATOR_DIR), shell=True)
sub.call("chmod 755 voxelyze", shell=True)

# load pickle from training data and extract the run champion
MyPhenotype = Phenotype
MyGenotype = Genotype
with open(PICKLE, 'rb') as handle:
    [optimizer, random_state, numpy_random_state] = cPickle.load(handle)

train_pop = optimizer.pop
MyPhenotype = train_pop.phenotype
MyGenotype = train_pop.genotype

# get the current run champion
starting_robot = None
for ind in train_pop:
    if ind.fitness == train_pop.best_fit_so_far:
        starting_robot = ind

CONTROLLER_0 = starting_robot.genotype.to_phenotype_mapping["phase_offset"]["state"]
CONTROLLER = np.rot90(CONTROLLER_0, k=(SEED-1)/5, axes=(0, 1))

pre_damage_shape = quadruped(QUAD_SIZE)
post_damage_shape = quadruped(QUAD_SIZE)
post_damage_shape[:IND_SIZE[1]/2, :IND_SIZE[1]/2, :] = 0  # quarter 1
post_damage_shape[IND_SIZE[1]/2:, :IND_SIZE[1]/2, :] = 0  # quarter 2
# post_damage_shape[:IND_SIZE[1]/2, IND_SIZE[1]/2:, :] = 0  # quarter 3
# post_damage_shape[IND_SIZE[1]/2:, IND_SIZE[1]/2:, :] = 0  # quarter 4


# calculate manhattan distance from the site of damage
geom_new = np.array(post_damage_shape > 0, dtype=int)
geom_old = np.array(pre_damage_shape > 0, dtype=int)
geom_diff = geom_old - geom_new

first_block = np.reshape(count_neighbors(geom_diff), IND_SIZE)
first_block[np.where(geom_new == 0)] = 0
already_counted = np.array(first_block > 0, dtype=int)
blocks = [first_block]
n = 1
while True:
    this_block = np.reshape(count_neighbors(blocks[n-1]), IND_SIZE)
    this_block[np.where(geom_new == 0)] = 0
    this_block[np.where(this_block > 0)] = 1
    this_block[np.where(already_counted > 0)] = 0
    already_counted += this_block
    blocks += [this_block]
    n += 1

    if np.sum(already_counted - geom_new) == 0:
        break

manhattan = np.zeros(IND_SIZE)
for n, b in enumerate(blocks):
    manhattan += n*b

# print n-1
# print manhattan

MyGenotype.NET_DICT = {"phase_offset": CONTROLLER, "material": post_damage_shape}


class MyGenotype(Genotype):
    def __init__(self):
        Genotype.__init__(self, orig_size_xyz=IND_SIZE)

        self.add_network(DirectEncoding(output_node_name="phase_offset", orig_size_xyz=IND_SIZE), freeze=True)
        self.to_phenotype_mapping.add_map(name="phase_offset", tag="<PhaseOffset>", logging_stats=None)

        self.add_network(DirectEncoding(output_node_name="material", orig_size_xyz=IND_SIZE), freeze=True)
        self.to_phenotype_mapping.add_map(name="material", tag="<Data>", output_type=int, logging_stats=None)

        self.add_network(CPPN(output_node_names=["init_size"]))
        self.to_phenotype_mapping.add_map(name="init_size", tag="<InitialVoxelSize>")


if not os.path.isfile("./" + RUN_DIR + "/pickledPops/Gen_0.pickle"):

    random.seed(SEED)
    np.random.seed(SEED)

    my_sim = Sim(dt_frac=DT_FRAC, simulation_time=SIM_TIME, fitness_eval_init_time=INIT_TIME,
                 min_temp_fact=MIN_TEMP_FACT)

    my_env = Env(temp_amp=TEMP_AMP, frequency=FREQ, muscle_stiffness=STIFFNESS, growth_amp=GROWTH_AMPLITUDE)

    my_objective_dict = ObjectiveDict()
    my_objective_dict.add_objective(name="fitness", maximize=True, tag=FITNESS_TAG)
    my_objective_dict.add_objective(name="age", maximize=False, tag=None)

    my_pop = Population(my_objective_dict, MyGenotype, Phenotype, pop_size=POP_SIZE)

    my_optimization = ParetoOptimization(my_sim, my_env, my_pop)
    my_optimization.run(max_hours_runtime=MAX_TIME, max_gens=MAX_GENS, num_random_individuals=NUM_RANDOM_INDS,
                        directory=RUN_DIR, name=RUN_NAME, max_eval_time=MAX_EVAL_TIME,
                        time_to_try_again=TIME_TO_TRY_AGAIN, checkpoint_every=CHECKPOINT_EVERY,
                        save_vxa_every=SAVE_VXA_EVERY)

else:
    continue_from_checkpoint(directory=RUN_DIR, max_hours_runtime=MAX_TIME, max_eval_time=MAX_EVAL_TIME,
                             time_to_try_again=TIME_TO_TRY_AGAIN, checkpoint_every=CHECKPOINT_EVERY,
                             save_vxa_every=SAVE_VXA_EVERY)
