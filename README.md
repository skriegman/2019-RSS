Automated shapeshifting for function recovery in damaged robots
--------------------
Sam Kriegman, Stephanie Walker, Dylan Shah, Michael Levin, Rebecca Kramer-Bottiglio, Josh Bongard.<br>
In Proceedings of _Robotics: Science and Systems (RSS)_, 2019. <br>
June 22-26, 2019. Freiburg im Breisgau, Germany.<br>

<a href="http://www.roboticsproceedings.org/rss15/p28.pdf">Read the full paper.</a>

<a href="https://youtu.be/fFIDz8maVh0">Watch an annotated summary video.</a>

<a href="https://youtu.be/stYJ1Miesk4">Watch the oral presentation from RSS (4 mins).</a>


Bibtex
------------

@inproceedings{kriegman2019automated, <br> 
    author={Kriegman, Sam and Walker, Stephanie and Shah, Dylan and Levin, Michael and Kramer-Bottiglio, Rebecca and Bongard, Josh}, <br>
    title={Automated Shapeshifting for Function Recovery in Damaged Robots}, <br>
    booktitle={Proceedings of Robotics: Science and Systems}, <br>
    year={2019}, <br>
    doi={10.15607/RSS.2019.XV.028}, <br>
    url={http://www.roboticsproceedings.org/rss15/p28.pdf} <br>
} <br>


Installation
------------

Install [Anaconda](https://docs.continuum.io/anaconda/install#) as your Python (2.7) distribution. Anaconda is a free package manager and Python distribution that includes all of the dependencies required for evosoro. However if you instead choose to manually install Python 2.7, the following packages are required: scipy, numpy, networkx, decorator.

Important: networkx must be <2.0. When networkx updated 1.0-->2.0 some function changed and I haven't updated the python code to reflect this change.

    pip install networkx==1.11


Install Qt and QMake if you have not already done so, specifically these packages: "libqt4-dev", "qt4-qmake", "libqwt-dev", "freeglut3-dev" and "zlib1g-dev".

    sudo apt-get install libqt4-dev qt4-qmake libqwt-dev freeglut3-dev zlib1g-dev


Install git if you have not already done so.

    sudo apt-get install git

Navigate to your working directory (e.g. your home).

    cd ~

Clone the repo.

    git clone https://github.com/skriegman/2019-RSS.git

There are different well documented examples (evosoro/examples) and custom versions of VoxCad/Voxelyze included in this repository (evosoro/_voxcad* folders).
Let's try running an example in which soft robots are optimized to locomote in a terrestrial environment, using an evolutionary algorithm and a basic version (_voxcad) of the physics engine (the procedure is the same for all the examples). 

Navigate to the _voxcad directory:

    cd evosoro/evosoro/_voxcad/

The following command compiles both VoxCad and Voxelyze, installing the library at the same time:

    ./rebuild_everything.sh

If you happen to modify VoxCad or Voxelyze in the future, you can call the same script to be sure to clean and recompile everything. 

    make

Install the voxelyze library.

    cd Voxelyze
    make
    make installusr
    cd ../voxelyzeMain/
    make

Navigate back out to the exp folder and run one of the *.py with two args (seed and runtime):
    
    cd ../exp
    python RSS_0B_Half_Leg_XYZDB.py 1 1

You should start seeing some output being produced in your console, and a new directory being created (evosoro/evosoro/basic_data), which contains the results of the simulation.


After allowing the experiment to run for a few generations, you can view the shape/controller adaptation by opening up the generated .vxa files within the VoxCAD GUI. A .vxa file is just an XML file representing a robot that can be simulated by VoxCad/Voxelyze. Different versions of the physics engine can play slightly different .vxa files.
Navigate to evosoro/evosoro/_voxcad/release:
    
    cd ../_voxcad/release
    
Open VoxCad:

    ./VoxCad

Then select the desired .vxa file from 

    "File -> Import -> Simulation"

The .vxa files for the best performing individuals will be saved in the working dir inside a run_* where * is the seed (we used 1 as the first arg)

    evosoro/evosoro/exp/run_1/bestSoFar/fitOnly.

Once the design is loaded, you can start the physics simulation by clicking the <img src="https://github.com/skriegman/evosoro/blob/master/evosoro/_voxcad/VoxCad/Icons/Sandbox.png" height="25" width="25"> icon in the top bar ("Physics Sandbox").  The robot should start moving: if it doesn't, please check the following section (Known issues).


Known issues
--------

If the robot does not move, disappears, or seems to behave in an unexpected manner when running a .vxa file in VoxCad (GUI), you may be affected by a known problem observed on some non-US machines.
The problem is due to an unexpected behavior of the <a href="http://www.cplusplus.com/reference/cstdlib/atof/">atof</a> function when the system's numeric <a href="https://en.wikipedia.org/wiki/Locale_(computer_software)">locale</a> differs from en_US.UTF-8, which entails loading wrong parameters from the .vxa file (in some cases it was observed how the atof function was approximating all double and floating point values to their integer part, which was the cause of the unexpected behavior).

While we work on a better solution, you can fix this problem by making sure that your machine is configured according to a US numeric locale.
Open the following file:

    sudo gedit /etc/default/locale

Make sure that LC_NUMERIC is set as follows:

    LC_NUMERIC="en_US.UTF-8"

Save, close the file, and reboot.


Documentation
-------------

Voxelyze documentation, available [here](http://jonhiller.github.io/Voxelyze/annotated.html).


