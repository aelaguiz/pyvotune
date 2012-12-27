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
             6        350      85.64      99.11      98.21    97.6118 2.68660431

                 precision    recall  f1-score   support

              0       1.00      1.00      1.00        29
              1       0.94      1.00      0.97        17
              2       1.00      1.00      1.00        32
              3       1.00      1.00      1.00        23
              4       1.00      1.00      1.00        23
              5       1.00      0.90      0.95        20
              6       1.00      1.00      1.00        19
              7       1.00      0.95      0.98        21
              8       1.00      0.96      0.98        24
              9       0.85      1.00      0.92        17

    avg / total       0.98      0.98      0.98       225

    Fitness: 99.11
    Genome: 2NWYgK
    	Gene 0: Normalizer
    		Param 0: norm: choice - l1
    	Gene 1: PCA
    		Param 0: whiten: bool - False
    	Gene 2: PCA
    		Param 0: whiten: bool - False
    	Gene 3: SVC
    		Param 0: C: float - 382.493666708
    		Param 1: kernel: choice - linear
    		Param 2: degree: int - 3
    		Param 3: gamma: float - 74.2633913798
    		Param 4: coef0: float - 7528.0708478
    		Param 5: shrinking: bool - True


    real	7m0.304s

Using the sklearn digit recognition dataset we evolve a classifier pipeline.

* * *

### License

* Authored by Amir Elaguizy <aelaguiz@gmail.com>
* Distributed under MIT License, see *LICENSE.md*