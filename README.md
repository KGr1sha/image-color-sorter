# RED SORT 3000
## Lil program that sorts images based on how much red they contain
```
    ____  __________     _____ ____  ____  ______
   / __ \/ ____/ __ \   / ___// __ \/ __ \/_  __/
  / /_/ / __/ / / / /   \__ \/ / / / /_/ / / /   
 / _, _/ /___/ /_/ /   ___/ / /_/ / _, _/ / /    
/_/ |_/_____/_____/   /____/\____/_/ |_| /_/     
                                                 
```
## Installation
### Clone this repo
 ```
 git clone https://github.com/KGr1sha/image-color-sorter.git
 cd image-color-sorter
 ```
### Create python virtual env (or just skip & install all libs globaly)
```
python -m venv venv
```
Activate it
#### Windows
```
venv\scripts\activate
```
#### Unix/MacOS
```
source venv/bin/activate
```

### Install dependencies
```
pip install -r requirements.txt
```
## Usage
As an example you can use this [images](https://drive.google.com/drive/folders/1ILjpEHc2KRVD2a4VQZ3XDQVjrFzkVjbH)

```
python img-red-sort.py -d <directory with images>
```
To see more options use
```
python img-red-sort.py --help
```
