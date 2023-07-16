We were able to get a torch model, but becasue we were unable to run a VM in VM we weren't able to actually deploy our model to have the Qualcomm device be the main target. 

Below is the code that we made to convert the model to a DLC file, but we were unable to test it. Given a native Ubuntu OS we could test within an hour. 

```import torch

```import torch
import subprocess

# Step 1: Convert PyTorch model to ONNX
# Assuming you have already loaded and trained your PyTorch model
model = MyModel()  # Replace with your own PyTorch model

# Set the model to evaluation mode
model.eval()

# Define a sample input tensor (adjust the shape and data type as per your model's input requirements)
sample_input = torch.randn(1, 3, 128, 128)  # Example input shape for the super-resolution model

# Export the model to ONNX format
onnx_file_path = 'super_resolution.onnx'
torch.onnx.export(model, sample_input, onnx_file_path, export_params=True,
                  opset_version=11, do_constant_folding=True,
                  input_names=['lr'], output_names=['sr'])

# Step 2: Convert ONNX model to DLC using AIMET-MODEL-ZOO
aimet_model_zoo_path = '/path/to/aimet-model-zoo'  # Replace with the actual path to AIMET-MODEL-ZOO

# Change the working directory to the AIMET-MODEL-ZOO directory
import os
os.chdir(aimet_model_zoo_path)

# Modify inference.py to include ONNX export
inference_py_path = os.path.join(aimet_model_zoo_path, 'zoo_torch', 'examples', 'superres', 'utils', 'inference.py')
subprocess.call(['sed', '-i', 's/from aimet_torch.quantsim import QuantizationSimModel/#from aimet_torch.quantsim import QuantizationSimModel/', inference_py_path])
subprocess.call(['sed', '-i', 's/from aimet_torch.qc_quantize_op import QuantScheme/#from aimet_torch.qc_quantize_op import QuantScheme/', inference_py_path])

# Run superres_quanteval.ipynb using jupyter notebook command (assuming you have jupyter notebook installed)
notebook_path = os.path.join(aimet_model_zoo_path, 'zoo_torch', 'examples', 'superres', 'notebooks', 'superres_quanteval.ipynb')
subprocess.call(['jupyter', 'notebook', notebook_path])

# Step 3: Convert the ONNX model to DLC
dlc_output_path = 'super_resolution_sesr_opt.dlc'
subprocess.call(['snpe-onnx-to-dlc', '--input_network', 'super_resolution.onnx', '--output_path', dlc_output_path])

# Step 4: Package the DLC in the desired location
# Move the generated DLC to your desired location, e.g., in the application/src/<package_name>/assets folder
```