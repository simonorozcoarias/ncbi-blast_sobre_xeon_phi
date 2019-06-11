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
        echo "Usage: ./LongSplitter.sh -f <fasta_file> -n <count_machine> -q <out_file>"
        ;;
    esac
  done

longitud=`grep -v '^>' $FASTA_FILE | wc -c`
longitud=`expr $longitud / $machines`

alg=$(awk -v parte=0 -v long="$longitud" -v file="$query" -v ban=0 -v mac="$machines" '
{if (index($0,">") == 0){
    seqParcial+=length($0)
    if(seqParcial >= long){
      ban=1
    } 
  }else{
    if(ban==1){
      parte+=1
      seqParcial=0
      ban=0
    }
  }
next}
END{
  if(parte==(mac-1)){
   print "true"
  }else{
   print "false"
  }
}' $FASTA_FILE )

echo 'aplica: ' $alg

if [ $alg == 'true' ]; then
echo 'Using the best way...'

awk -v parte=0 -v long="$longitud" -v ban=0 -v file="$query" '
{if (index($0,">") == 0){
    print $0 >> file"."parte
    seqParcial+=length($0)
    if(seqParcial >= long){
      ban=1
    } 
  }else{
    if(ban==1){
      parte+=1
      seqParcial=0
      ban=0
    }
    print $0 >> file"."parte
  }
}' $FASTA_FILE
else
echo 'Using the second way...'
echo 'splitting file in '$machines' parts'
./sizeseq -descending Y -outseq $FASTA_FILE'-sort' $FASTA_FILE

awk -v parte=-1 -v long="$longitud" -v file="$query" -v mac="$machines" '
{if (index($0,">") == 0){
    print $0 >> file"."parte
  }else{
    parte+=1
    if(parte==mac){
      parte=0
    }
    print $0 >> file"."parte
  }
}' $FASTA_FILE'-sort'
rm $FASTA_FILE'-sort'
fi
