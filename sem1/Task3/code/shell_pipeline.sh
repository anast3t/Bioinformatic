#!/bin/bash

fastqc ./biofiles/input_good.fastq -o ./biofiles
bwa index ./biofiles/index/input.fna.gz
bwa mem -t 8 ./biofiles/index/input.fna.gz ./biofiles/input_good.fastq > ./output.sam
samtools view -b ./output.sam > ./output.bam
samtools flagstat ./output.bam > ./flagstat.txt
# most easy way to grab that values
qc=$(python3 flagstat_qc.py flagstat.txt)
echo "ReadQC = $qc"
if [ "$qc" = "GOOD" ]
then
  samtools sort -o ./output.sorted.bam ./output.bam
  freebayes -f ./biofiles/index/input.fna.gz ./output.sorted.bam > ./result.vcf
  echo "Successful finish!"
else
  echo "Exit due to bad read"
fi
