# Jupyter notebook line movement tracker


### Move

Can have probability

* Total Move
	* len(child) == len(parent), All $a \in child$, are also $\in parent$

* Add parent Move
	* len(child) < len(parent), All $ a \in child$, are also $\in parent$

* Add child Move
	* len(child) > len(parent), All $ b \in parent$ are also $\in child$

* Mul Move
	* len(child) $\neq$ len(parent), Exist some $a \in child$ are also $\in parent$

### Split

* Exist at least two parent such that $a \in P_{1}$ and $b \in P_{2}$ where $a,b \in C$, so C is split.


### Merge

* Exist at least two child such that $a \in C_{1}$ and $b \in C_{2}$ where $a,b \in P$, so P is split.


### Add

For all $b \in parent$ not exist $b \in$ any child.

* By index 
	* first
	* middle
	* last


### Delete

For all $a \in child$ not exist $a \in$ any parent.


* By index
	* first
	* middle
	* last






### Types of Block mapping

#### Block Split

<center> ![alt_text](png/block_split.png)</center>

#### Block reorder

<center> ![alt_text](png/reorder.png)</center>


#### Block Add

<center> ![alt_text](png/add.png)</center>


#### ???

<center> ![alt_text](png/un.png)</center>



