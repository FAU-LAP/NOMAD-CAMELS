---
layout: default
title: Plots in Protocols
parent: Quick Start
nav_order: 4
---

## 0. Table of contents
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

# 1. Plots
You can display live-plots in the measurement protocols to have a better understanding of what is going on during the measurement. 
## 1.1. Configure Plots
To configure the plots simply click `Define Plots / Fits`. Here we bill be doing this for the for-loop measurement protocol created [here](#23-sweeping-using-a-for-loopstep)
<p float="left">
  <img src="img_48.png" width="75%" />
</p>

Add a new plot by clicking the &#10133; symbol and choosing a plot type.

<p float="left">
  <img src="img_49.png" width="40%" />
</p>

The `x-axis` is set by either typing the channel into the field or by simply right-clicking and adding the channel value with `Insert Channel Value`. We will be plotting the `motorZ` channel (y-axis) against `For_Loop_Count` (x-axis). Add a new y-axis with the &#10133; symbol next to `y-axes`. Enter the `motorZ` channel via right click into the `formula` field. As with most fields you can to any mathematical operation as a string in this field (see examples above for more information). Select if the y-axis should be plotted on the left or right side of the x-axis. \
![img_50.png](img_50.png)

Give the plot a `x-label` and `y-label` as well as a `title`. 

A finished plot configuration (without a fit) could look like this for example
![img_51.png](img_51.png)
## 1.2. Run Protocol with Plots
If you then run the protocol the plot is displayed and updated live.
<p float="left">
  <img src="img_52.png" width="80%" />
</p>

> &#9888; To get this plot you have to modify the protocol from [before](#23-sweeping-using-a-for-loopstep) by adding a small `Wait` time of `0.1` seconds as the internal software sweep is too fast for the plot to follow.\
> ![img_53.png](img_53.png)


[&#8679; Back to the top &#8679;](#0-table-of-contents)
<p style="text-align:left;">
  <span style="color: grey;">
  <a href="quick_start_manual_control.html">&larr; Back</a>
  </span>
  <span style="float:right;">
    <a href="../users_guide.html">Next &rarr;</a><br>
  </span>
</p>