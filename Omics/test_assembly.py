import assembly as a


dicoreads=a.readFASTQ('reads.fastq')

total_reads=list(dicoreads.values())
reads=total_reads[0:199]
greedy=a.compute_assembly_greedy(reads)
print(greedy)
scs=a.compute_assembly_scs(reads)
print(scs)
























