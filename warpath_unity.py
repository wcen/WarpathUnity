import json
import logging
import os
import sys
import traceback

import UnityPy


logging.basicConfig(stream=sys.stdout,
                    format='%(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger()


class WarpathUnity:

    def __init__(self, source_path: str, destination_path: str):
        self.destination_path = destination_path

        self.objects = UnityPy.load(source_path).objects
        self.object_index = {'TextAsset': set(),
                             'Texture2D': set(),
                             'Sprite': set(),
                             'MonoBehaviour': set()}
        for idx, obj in enumerate(self.objects):
            if obj.type.name in self.object_index:
                self.object_index[obj.type.name].add(idx)

    def export_texture2d(self):
        return self._export_png('Texture2D')

    def export_sprite(self):
        return self._export_png('Sprite')

    def _export_png(self, obj_type: str):
        assert obj_type in ('Texture2D', 'Sprite')
        dst_folder = os.path.join(self.destination_path, obj_type)
        os.makedirs(dst_folder, exist_ok=True)

        for idx in self.object_index[obj_type]:
            obj = self.objects[idx]
            data = obj.read()

            try:
                filename, file_extension = os.path.splitext(data.name)
                dst_file = os.path.join(dst_folder, f'{filename}.png')
                img = data.image
                img.save(dst_file)
            except Exception as err:
                logger.debug(traceback.format_exc())
                logger.error(f'Failed to handle {obj} in index {idx}, {err}.')

    def export_textasset(self):
        obj_type = 'TextAsset'
        dst_folder = os.path.join(self.destination_path, obj_type)
        os.makedirs(dst_folder, exist_ok=True)

        for idx in self.object_index[obj_type]:
            obj = self.objects[idx]
            data = obj.read()

            try:
                dst_file = os.path.join(dst_folder, data.name)
                with open(dst_file, 'wb') as _file:
                    _file.write(bytes(data.script))
            except Exception as err:
                logger.debug(traceback.format_exc())
                logger.error(f'Failed to handle {obj} in index {idx}, {err}.')

    def export_monobehaviour(self):
        obj_type = 'MonoBehaviour'
        dst_folder = os.path.join(self.destination_path, obj_type)
        os.makedirs(dst_folder, exist_ok=True)

        for idx in self.object_index[obj_type]:
            obj = self.objects[idx]

            try:
                if obj.serialized_type.nodes:
                    tree = obj.read_typetree()
                    dst_file = os.path.join(dst_folder, f'{tree["m_Name"]}.json')
                    with open(dst_file, 'wt', encoding='utf8') as _file:
                        json.dump(tree, _file, ensure_ascii=False, indent=4)
                else:
                    data = obj.read()
                    dst_file = os.path.join(dst_folder, f'{data.name}.bin')
                    with open(dst_file, 'wb') as _file:
                        _file.write(data.raw_data)
            except Exception as err:
                logger.debug(traceback.format_exc())
                logger.error(f'Failed to handle {obj} in index {idx}, {err}.')
                    