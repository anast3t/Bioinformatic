from clearml.automation.controller import PipelineDecorator
from clearml import TaskTypes


def arr2str(arr):
    return ' '.join(str(x) for x in arr)

def subexec(call):
    from subprocess import Popen, PIPE
    print(f"Calling: {call}")
    # command = shlex.split(call)
    with Popen(call, shell=True, stdout=PIPE) as proc:
        res = proc.stdout.read()
    return res

def strsubexec(call):
    return subexec(call).decode('ascii')

def get_path(name):
    splited = strsubexec(f"whereis -b {name}").split()
    path = [a for a in splited if '/bin/' in a][0]
    print(f'Program path: {path}')
    return path

def cstrsubex(fn, call):
    return strsubexec(f"{get_path(fn)} {call}")

helper =[arr2str, subexec, strsubexec, get_path, cstrsubex]


@PipelineDecorator.component(return_values=["chain"], task_type=TaskTypes.service)
def entrance():
    print("Entering pipeline")
    return 1

@PipelineDecorator.component(parents=["evaluate_flagstat"], return_values=["chain"], task_type=TaskTypes.service)
def fault_exit(reason, chain):
    print(f"Exiting due to {reason}")
    return chain + 1

@PipelineDecorator.component(parents=['entrance'], return_values=["chain"], helper_functions=helper, task_type=TaskTypes.qc)
def qc_report(fastq_paths, out_dir, chain):
    cstrsubex('fastqc', f'{arr2str(fastq_paths)} -o {out_dir}')
    return chain+1

@PipelineDecorator.component(parents=['entrance'], return_values=["chain"], helper_functions=helper, task_type=TaskTypes.data_processing)
def bwa_index(path, chain):
    cstrsubex('bwa', f"index {path}")
    return chain+1

@PipelineDecorator.component(parents=['bwa_index'], return_values=["chain"], helper_functions=helper, task_type=TaskTypes.data_processing)
def bwa_mem(fasta_path, fastq_paths, out_path_name, cores, chain):
    cstrsubex('bwa', f"mem -t {cores} {fasta_path} {arr2str(fastq_paths)} > {out_path_name}")
    return chain+1

@PipelineDecorator.component(parents=['bwa_mem'], return_values=["chain"], helper_functions=helper, task_type=TaskTypes.data_processing)
def samtools_view(sam_path, bam_path, chain):
    cstrsubex('samtools', f'view -b {sam_path} > {bam_path}')
    return chain+1

@PipelineDecorator.component(parents=['samtools_view'], return_values=["chain"], helper_functions=helper, task_type=TaskTypes.qc)
def samtools_flagstat(bam_path, report_path_name, chain):
    cstrsubex('samtools', f'flagstat {bam_path} > {report_path_name}')
    return chain+1

@PipelineDecorator.component(parents=['samtools_flagstat'], return_values=["chain"], helper_functions=helper, task_type=TaskTypes.qc)
def evaluate_flagstat(report_path, chain):
    with open(report_path, 'r') as f:
        lines = f.readlines()
    percent = float(lines[6].split()[4][1:-1]) # maaagic constants)
    if percent > 90:
        print(f"Values are GOOD {percent}%")
        return 1
    else:
        print(f"Values are BAD: {percent}%")
        return 0

@PipelineDecorator.component(parents=['evaluate_flagstat'], return_values=["chain"], helper_functions=helper, task_type=TaskTypes.data_processing)
def samtools_sort(bam_path, sorted_path_name, chain):
    print(cstrsubex('samtools', f'sort -o {sorted_path_name} {bam_path}'))
    return chain+1

@PipelineDecorator.component(parents=['samtools_sort'], return_values=["chain"], helper_functions=helper, task_type=TaskTypes.data_processing)
def freebayes(fasta_path, bam_sorted_path, vcf_path_name, chain):
    print(cstrsubex('freebayes', f'-f {fasta_path} {bam_sorted_path} > {vcf_path_name}'))
    return chain+1

@PipelineDecorator.pipeline(name='biopipeline2', project='bioinformatics', version='0.0.1')
def executing_pipeline(fastq_paths, fasta_path, cores, sam_path_name, bam_path_name, bam_sorted_path_name, flagstat_report_path_name, fastqc_report_path, vcf_path_name):
    chain = entrance()
    chain1 = qc_report(fastq_paths, out_dir=fastqc_report_path, chain=chain)
    chain = bwa_index(fasta_path, chain=chain)
    chain = bwa_mem(fasta_path, fastq_paths, sam_path_name, cores, chain=chain)
    chain = samtools_view(sam_path_name, bam_path_name, chain=chain)
    chain = samtools_flagstat(bam_path_name, flagstat_report_path_name, chain=chain)
    res = evaluate_flagstat(flagstat_report_path_name, chain=chain)
    if res:
        chain = samtools_sort(bam_path_name, bam_sorted_path_name, chain=res)
        chain = freebayes(fasta_path, bam_sorted_path_name, vcf_path_name, chain=chain)
    else:
        chain = fault_exit('bad alignment values', res)


if __name__ == '__main__':
    # PipelineDecorator.set_default_execution_queue("defaults")
    PipelineDecorator.run_locally()
    # Start the pipeline execution logic.
    executing_pipeline(
        fastq_paths=['./biofiles/input_good.fastq'],
        fasta_path='./biofiles/index/input.fna.gz',
        cores=8,
        sam_path_name='./output.sam',
        bam_path_name='./output.bam',
        bam_sorted_path_name='./output.sorted.bam',
        flagstat_report_path_name='./flagstat.txt',
        fastqc_report_path='./biofiles',
        vcf_path_name='./result.vcf'
    )

# ['./biofiles/input.fastq.gz']
# './biofiles/index/input.fna.gz'
# './output.sam'
# './output.bam'
# './output.sorted.bam'
# './flagstat.txt'
# './result.vcf'
