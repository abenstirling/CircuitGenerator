## Problem
Electrical Engineering is time consuming, convoluted and very analytical. It can take weeks to produce a single iteration of a Printed Circuit Board (PCB), and even months to years for more complicated boards in industry. 

## Solution
We built a tool to generate circuit designs in a matter of seconds. This allows for  orders of magnitudes faster rapid prototyping and lowers the barrier to board design and practical electrical engineering. 

## How we built it
Our project has three main components: 
1.  Synthetic Circuit Analysis + Data generation
2. Custom Neural Network 
3. Physical Circuit Analyzer 

## Challenges we ran into
1. We started from scratch
2. Our computers limited our time to iterate, since the data generation took 4hrs/10,000 samples
3. Unable to deploy Android App to Qualcomm Device because we were unable to boot Ubuntu (No VM in Vm) given our setup

## Accomplishments that we're proud of
1. Starting from scratch 
2. Training and tuning 
3. Making a functional and effective solution to a personal and professional problem

## What we learned
1. How to clock hardware for accurate noise reading
2. How to write a functional neural net from scratch
3. Numpy and itertools libraries

## What's next for Superpowers For Electrical Engineers
1. Expand training data to non-linear components (MOSFETs, ICs) 
2. Create an effective datasheet parser and scraper
3. Make a chat-based circuit generation solution
