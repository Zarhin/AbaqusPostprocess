# AbaqusPostprocess
The scrip of abaqus odb file, it can extract the node and element result from odb file.

Steps to use:
1) Copy the 'get_data_from_odb.py' to the odb file
2) open cmd command or open Abaqus command
3) Change the path to odb file
4) input command: abaqus python
5) >>>from get_data_from_odb import Odb_data
6) >>>odb = Odb_data(odb_name)
7) >>>odb.get_result(node_sets=node_sets, ele_sets=ele_sets)
