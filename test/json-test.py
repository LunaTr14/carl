from json import dump
from os import remove
from os.path import exists, abspath
import sys

parent_dir = abspath('./../')
sys.path.append(parent_dir)
from main import JsonParser

class TestJsonParser(JsonParser):
    __template_json = {"test": {"read": "9649718a1cd61179343786855795b9c75269d97016f752f697e52e7d0d4141fa",
                                "write": ""}}
    __write_answer = "32539bab79202b64f4cfe9dff1288d77f8311ab8934ad9b963679750aca7d238"
    __read_answer = "9649718a1cd61179343786855795b9c75269d97016f752f697e52e7d0d4141fa"

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.__reset_json()

    def __reset_json(self):
        json_file = open(self._file_path, mode="w")
        dump(self.__template_json, json_file)
        json_file.close()

    def __print_err(self, expected : str, result: str) -> None:
        return "\n>>Expected: {sample}\n>>Got: {result}".format(sample=expected, result=result)
    
    def __print_pass(self, test_type : str) -> None:
        return "{test}: ☑".format(test=test_type)

    def test_read(self) -> None:
        result = self.read_content()["test"]["read"]
        assert result == self.__read_answer, self.__print_err(result,self.__read_answer)
        print(self.__print_pass("Json Read"))

    def test_write(self) -> None:
        content = self.read_content()
        content["test"]["write"] = "32539bab79202b64f4cfe9dff1288d77f8311ab8934ad9b963679750aca7d238"
        self.write_content(content)
        result = self.read_content()["test"]["write"]
        assert result == self.__write_answer, self.__print_err(self.__write_answer, result)
        print(self.__print_pass("Json Write"))

    def test_file_existance(self) -> None:
        file_path = "./test.json"
        assert self._does_path_exist(file_path), self.__print_err(file_path + ": Does not exist", "")
        print(self.__print_pass("Json Create"))
    
    def test_json_create(self) -> None:
        file_to_create = "./temp"
        self._file_path = file_to_create
        self._create_json()
        assert exists(self._file_path), self.__print_err("{file}: does not exist".format(file=file_to_create),"")
        self._file_path = "./test.json"
        remove(file_to_create)
        print(self.__print_pass("Json Create"))

if __name__ == "__main__":
    test_object = TestJsonParser("./test.json")
    test_object.test_read()
    test_object.test_write()
    test_object.test_file_existance()
    test_object.test_json_create()
    print("Testing Complete ☑")