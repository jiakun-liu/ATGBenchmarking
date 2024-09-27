from core.file_paths import *


class ToolExecutor:
    def __init__(self, apk_path: str, tool_name: str, test_time: str = "60m"):
        # get the absolute path of apk_path
        self.apk_path = os.path.abspath(apk_path)
        self.root_dir = os.path.abspath(root_dir)
        self.tool_name = tool_name
        self.test_time = test_time
        self.apk_name = apk_path.split('/')[-1].strip()
        self.docker_test_time = self.test_time
        self.docker_image = "atg/common"

    def get_result_dir(self):
        return get_result_dir(self.tool_name, self.apk_name)

    def get_log_file(self):
        return get_log_file(self.tool_name, self.apk_name)

    def get_cmd(self):
        result_dir = self.get_result_dir()
        log_file = self.get_log_file()
        # additional_args = "--network none"
        # if self.tool_name == "scenedroid":
        additional_args = ""
        cmd = f'docker run {additional_args} --rm -v {self.root_dir}/:{self.root_dir} -w {self.root_dir}/tools/{self.tool_name} --device=/dev/kvm {self.docker_image} timeout {self.docker_test_time} bash ./run_{self.tool_name}.sh {self.apk_path} {result_dir} {self.test_time} 2>&1 | tee {log_file}'
        return cmd

    def run(self):
        cmd = self.get_cmd()
        print(cmd)
        os.system(cmd)

