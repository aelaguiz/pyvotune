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

* * *

### License

* Authored by Amir Elaguizy <aelaguiz@gmail.com>
* Distributed under MIT License, see *LICENSE.md*