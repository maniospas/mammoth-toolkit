from typing import Dict, List
from kfp import compiler, components, dsl

model_onnx = components.load_component_from_file("/var/lib/components_yaml/model_onnx.yaml")
data_csv = components.load_component_from_file("/var/lib/components_yaml/data_csv.yaml")
new_metric = components.load_component_from_file("/var/lib/components_yaml/new_metric.yaml")

@dsl.pipeline(
	name='Hercules'
)
def pipeline(model_onnx__params:Dict, data_csv__params:Dict, new_metric__params:Dict, sensitive_attributes:List):
	model_onnx_task = model_onnx(model_onnx__params=model_onnx__params)
	data_csv_task = data_csv(data_csv__params=data_csv__params)
	new_metric_task = new_metric(new_metric__params=new_metric__params, sensitive_attributes=sensitive_attributes, csv_dataset=data_csv_task.outputs['loaded_dataset'], onnx_model=model_onnx_task.outputs['loaded_model'])


compiler.Compiler().compile(pipeline, "/var/lib/pipelines/pipeline.yaml")