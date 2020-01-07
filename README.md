Automated shapeshifting for function recovery in damaged robots
--------------------
[Sam Kriegman](https://scholar.google.com/citations?user=DCIwaLwAAAAJ), 
[Stephanie Walker](https://scholar.google.com/citations?user=0xspn9YAAAAJ), 
[Dylan Shah](https://scholar.google.com/citations?user=bfxXEJkAAAAJ), 
[Michael Levin](https://scholar.google.com/citations?user=luouyakAAAAJ), 
[Rebecca Kramer-Bottiglio](https://scholar.google.com/citations?user=2ARbFNoAAAAJ),
and 
[Josh Bongard](https://scholar.google.com/citations?user=Dj-kPasAAAAJ).<br>

<img src="https://github.com/skriegman/2019-RSS/blob/master/misc/teaserA.png" width="750"> <br>
<img src="https://github.com/skriegman/2019-RSS/blob/master/misc/teaserB.png" width="750">

<a href="http://www.roboticsproceedings.org/rss15/p28.pdf">Read the full paper.</a>

<a href="https://www.nature.com/articles/s42256-019-0076-6.epdf?author_access_token=R-S3FjSBIhUsomuDvARA7dRgN0jAjWel9jnR3ZoTv0OIXKmCfd5tDZfG1f8Y5jvWw1CSopZsGNYUdE_VbrVz-w5iIfuBDqNnm4FKFVTmuh3hNAJu38EzDsJc8di2AANa1jSA3LV3Q3Vd-wov1l5Amw%3D%3D">Read a perspective article on this work, published in Nature Machine Intelligence.</a>

<!-- <a href="https://youtu.be/fFIDz8maVh0">Watch an annotated video summary.</a> -->
<a href="https://youtu.be/2VVzz6YBWvc">Watch an annotated video summary.</a>

<a href="https://youtu.be/stYJ1Miesk4">Listen to the oral presentation from RSS (4 mins).</a>


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

The first step is to install [Anaconda](http://docs.continuum.io/anaconda/install/linux/) as your 
<b>python 2.7</b> distribution on a linux machine.

But revert Anaconda's networkx <2.0.

    pip install networkx==1.11

Install Qt and QMake, specifically these packages: "libqt4-dev", "qt4-qmake", "libqwt-dev", "freeglut3-dev" and "zlib1g-dev".

    sudo apt-get install libqt4-dev qt4-qmake libqwt-dev freeglut3-dev zlib1g-dev


Install git.

    sudo apt-get install git

Navigate to the working directory (e.g., your home).

    cd ~

Clone the repo.

    git clone https://github.com/skriegman/2019-RSS.git

Navigate to the _voxcad directory.

    cd 2019-RSS/_voxcad/

Compile both VoxCad (GUI) and Voxelyze (physics engine).

    ./rebuild_everything.sh

If you happen to modify VoxCad or Voxelyze in the future, call the same script to clean and recompile everything. 

    make

Install the voxelyze library.

    cd Voxelyze
    make
    cd ../voxelyzeMain/
    make

Navigate to the exp folder and run one of the .py experiments (detailed in the paper),
which require two input args (seed and runtime), both of which can be set to 1 for now.
    
    cd ../exp
    PYTHONPATH=$HOME/2019-RSS/ $HOME/anaconda/bin/python RSS_0B_Half_Leg_XYZDB.py 1 1

This creates a directory (~/2019-RSS/evosoro/run_1) to hold the results.

Output should appear in the console.

After the experiment runs for a few generations, 
the current shape/controller adaptation can be seen by opening 
one of the generated .vxa files within the VoxCAD GUI. 
A .vxa file is just an XML file representing a robot that can be simulated by VoxCad/Voxelyze.

Navigate to 2019-RSS/evosoro/_voxcad/release.
    
    cd ../_voxcad/release
    
Open VoxCad.

    ./VoxCad

Then select the desired .vxa file from:

    "File -> Import -> Simulation"

The .vxa files for the best performing individuals will be saved in:

    2019-RSS/evosoro/exp/run_1/bestSoFar/fitOnly.

Once the robot is loaded, you can start the physics simulation by clicking the <img src="https://github.com/skriegman/2019-RSS/blob/master/_voxcad/VoxCad/Icons/Sandbox.png" height="25" width="25"> icon in the top bar ("Physics Sandbox").


A known issue with non-US machines
--------

If the system's numeric 
<a href="https://en.wikipedia.org/wiki/Locale_(computer_software)">locale</a> 
differs from en_US.UTF-8, the 
<a href="http://www.cplusplus.com/reference/cstdlib/atof/">atof</a> 
function might read double and floating point values in the .vxa 
as integers.
 
This will cause the robot not to move, disappear, or just behave strangely 
when running a .vxa file in VoxCad.

To fix this issue, open the locale settings.

    sudo gedit /etc/default/locale

Set LC_NUMERIC to en_US.UTF-8.

    LC_NUMERIC="en_US.UTF-8"

Save, close the file, and reboot.


Documentation
-------------

Voxelyze documentation is available [here](http://jonhiller.github.io/Voxelyze/annotated.html).


