PyvoTune
=========

Python Evolutionary Parametric Hypertuning
------------------------------------------

PyvoTune is designed to make implementing an evolutionary strategy based hypertuning mechanism for your existing applications easy to do using syntactic sugar.

## Disclaimer

PyvoTune is a work in progress, there has been no major release yet.

## Examples

### Relativity the easy way!


    Generation Evaluation      Worst       Best     Median    Average    Std Dev
    ---------- ---------- ---------- ---------- ---------- ---------- ----------
           493      98800 8.81825889 2.23565548 4.30806327 3.53779184 1.81638187

	0 3,655,044,673,627,861,549,056. 3,657,287,779,091,636,813,824. 2,243,105,463,775,264,768. 0.061370%
    1 -969,562,359,305,185,656,832. -970,157,380,932,979,654,656. 595,021,627,793,997,824. 0.061370%
    2 8,437,443,878,855,858,192,384. 8,442,621,948,664,764,956,672. 5,178,069,808,906,764,288. 0.061370%
    3 8,008,594,387,571,613,630,464. 8,013,509,271,910,479,822,848. 4,914,884,338,866,192,384. 0.061370%
    4 2,362,896,001,681,791,647,744. 2,364,346,113,898,112,876,544. 1,450,112,216,321,228,800. 0.061370%

    Actual Solution:E = m * 299792458 * 299792458
    Best Solution: E = m * 98580454.4765 / 10115015.3646 * -95281008.7998 * -96845007.0946
    Actual C: 89875517873681764
    Our C: 8.99306745908e+16
    Diff: 5.51567171528e+13
    Diff Pct: 0.06
    Fitness 2.23565548937e+20
    MSE 1.16913786619e+37

This *very* contrived example essentially is guessing at the speed of light. What it is doing is generating an equation attempting to approximate E=mc^2.

### Boston Home Price Regression


    $ time python samples/boston/main.py
    
    Generation Evaluation      Worst       Best     Median    Average    Std Dev
    ---------- ---------- ---------- ---------- ---------- ---------- ----------
             0        100        inf 7.34668954 41.3256808        inf        nan
         
    Generation Evaluation      Worst       Best     Median    Average    Std Dev
    ---------- ---------- ---------- ---------- ---------- ---------- ----------
             1        200 224.844920 7.34668954 30.1042747 35.5401870 35.4997440
         
    Generation Evaluation      Worst       Best     Median    Average    Std Dev
    ---------- ---------- ---------- ---------- ---------- ---------- ----------
             2        300 54.5085468 7.30813494 12.2143726 19.1619154 13.1476481
         
    Generation Evaluation      Worst       Best     Median    Average    Std Dev
    ---------- ---------- ---------- ---------- ---------- ---------- ----------
             3        400 30.9871428 7.07872928 8.71327343 9.90077064 3.32779459

    Generation Evaluation      Worst       Best     Median    Average    Std Dev
    ---------- ---------- ---------- ---------- ---------- ---------- ----------
             4        500 11.2183600 7.07872928 7.78732169 8.27628039 1.15729929

    Generation Evaluation      Worst       Best     Median    Average    Std Dev
    ---------- ---------- ---------- ---------- ---------- ---------- ----------
             5        600 11.3144702 7.07872928 7.74535805 7.96155504 0.86525738

      # Actual Observed Err %
    --- ------ -------- -----
    000 29.8   29.1333333333 2.24
    001 12.6   15.4272727273 22.44
    002 24.4   22.6060606061 7.35
    003 19.8   21.5636363636 8.91
    004 24.4   24.1787878788 0.91
    005 32.0   26.9909090909 15.65
    006 33.1   30.8757575758 6.72
    007 12.0   15.1515151515 26.26
    008 19.1   22.1515151515 15.98
    009 16.2   16.2151515152 0.09
    MSE: 13.1558693469
    Avg Err %: 9.28
    Genome: 9n1yF7
    	Gene 0: RandomForestRegressor
	    	Param 0: n_estimators: int - 33
		    Param 1: min_density: float - 0.590620781629
    		Param 2: n_jobs: const - 1
    		Param 3: bootstrap: bool - True
    		
    real	7m4.479s

This example uses the [Boston Housing Dataset](http://archive.ics.uci.edu/ml/datasets/Housing) to show how PyEvoTune can be used with sklearn to optimize pipelines. The real triumph here is the implementation cost and how little understanding we or the algorithm have in the problem domain. Allowing the algorithm to run longer would presumably generate more accurate results.

* * *

### License

* Authored by Amir Elaguizy <aelaguiz@gmail.com>
* Distributed under MIT License, see *LICENSE.md*