#!/bin/bash

# developed by Simon Orozco Arias
# BIOS 2016

while getopts ":f:n:q:h:" optname
  do
    case "$optname" in
      "f")
        FASTA_FILE=$OPTARG
        ;;
      "n")
	machines=$OPTARG
        ;;
      "q")
        query=$OPTARG
        ;;
      "h")
        echo "Usage: SorterSplitter.sh -f <fasta_file> -n <count_machine> -q <out_file>"
        ;;
    esac
  done

longitud=`grep -c '>' $FASTA_FILE`
longitud=`expr $longitud / $machines` 
longitud=`expr $longitud + 1` 

./sizeseq -descending Y -outseq $FASTA_FILE'-sort' $FASTA_FILE
awk -v parte=0 -v long="$longitud" -v ban=0 -v file="$query" '
{if (index($0,">") == 0){
    print $0 >> file"."parte
  }else{
    if(ban==1){
      parte+=1
      count=0
      ban=0
    }
    print $0 >> file"."parte
    count+=1
    if(count >= long){
      ban=1
    }
  }
}' $FASTA_FILE'-sort'

rm $FASTA_FILE'-sort' 

