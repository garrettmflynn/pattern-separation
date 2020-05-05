# pattern-separation
 A gesture-controlled interface for visualizing hippocampal dynamics

In the human brain, the hippocampus is theorized to transform non-simultaneous input patterns into less similar output patterns in a process known as "pattern separation", allowing us to distinguish similar memories from one another.

In **pattern-separation**, we created a custom version of Visbrain to visualize the dynamic activity of the hippocampus during a delayed match-to-sample memory task. Additionally, an Arduino distance sensor was used as a gesture-controlled interface to increase/decrease the amount of "pattern separation" within the Visbrain window.

[![Github badge](https://img.shields.io/badge/github-source_code-blue.svg?logo=github&logoColor=white)](https://github.com/garrettmflynn/pattern-separation)
[![License badge](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

* [Installation](#Installation)
* [Usage](#Usage)
* [Interaction](#Installation)
* [Dependencies](#DEPENDENCIES)
* [Support](#SUPPORT)
* [Acknowledgements](#ACKNOWLEDGEMENTS)

## Installation
### Code
1. Clone or download the [pattern-separation](https://github.com/garrettmflynn/pattern-separation) repository

2. Install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/).

3. Create a conda environment from the environment.yml file.

```bash
$ conda env create -f environment.yml
```
### Hardware
![tinkercad circuit](images/tinkercad.png)

### Example System
#### Breadboard Test
![distance sensor breadboard](images/distance_sensor_breadboard.jpg)

#### Final Enclosure
Outside                         |  Inside
:------------------------------:|:------------------------------:
![](images/form_1_outside.jpg)  |  ![](images/form_1_inside.jpg)

## Usage
Default Settings upon Installation:
* Synthetic Data
* Keyboard Control

### Run with **Default Settings**
Enter the pattern-separation directory, then run pattern-separation.py.
```bash
$ python pattern-separation.py
```
### Load **Custom Data**
Example scripts for loading your own binary signals are included in the /custom folder.

Enter the pattern-separation directory, then run pattern-separation.py.
```bash
$ python pattern-separation.py
```

### Enable **Remote + Gesture Control**
On line 80, replace 
```python
id.episode(shader='separation', control_method='keyboard')
```
with
```python
id.episode(shader='separation', control_method='Remote_Gesture)
```

## DEPENDENCIES
This project uses the following libraries:
* ???
* ???
* ???
* ???
* ???
* ???

## SUPPORT

If you are having issues, please email me at garrett@garrettflynn.com

## ACKNOWLEDGEMENTS
This code was created for IML 404 (Tangible and Spatial Computing) taught by [John Carpenter](http://www.johnbcarpenter.com/) at the University of Southern California, and heavily influenced by my work with Dong Song at the [USC Center for Neural Engineering](https://cne.usc.edu/).