# bomberman

Gameplay
========
The player must navigate Bomberman through a maze by destroying soft blocks and enemies with his bombs. Hidden in every stage is one item that will either increase his blast radius, spped. The player must find the goal that is hidden under one of the soft blocks and defeat all the enemies to open it. There are {TODO} levels in total.

Representation
==============

```
Bomberman
[^^]
 ][
 ```

```
Wall
####
####
```

```
Brick
%%%%
%%%%
```


```
Bomb Timer
3333
3333
```

```
Explosion
eeee
eeee
```

```
Enemy 1
\--/
/aa\
```

```
Enemy 2
\--/
/bb\
```

```
Enemy 3
\--/
/cc\
```

```
Enemy 4
\@@/
/@@\
```

Controls
========

w: Move Up
a: Move left
s: Move down
d: Move right

b: Plant Bomb
space: Pause Game
q: Quit Game
p: Powerup


OOPS Concepts
=============

Modularity
----------
Each elemennt has been decomposed into independant modules

Inheritence
-----------
Player and Enemy classes are inheriting from Person class as they have a lot of variables and member functions in common


Polymorphism
------------


Encapsulation
-------------
Only the required functions are public in each class otherwise every variable and function is private.
