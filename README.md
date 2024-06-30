# ComfyUI-Photographer-Alpha7-Nodes

## Description
ComfyUI Photographer Alpha7 Nodes is a group of nodes for ComfyUI that provides some really useful tools to users, including:
1. PA7_ComfyViewer, which gives users a very handy second preview window for those with multiple monitors or a large screen.
2. PA7_Negative_Prompt that includes negative prompts ready to be connected to the Clip text encoder (negative).
3. PA7_PromptGenerator coming soon.
![cover](https://github.com/Tcheko243/ComfyUI-Photographer-Alpha7-Nodes/assets/51052375/a4cbbdcd-726b-4a0e-82ca-a79a65a50993)

## Installation

 Placez le dossier `ComfyUI-Photographer-Alpha7-Nodes` dans le dossier `custom_nodes` de ComfyUI.

## Usage

1. Add the `PA7_Comfy_Viewer` node to your ComfyUI pipeline.
2. Connect a generated image as input to this node.
3. When the node is executed, an HTML visualization window will automatically open to display the image and associated metadata. If a `ComfyViewer` window is already open, it will be reused.
4. The visualization window automatically refreshes every second to display the latest image.

## Notes
- The node creates a temporary folder `temp` in the same directory as `PA7_Comfy_Viewer.py` to store the image and metadata.
- Make sure that the file permissions allow for creating and writing in this folder.
- Image batch is not yet supported.
