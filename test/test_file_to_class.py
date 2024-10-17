import set_path
set_path.set_path_to_root()

from AudioEffect import EffectObjectMap




if __name__ == "__main__":
    file1 = "overdrive.py"
    file2 = "delay"
    file3 = "test_effect_with_no_py.py"
    file4 = "test_effect_with_no_py"

    file_lst = [file1,file2,file3,file4]
    
    effect_map = EffectObjectMap()

    for file in file_lst:
        print(effect_map.file_name_to_class_name_converter(file))