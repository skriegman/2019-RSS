Automated shapeshifting for function recovery in damaged robots
--------------------
Sam Kriegman, Stephanie Walker, Dylan Shah, Michael Levin, Rebecca Kramer-Bottiglio, Josh Bongard.<br>

<img src="https://github.com/skriegman/2019-RSS/blob/master/misc/teaserA.png" width="750"> <br>
<img src="https://github.com/skriegman/2019-RSS/blob/master/misc/teaserB.png" width="750">

<a href="http://www.roboticsproceedings.org/rss15/p28.pdf">Read the full paper.</a>

<a href="https://youtu.be/fFIDz8maVh0">Watch an annotated summary video.</a>

<a href="https://youtu.be/stYJ1Miesk4">Watch the oral presentation from RSS (4 mins).</a>


Bibtex
------------
<pre>
@inproceedings{kriegman2019automated,
&nbsp;&nbsp; author={Kriegman, Sam and Walker, Stephanie and Shah, Dylan and Levin, Michael and Kramer-Bottiglio, Rebecca and Bongard, Josh},
&nbsp;&nbsp; title={Automated shapeshifting for function recovery in damaged robots},
&nbsp;&nbsp; booktitle={Proceedings of Robotics: Science and Systems},
&nbsp;&nbsp; year={2019},
&nbsp;&nbsp; doi={10.15607/RSS.2019.XV.028},
&nbsp;&nbsp; url={<a href="http://www.roboticsproceedings.org/rss15/p28.pdf">http://www.roboticsproceedings.org/rss15/p28.pdf</a>}
}
</pre>


Installation
------------

The first step is to install [Anaconda](https://docs.continuum.io/anaconda/install#) as your Python 2.7 distribution on a linux machine.

Next, networkx must be <2.0. When networkx updated 1.0-->2.0 some function changed and I haven't updated the python code to reflect this change.

    pip install networkx==1.11


Install Qt and QMake if you have not already done so, specifically these packages: "libqt4-dev", "qt4-qmake", "libqwt-dev", "freeglut3-dev" and "zlib1g-dev".

    sudo apt-get install libqt4-dev qt4-qmake libqwt-dev freeglut3-dev zlib1g-dev


Install git if you have not already done so.

    sudo apt-get install git

Navigate to your working directory (e.g. your home).

    cd ~

Clone the repo.

    git clone https://github.com/skriegman/2019-RSS.git

Let's try running one of the experiments from the paper.

Navigate to the _voxcad directory:

    cd 2019-RSS/evosoro/_voxcad/

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

Navigate back out to the exp folder and run one of the .py experiments (detailed in the paper) with two args (seed and runtime; let's set both to 1 for now):
    
    cd ../exp
    python RSS_0B_Half_Leg_XYZDB.py 1 1

You should start seeing output in your console, and a newly created directory (~/2019-RSS/evosoro/run_1), which contains the results of the simulation.


After allowing the experiment to run for a few generations, you can view the current shape/controller adaptation by opening one of the generated .vxa files within the VoxCAD GUI. A .vxa file is just an XML file representing a robot that can be simulated by VoxCad/Voxelyze.
Navigate to 2019-RSS/evosoro/_voxcad/release:
    
    cd ../_voxcad/release
    
Open VoxCad:

    ./VoxCad

Then select the desired .vxa file from:

    "File -> Import -> Simulation"

The .vxa files for the best performing individuals will be saved in:

    2019-RSS/evosoro/exp/run_1/bestSoFar/fitOnly.

Once the robot is loaded, you can start the physics simulation by clicking the <img src="https://github.com/skriegman/2019-RSS/blob/master/evosoro/_voxcad/VoxCad/Icons/Sandbox.png" height="25" width="25"> icon in the top bar ("Physics Sandbox").


Known issues
--------

If the robot does not move, disappears, or behaves weirdly when running a .vxa file in VoxCad (GUI), you may be affected by a known problem observed on some non-US machines.
The problem is due to the <a href="http://www.cplusplus.com/reference/cstdlib/atof/">atof</a> function when the system's numeric <a href="https://en.wikipedia.org/wiki/Locale_(computer_software)">locale</a> differs from en_US.UTF-8, and can cause double and floating point values in the .vxa to be read as integers.

You can fix this problem by making sure that your machine is configured according to a US numeric locale.
Open the following file:

    sudo gedit /etc/default/locale

Make sure that LC_NUMERIC is set as follows:

    LC_NUMERIC="en_US.UTF-8"

Save, close the file, and reboot.


Documentation
-------------

Voxelyze documentation, available [here](http://jonhiller.github.io/Voxelyze/annotated.html).


