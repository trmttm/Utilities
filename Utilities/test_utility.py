import unittest


class MyTestCase(unittest.TestCase):

    def test_tree_data(self):
        from Utilities.tree_data import TreeData
        tree_data = TreeData()
        tree_data.add_data('Name00',
                           'Data00')
        self.assertEqual(tree_data.get_name(0),
                         'Name00')
        self.assertEqual(tree_data.get_data(0),
                         'Data00')

        tree_data.add_data('Name01',
                           'Data01')
        tree_data.add_data('Name02',
                           'Data02')
        self.assertEqual(tree_data.get_name(2),
                         'Name02')
        self.assertEqual(tree_data.get_data(2),
                         'Data02')
        self.assertEqual(tree_data.get_name(3), None)
        self.assertEqual(tree_data.get_data(3), None)

        tree_data.remove(1)
        self.assertEqual(tree_data.get_name(2), None)
        self.assertEqual(tree_data.get_data(2), None)
        self.assertEqual(tree_data.get_name(1),
                         'Name02')
        self.assertEqual(tree_data.get_data(1),
                         'Data02')

        print(tree_data.state)

        tree_data.select_data_by_indexes((0, 1))
        self.assertEqual(tree_data.selected_indexes, (0, 1))
        self.assertEqual(tree_data.selected_names, ('Name00',
                                                    'Name02'))
        self.assertEqual(tree_data.selected_datas, ('Data00',
                                                    'Data02'))

        tree_data.unselect_data_by_indexes((0,))
        self.assertEqual(tree_data.selected_indexes, (1,))

    def test_tree_data_sorting(self):
        from Utilities.tree_data import TreeData
        tree_data = TreeData()
        for n in range(20):
            tree_data.add_data(f'Name{n}', f'Data{n}')
        tree_data.select_data_by_indexes((3, 4))
        tree_data.sort_data(-1)
        self.assertEqual(tree_data.selected_indexes, (2, 3))
        expected_state = {
            'names': [
                'Name0',
                'Name1',
                'Name3',
                'Name4',
                'Name2',
                'Name5',
                'Name6',
                'Name7',
                'Name8',
                'Name9',
                'Name10',
                'Name11',
                'Name12',
                'Name13',
                'Name14',
                'Name15',
                'Name16',
                'Name17',
                'Name18',
                'Name19'],
            'data': [
                'Data0',
                'Data1',
                'Data3',
                'Data4',
                'Data2',
                'Data5',
                'Data6',
                'Data7',
                'Data8',
                'Data9',
                'Data10',
                'Data11',
                'Data12',
                'Data13',
                'Data14',
                'Data15',
                'Data16',
                'Data17',
                'Data18',
                'Data19'],
            'selected': (2, 3)}
        self.assertEqual(tree_data.state, expected_state)
        tree_data.sort_data(-2)
        expected_state = {
            'names': [
                'Name3',
                'Name4',
                'Name0',
                'Name1',
                'Name2',
                'Name5',
                'Name6',
                'Name7',
                'Name8',
                'Name9',
                'Name10',
                'Name11',
                'Name12',
                'Name13',
                'Name14',
                'Name15',
                'Name16',
                'Name17',
                'Name18',
                'Name19'],
            'data': [
                'Data3',
                'Data4',
                'Data0',
                'Data1',
                'Data2',
                'Data5',
                'Data6',
                'Data7',
                'Data8',
                'Data9',
                'Data10',
                'Data11',
                'Data12',
                'Data13',
                'Data14',
                'Data15',
                'Data16',
                'Data17',
                'Data18',
                'Data19'],
            'selected': (0, 1)}
        self.assertEqual(tree_data.state, expected_state)
        tree_data.sort_data(-1)

        tree_data.select_data_by_indexes((19,))
        self.assertEqual(tree_data.selected_indexes, (19,))
        tree_data.sort_data(1)
        expected_state = {
            'names': [
                'Name3',
                'Name4',
                'Name0',
                'Name1',
                'Name2',
                'Name5',
                'Name6',
                'Name7',
                'Name8',
                'Name9',
                'Name10',
                'Name11',
                'Name12',
                'Name13',
                'Name14',
                'Name15',
                'Name16',
                'Name17',
                'Name18',
                'Name19'],
            'data': [
                'Data3',
                'Data4',
                'Data0',
                'Data1',
                'Data2',
                'Data5',
                'Data6',
                'Data7',
                'Data8',
                'Data9',
                'Data10',
                'Data11',
                'Data12',
                'Data13',
                'Data14',
                'Data15',
                'Data16',
                'Data17',
                'Data18',
                'Data19'],
            'selected': (19,)}
        self.assertEqual(tree_data.state, expected_state)

        tree_data.select_data_by_indexes((17, 19))
        tree_data.sort_data(1)
        expected_state = {
            'names': [
                'Name3',
                'Name4',
                'Name0',
                'Name1',
                'Name2',
                'Name5',
                'Name6',
                'Name7',
                'Name8',
                'Name9',
                'Name10',
                'Name11',
                'Name12',
                'Name13',
                'Name14',
                'Name15',
                'Name16',
                'Name17',
                'Name18',
                'Name19'],
            'data': [
                'Data3',
                'Data4',
                'Data0',
                'Data1',
                'Data2',
                'Data5',
                'Data6',
                'Data7',
                'Data8',
                'Data9',
                'Data10',
                'Data11',
                'Data12',
                'Data13',
                'Data14',
                'Data15',
                'Data16',
                'Data17',
                'Data18',
                'Data19'],
            'selected': (17, 19,)}
        self.assertEqual(tree_data.state, expected_state)

        tree_data.add_data('Name20', 'Data20')
        self.assertEqual(tree_data.selected_indexes, (17, 19,))

        tree_data.select_data_by_indexes((2, 17, 19))
        tree_data.remove(3)
        self.assertEqual(tree_data.selected_indexes, (2, 16, 18,))
