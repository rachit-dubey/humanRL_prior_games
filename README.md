## Investigating Human Priors for Playing Video Games ##
#### In ICML 2018 [[Project Website]](https://rach0012.github.io/humanRL_website/) 
![Games](screens.png?raw=True "Games!")

[Rachit Dubey](http://cocosci.berkeley.edu/rachit/), [Pulkit Agrawal](https://people.eecs.berkeley.edu/~pulkitag/), [Deepak Pathak](https://people.eecs.berkeley.edu/~pathak/), [Thomas L. Griffiths](http://cocosci.berkeley.edu/tom/tom.php), [Alexei A. Efros](https://people.eecs.berkeley.edu/~efros/)<br/>
University of California, Berkeley<br/>

This contains code for our suit of custom games built to test performance of RL agents for our paper 'Investigating Human Priors for Playing Video Games' published in ICML 2018.

The 'original game' is a simple platformer game. The 'no semantics' is the game which removes semantic information prior. The 'no object' is the game which removes concept of object prior. The 'no affordance' is the game which removes affordance prior. The 'no similarity' is the game which masks similarity prior. 

Refer to our paper available here for more details - https://arxiv.org/abs/1802.10217

We used the PyGame-Learning-Environment to build these games - https://github.com/ntasfi/PyGame-Learning-Environment. 
All the games are based on the codes from the game 'MonsterKong' from PLE. 

To train your RL agent on the games, you would also need gym-ple, a package that allows to use PLE as a gym environment. Our version of gym-ple which includes our games is available here - https://github.com/rach0012/humanRL_gym_ple/

If you find this work useful in your research, please cite:

    @inproceedings{dubeyICMl18humanRL,
        Author = {Dubey, Rachit and Agrawal, Pulkit
    and Pathak, Deepak and Griffiths, Thomas L.
    and Efros, Alexei A.},
        Title = {Investigating Human Priors for
    Playing Video Games},
        Booktitle = {International Conference on Machine Learning ({ICML})},
        Year = {2018}
    }


## Getting started

A `PLE` instance requires a game exposing a set of control methods. To see the required methods look at `ple/games/base.py`. 

Here's an example of importing the original game from the games library within PLE:

```python
from ple.games.originalGame import originalGame

game = originalGame()
```

Next we configure and initialize PLE:

```python
from ple import PLE

p = PLE(game, fps=30, display_screen=True, force_fps=False)
p.init()
```

The options above instruct PLE to display the game screen, with `display_screen`, while allowing PyGame to select the appropriate delay timing between frames to ensure 30fps with `force_fps`.

You are free to use any agent with the PLE. Below we create a fictional agent and grab the valid actions:

```python
myAgent = MyAgent(p.getActionSet())
```

We can now have our agent, with the help of PLE, interact with the game over a certain number of frames:

```python

nb_frames = 1000
reward = 0.0

for f in range(nb_frames):
	if p.game_over(): #check if the game is over
		p.reset_game()

	obs = p.getScreenRGB()
	action = myAgent.pickAction(reward, obs)
	reward = p.act(action)

```

Just like that we have our agent interacting with our game environment.

## Installation

PLE requires the following dependencies:
* numpy
* pygame
* pillow

Clone the repo and install with pip.

```bash
git clone https://github.com/ntasfi/PyGame-Learning-Environment.git
cd PyGame-Learning-Environment/
pip install -e .
``` 

## Headless Usage

Set the following in your code before usage:
```python
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.environ["SDL_VIDEODRIVER"] = "dummy"
```
