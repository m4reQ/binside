**Binside**

Binside is an AI powered reverse engineering tool that allows recognizing data type from unknown files or memory blocks. It works by creating memory map, using Dynamic Binary Visualization algorithm and using AI model to recognize certain patterns from generated images to determine type of provided data.

For now the only supported file types are:

* Images: JPG and PNG
* Executables: EXE (coming up: x86_64 vs ARM architecture recognition)
* Sounds: MP3
* Text: TXT

This respository contains two separate applications:

* **binside** which is the main application
* **binside_trainer** which is an application designed to help train the AI model

To run any of those navigate to the repository's main directory and use:

On Windows: `py run.py <app_name>`

On Linux: `python3 run.py <app_name>`

where `<app_name>` is either `binside` or `binside_trainer`.
