from clearml.automation.controller import PipelineDecorator
from clearml import TaskTypes


@PipelineDecorator.component(return_values=["y"], cache=True, task_type=TaskTypes.data_processing)
def step_one(x):
    print("step1 got ")
    print(x)
    print('step_one here!')
    return x*10

@PipelineDecorator.component(return_values=["x"], cache=True, task_type=TaskTypes.data_processing)
def step_zero():
    from random import randint

    print('step_zero here!')
    return randint(0, 100)


@PipelineDecorator.pipeline(name='custom', project='tests', version='0.0.1')
def executing_pipeline():
    x = step_zero()
    y = step_one(x)
    print(y)



if __name__ == '__main__':
    # PipelineDecorator.set_default_execution_queue("defaults")
    PipelineDecorator.run_locally()
    # Start the pipeline execution logic.
    executing_pipeline()

    print('process completed')