# **Sub-compartment Identifier (SCI)**
--------------

**Authors**: Haitham Ashoor, Sheng Li  **Contact**: haitham.ashoor@jax.org, sheng.li@jax.org


## Description 
SCI is a program to identify sub-compartments from HiC data. SCI utilizes graph embedding followed by K-means clustering in order to predict sub-compartments from HiC data. 

![SCI workflow](images/sci.jpg)

## Dependencies
* python 2.7

**Python Libraries**
* [scikit-learn] >=0.19.0 
* [Numpy] >= 1.15
* [tqdm]>=4.24

**C++ libraries**
* [GSL]

## Installation 

```sh
$ python setup.py
```
## Input format

SCI accepts [bedpe](https://bedtools.readthedocs.io/en/latest/content/general-usage.html#bedpe-format)-like format

1. **chr1**: is the chromosome name for the first interacting HiC bin
2. **start1**: is the starting coordinate for the first interacting HiC bin
3. **end1**: is the ending coordinate for the first interacting HiC bin
4. **chr2**: is the chromosome name for the second interacting HiC bin
5. **start2**: is the starting coordinate for the second interacting HiC bin
6. **end2**: is the ending coordinate for the second interacting HiC bin
7. **HiC count**: number of HiC reads for the interacting HiC bins. SCI does not perform HiC normalization, if user wants to use normalized HiC data, HiC count should corresponds to the normalized HiC read-count. 

SCI provides a script to convert .hic format into SCI accepted format under scripts/hic2sci.sh. 
In order to convert .hic file into please follow the following instructions:

export installed juicer-tools into JUICERTOOLS environment variable 

```sh
$ cd export JUICERTOOLS=/path/to/juicer-tools
```

Then, run hic2sci script to get SCI formatted input data:

```sh
$ scripts/hic2sci.sh <input .hic file> <output file> <resolution> 
```


## Parameters description:


Parameter | Mandatory/Optional | Description
--------------|---------------------------|----------------
-n, --name| yes| Name of the experiment, it will be used as a prefix for all output files
-r, --resolution| yes| Required resolution to predict compartments,provided bins' size should have resolution greater than or equal the provided value
-g, --genome_size| yes|File containing chromosome sizes of the target genome
-o, --order| No. Default: 1| Graph order to consider when performing graph embedding. Available options are 1,2 or both
-s, --samples| No. Default: 25| Number of edges to sample in millions order from the graph
-k, --clusters| No. Default: 2| Nubmer of sub-compartments to be predicted

## Output  

SCI output sub-compartments annotation into BED format with the following fields: 

1. **chr**: chromosome for sub-compartment annotaiton
2. **start**: genomic location where sub-compartment bin starts
3. **end**: genomic location where sub-compartment bin ends
4. **label**: sub-compartment unique label. Bins that do not have sub-compartment label due to low mapability are labeled with NA. 


## Test run
To preform test run for SCI please follow the following steps:
1. Go the Input_sample directory
```sh
$ cd Input_sample
```
Uncompress the sample file:
```sh
$ gunzip SCI_input.txt.gz
```

2. Go back to SCI main directory
```sh
$ cd ..
```

3. run SCI using the following command
```sh
$ python sci.py -n test -f Input_sample/SCI_input.txt -r 100000 -g chromosome_sizes/hg19.chrom.sizes -o both -s 1 -k 5
``` 

[scikit-learn]: http://scikit-learn.org/stable/
[Numpy]: http://www.numpy.org/
[tqdm]: https://pypi.org/project/tqdm/
[GSL]:  http://www.gnu.org/software/gsl/