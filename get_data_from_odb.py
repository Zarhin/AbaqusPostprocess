from odbAccess import openOdb
import numpy as np

class Odb_data(object):
    def __init__(self, odb_name):
        """Inintial the odb data
        """
        odb = openOdb(odb_name)
        instances = odb.rootAssembly.instances
        _instance_names = list(instances.keys())
        print('The instance of odb: {0}...'.format(_instance_names))
        # steps
        _steps = odb.steps.keys()
        print('The steps of odb: {0}...'.format(_steps))
        self.steps = _steps
        self.instances = instances
        self.odb = odb
        self.show_sets()

    def get_node_result(self, node_sets=None, **kwargs):
        """Extract the node result from odb

        Args:
            node_sets: list, optional
                The list for node set names, if the 'node_set' is None, all the
                node sets in the odb will be used, default is None.
            kwargs: dict, optional
                valid input is :
                    step_name: default is 'Step-1'
                    instance_name: default is 'PART-1-1'
                    rusult_type: default is ['U', 'A']
        
        Return:
            None
        """
        odb = self.odb
        # initial parameter
        step_name = kwargs.get('step_name', 'Step-1')
        instance_name = kwargs.get('instance_name', 'PART-1-1')
        result_type = kwargs.get('result_type', ['U', 'A'])
        odb_node_sets = odb.rootAssembly.instances[instance_name].nodeSets
        if node_sets is None:
            node_sets = odb_node_sets.keys()
        # get node result to file
        print('Extracting the element result...')
        # result dict
        result_dict = {}
        type2label = {}
        for frame in odb.steps[step_name].frames:
            print('{}  ...'.format(frame.description))
            for set_name in node_sets:
                for type_value in result_type:
                    result_key = set_name + '_' + type_value
                    if result_key in result_dict.keys():
                        _set_result = result_dict[result_key]
                    else:
                        _set_result = []
                    # get subset from result
                    result = frame.fieldOutputs[type_value]
                    _odb_set_name = odb_node_sets[set_name]
                    _result = result.getSubset(region=_odb_set_name)
                    _result_value = _result.values
                    _node_result = [data for v in _result_value for data in v.data]
                    # update result_dict
                    _set_result += [_node_result]
                    result_dict[result_key] = _set_result
                    # element labels
                    if result_key not in type2label.keys():
                        component_labels = result.componentLabels
                        node_label = []
                        for v in _result_value:
                            for comp in component_labels:
                                node_label += ['{0}:{1}'.format(v.nodeLabel, comp)]
                        type2label[result_key] = node_label
        # output data
        for key, value in result_dict.items():
            node_label = type2label[key]
            _result_values = [node_label] + value
            file_name = key + '.csv'
            np.savetxt(file_name, _result_values, delimiter=',', fmt='%s')
        print('Ending extract data!!!')
        return None
        
    def get_ele_result(self, ele_sets=None, **kwargs):
        """Extract the node result from odb

        Args:
            ele_sets: list, optional
                The list for node set names, if the 'node_set' is None, all the
                node sets in the odb will be used, default is None.
            kwargs: dict, optional
                valid input is :
                    step_name: default is 'Step-1'
                    instance_name: default is 'PART-1-1'
                    rusult_type: default is ['S']
        
        Return:
            None
        """
        odb = self.odb
        # initial parameter
        step_name = kwargs.get('step_name', 'Step-1')
        instance_name = kwargs.get('instance_name', 'PART-1-1')
        result_type = kwargs.get('result_type', ['S', 'E'])
        odb_ele_sets = odb.rootAssembly.instances[instance_name].elementSets
        if ele_sets is None:
            ele_sets = odb_ele_sets.keys()
        # get node result to file
        print('Extracting the element result...')
        # result dict
        result_dict = {}
        type2label = {}
        for frame in odb.steps[step_name].frames:
            print('{}  ...'.format(frame.description))
            for set_name in ele_sets:
                for type_value in result_type:
                    result_key = set_name + '_' + type_value
                    if result_key in result_dict.keys():
                        _set_result = result_dict[result_key]
                    else:
                        _set_result = []
                    # get subset from result
                    result = frame.fieldOutputs[type_value]
                    _odb_set_name = odb_ele_sets[set_name]
                    _result = result.getSubset(region=_odb_set_name)
                    _result_value = _result.values
                    _ele_result = [data for v in _result_value for data in v.data]
                    # update result_dict
                    _set_result += [_ele_result]
                    result_dict[result_key] = _set_result
                    # element labels
                    if result_key not in type2label.keys():
                        component_labels = result.componentLabels
                        ele_label = []
                        for v in _result_value:
                            for comp in component_labels:
                                ele_label += ['{0}:{1}'.format(v.elementLabel, comp)]
                        type2label[result_key] = ele_label
        # output data
        for key, value in result_dict.items():
            ele_label = type2label[key]
            _result_values = [ele_label] + value
            file_name = key + '.csv'
            np.savetxt(file_name, _result_values, delimiter=',', fmt='%s')
        print('Ending extract data!!!')
        return None

    def show_sets(self, instance_name=None):
        """Show all node set name"""
        if instance_name is None:
            instances = [instance for instance in self.instances.values()]
        else:
            if type(instance_name) == type('ss'):
                instance_name = [instance_name]
            else:
                assert hasattr(instance_name, '__iter__')
            instances = [self.instances[name] for name in instance_name]
        # set names
        node_sets = [name for instance in instances for name in instance.nodeSets.keys()]
        ele_sets = [name for instance in instances for name in instance.elementSets.keys()]
        print('The node sets of the instance is {0}'.format(node_sets))
        print('The element sets of the instance is {0}'.format(ele_sets))
        self.node_sets = node_sets
        self.ele_sets = ele_sets
        return None


if __name__ == '__main__':
    # result_type = ['U', 'A']
    # odb = Odb_data('part.odb')
    # odb.get_node_result(result_type=result_type)
    # odb.get_ele_result(result_type=['S'])
    result_type = ['U','V', 'A']
    node_sets = ['PILE_TOP_NODE', 'RECORDER_SLAB_NODE', 'M1_NODE']
    element_sets = ['RECORDER_PILE_ELEMENT', 'RECORDER_LRB_PILE_ELEMENT']
    element_sets += ['RECORDER_SLAB_ELEMENT', 'RECORDER_LRB_SPRING_ELEMENT']
    odb = Odb_data('f:/abaqus/gastank/elastic/model_1_elastic.odb')
    odb.get_node_result(node_sets, result_type=result_type)