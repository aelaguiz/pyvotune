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
    
    …
    
    Generation Evaluation      Worst       Best     Median    Average    Std Dev
    ---------- ---------- ---------- ---------- ---------- ---------- ----------
            24       1250 11.0346785 4.53306810 6.46303394 6.57444884 1.26032606

      # Actual Observed Err %
    --- ------ -------- -----
    000 34.9   30.1370242847 13.65
    001 30.8   30.6372567011 0.53
    002 17.3   15.8452022367 8.41
    003 45.4   47.5934588348 4.83
    004 23.6   25.347864608 7.41
    005 33.1   33.1862479121 0.26
    006 10.4   15.9982080446 53.83
    007 17.4   22.1055749735 27.04
    008 23.3   21.6639578698 7.02
    009 20.6   22.1880883774 7.71
    MSE: 7.72680473303
    Avg Err %: 9.32
    Genome: 6KMfc5
    	Gene 0: Scaler
    		Param 0: with_std: bool - True
    	Gene 1: GradientBoostingRegressor
    		Param 0: n_estimators: int - 241
    		Param 1: max_features: int - 7
    		Param 2: learning_rate: float - 0.182539777357
    		Param 3: subsample: float - 0.708019800365


    real	5m35.501s

This example uses the [Boston Housing Dataset](http://archive.ics.uci.edu/ml/datasets/Housing) to show how PyvoTune can be used with sklearn to optimize pipelines. The real triumph here is the implementation cost and how little understanding we or the algorithm have in the problem domain. Allowing the algorithm to run longer would presumably generate more accurate results.


### Digit Recognition Classification

    Generation Evaluation      Worst       Best     Median    Average    Std Dev
    ---------- ---------- ---------- ---------- ---------- ---------- ----------
            10        550          0      98.21        0.0    36.6346 46.8393266

                 precision    recall  f1-score   support

              0       1.00      1.00      1.00        19
              1       0.95      0.95      0.95        19
              2       1.00      1.00      1.00        19
              3       1.00      1.00      1.00        25
              4       1.00      0.94      0.97        16
              5       0.89      1.00      0.94        16
              6       1.00      0.95      0.97        20
              7       0.97      1.00      0.98        31
              8       1.00      0.97      0.99        36
              9       1.00      1.00      1.00        24

    avg / total       0.98      0.98      0.98       225

    Fitness: 98.21
    Genome: VlQ5c
    	Gene 0: ExtraTreesClassifier
    		Param 0: criterion: choice - entropy
    		Param 1: n_estimators: int - 291
    		Param 2: min_density: float - 0.582296870215
    		Param 3: n_jobs: const - 1
    		Param 4: bootstrap: bool - False
    		Param 5: oob_score: bool - False


    real	5m46.102s

We use

* * *

### License

* Authored by Amir Elaguizy <aelaguiz@gmail.com>
* Distributed under MIT License, see *LICENSE.md*