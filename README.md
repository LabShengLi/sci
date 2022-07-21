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
$ python setup.py install
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
$ export JUICERTOOLS=/path/to/juicer-tools
```

Then, run hic2sci script to get SCI formatted input data:

```sh
$ scripts/hic2sci.sh <input .hic file> <output file> <resolution> 
```

## Docker Container

Different operating systems my require certain adjustment for the script, thus we build a docker container to solve this problem. The packages are already installed thus we can directly run sci using the following commands. 

The command to start docker container is:

```sh
docker run -it -p 8080:8080 -v <directory of the Rao_2014.hic data file>:/data yuz12012/sci_container:latest
```
For the container, please run
```sh
export LD_LIBRARY_PATH=/sci/gsl/lib
export CPPFLAGS="-I/usr/local/zlib/1.2.8-4/include"
export JUICERTOOLS=/sci/juicer_tools_1.22.01.jar
sh scripts/hic2sci.sh /data/Rao_2014.hic sci_input 100000

bash
conda activate sci
```
For people using singularity to load the docker container, please change the output directory with writable authority.

## Test run
To preform test run for SCI please follow the following steps:
The sample input sample is at: ftp://ftp.jax.org/zhaoyu/demo_data.txt.zip

Please run the following command in sci root directory.

```sh
$ python -m sci.sci -n test -f /sci-data/demo_data.txt -r 100000 -g chromosome_sizes/hg19.chrom.sizes -o both -s 1 -k 5
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


[scikit-learn]: http://scikit-learn.org/stable/
[Numpy]: http://www.numpy.org/
[tqdm]: https://pypi.org/project/tqdm/
[GSL]:  http://www.gnu.org/software/gsl/