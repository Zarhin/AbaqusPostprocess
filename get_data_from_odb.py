from odbAccess import openOdb
import numpy as np
import pdb


class Odb_data(object):
    def __init__(self, odb_name):
        """Inintial the odb data
        """
        odb = openOdb(odb_name)
        self.odb = odb
        # steps
        _steps = list(odb.steps.keys())
        print('The steps of odb: {0}...'.format(_steps))
        self.steps = _steps
        # instances
        _instances = odb.rootAssembly.instances
        instances = list(_instances.values())
        _instance_names = [instance.name for instance in instances]
        print('The instance of odb: {0}...'.format(_instance_names))
        self.instances = instances
        self.instances_name = _instance_names
        self._instances = _instances
        # print all sets
        self.show_sets()

    def get_result(self, node_sets=None, ele_sets=None, **kwargs):
        """Extract the node result from odb

        Args:
            node_sets: list, optional
                The list for node set names, if the 'node_set' is None, all the
                node sets in the odb will be used, default is None.
            ele_sets: list, optional
                The list for ele set names, default is None.

            One of the node_sets and ele_sets must be given.

            kwargs: dict, optional
                valid input is :
                    step_name: default is the first step in odb file.
                    instance_name: default is the first instance's name.
                    node_result_type: default is ['U', 'A'].
                    ele_result_type: default is ['S'].
        
        Return:
            None
        """
        odb = self.odb
        # check sets
        if not any([node_sets, ele_sets]):
            raise ValueError(
                'The node_sets and ele_sets are None, please input the '
                'names of node_sets or ele_sets!')
        else:
            if type(node_sets) == type('ss'):
                node_sets = [node_sets]
            if type(ele_sets) == type('ss'):
                ele_sets = [ele_sets]

        # step name
        step_name = kwargs.get('step_name', None)
        if step_name is None:
            step_name = self.steps[0]
        # instance name
        instance_name = kwargs.get('instance_name', None)
        if instance_name is None:
            instance = self.instances[0]
            instance_name = instance.name
        else:
            instance = self._instances[instance_name]

        # result type
        node_result_type = kwargs.get('node_result_type', ['U', 'A'])
        ele_result_type = kwargs.get('ele_result_type', ['S'])
        # get node result to file
        print('Extracting the element result...')
        # result dict
        result_dict = {}
        type2label = {}
        for frame in odb.steps[step_name].frames:
            print('{}  ...'.format(frame.description))
            # for node result
            if node_sets is not None:
                result_dict, type2label = self._get_data_from_frame(
                    frame, instance, node_sets, node_result_type, result_dict,
                    type2label)
            # for element result
            if ele_sets is not None:
                result_dict, type2label = self._get_data_from_frame(
                    frame, instance, ele_sets, ele_result_type, result_dict,
                    type2label, 'element')
        # output data
        # pdb.set_trace()
        for key, value in result_dict.items():
            _label = type2label[key]
            _result_values = [_label] + value
            file_name = key + '.csv'
            np.savetxt(file_name, _result_values, delimiter=',', fmt='%s')
        print('Ending extract data!!!')
        return None

    @staticmethod
    def _get_data_from_frame(frame,
                             instance,
                             sets,
                             result_type,
                             result_dict,
                             type2label,
                             res_type='node'):
        """Get data from frame
        """
        for set_name in sets:
            # get odb set name
            if res_type == 'node':
                _odb_set_name = instance.nodeSets[set_name]
            else:
                _odb_set_name = instance.elementSets[set_name]
            # get data by different result type
            for type_value in result_type:
                result_key = set_name + '_' + type_value
                if result_key in result_dict.keys():
                    _set_result = result_dict[result_key]
                else:
                    _set_result = []
                # get subset from result
                result = frame.fieldOutputs[type_value]
                _result = result.getSubset(region=_odb_set_name)
                _result_value = _result.values
                _result_data = [
                    data for v in _result_value for data in v.data
                ]
                # update result_dict
                _set_result += [_result_data]
                result_dict[result_key] = _set_result
                # labels
                if result_key not in type2label.keys():
                    component_labels = result.componentLabels
                    if res_type == 'node':
                        node_label = []
                        for v in _result_value:
                            for comp in component_labels:
                                node_label += [
                                    '{0}:{1}'.format(v.nodeLabel, comp)
                                ]
                        type2label[result_key] = node_label
                    else:
                        ele_label = []
                        for v in _result_value:
                            for comp in component_labels:
                                ele_label += [
                                    '{0}:{1}'.format(v.elementLabel, comp)
                                ]
                        type2label[result_key] = ele_label
        return result_dict, type2label

    def show_sets(self, instance_name=None):
        """Show all node set name"""
        if instance_name is None:
            instances = self.instances
        else:
            if type(instance_name) == type('ss'):
                instance_name = [instance_name]
            else:
                assert hasattr(instance_name, '__iter__')
            instances = [self.instances[name] for name in instance_name]
        # set names
        # pdb.set_trace()
        all_node_sets = {}
        all_ele_sets = {}
        for instance in instances:
            # node sets
            _node_sets = [name for name in instance.nodeSets.keys()]
            all_node_sets[instance.name] = _node_sets
            print('The node sets of {0} is {1}...'.format(
                instance.name, _node_sets))
            # element sets
            _element_sets = [name for name in instance.elementSets.keys()]
            all_ele_sets[instance.name] = _element_sets
            print('The element sets of {0} is {1}...'.format(
                instance.name, _element_sets))
        self.node_sets = all_node_sets
        self.ele_sets = all_ele_sets
        return None


if __name__ == '__main__':
    odb = Odb_data('part.odb')
    odb.get_result(node_sets=['ALL_NODE', 'X2'],
                   ele_sets=['ALL_ELEMENT', 'LAYER1'])
