from sys import argv

import owlready2 as owl

def build_stub_ontology(prefix='own.tology'):
    onto = owl.get_ontology(prefix)

    with onto:
        class Language(owl.Thing):
            pass

        class Implementation(owl.Thing):
            pass

        class implements(Implementation >> Language):
            pass

    python = Language('Python')
    cpython = Implementation('CPython')
    cpython.implements = [python]

    return onto

if __name__ == '__main__':
    try:
        path = argv[1]
    except IndexError:
        print('Usage: goodl <ontology file>\n'
              '       goodl --stub')
        exit(1)

    print('[INFO] Welcome to the new ontology analyser!')
    if path == '--stub':
        print(f'[INFO] Building stub ontology...', end='')
        onto = build_stub_ontology()
    else:
        print(f'[INFO] Analysing "{path}"...', end='')
        owl.onto_path.append(path)
        onto = owl.get_ontology(path).load()
    print('Done')

    classes = [*onto.classes()]
    print(f'\n[INFO] This funny ontology has {len(classes)} classes! Look:')
    for _class in classes:
        print(f'       Class {_class}:\n'
              f'           Ancestors: {_class.ancestors()}\n'
              f'           Instances: {_class.instances()}')

    obj_props = [*onto.object_properties()]
    if obj_props:
        print(f'\n[INFO] It also has some object properties:')
        for prop in obj_props:
            print(f'       ObjProperty {prop} is a thing')
    else:
        print('\n[WARN] Oh, sorry, no object properties found!')

    print('\n[INFO] Now, trying to see that'
          ' CPython is an implementation of Python (somehow)...')
    cpython = onto['CPython']
    print(f'{cpython} implements {cpython.implements}')
