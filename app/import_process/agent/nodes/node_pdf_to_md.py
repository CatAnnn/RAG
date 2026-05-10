import sys
from pathlib import Path

from sqlalchemy.testing.util import function_named

from app.core.logger import logger
from app.import_process.agent.state import ImportGraphState
from app.utils.task_utils import add_running_task, add_done_task
from app.utils.path_util import PROJECT_ROOT


def step_1_validate_paths(state):
    pass


def node_pdf_to_md(state: ImportGraphState) -> ImportGraphState:
    """
    节点: PDF转Markdown (node_pdf_to_md)
    为什么叫这个名字: 核心任务是将 PDF 非结构化数据转换为 Markdown 结构化数据。
    未来要实现:
        1. 进入的日志和任务状态的配置
        2. 进行参数校验 （local_dir -》 给与默认值 | local_file_path完成字面意思的校验 -》 深入校验校验的文件是否真的存在）
        3. 调用minerU进行pdf的解析（local_file_path）返回一个下载文件的地址 xx.zip url地址
        4. 下载zip包，并且解析和提取 （local_dir）
        5. 把md_path地址进行赋值，读取md的文件内容 md_content赋值（文本内容）
        6. 结束的日志和任务状态的配置
        容错率处理！！ try异常处理
    """
    # 1. 进入的日志和任务状态的配置
    function_name = sys._getframe().f_code.co_name
    logger.info(f">>> [{function_name}]开始执行了！现在的状态为：{state}")
    add_running_task(state['task_id'], function_name)
    try:
        # 2. 进行参数校验（local_dir"当前文件地址|输出文件地址"   ->给出默认值|ocal_file_path 完成字面意思的校验->深入校验 校验的文件是否存在）
        # 参数: state local_file_path | local_dir
        # 返回：校验后的文件和输出文件夹Path对象
        pdf_path_obj,local_dir_obj = step_1_validate_paths(state)
        # 3. 调用mineru 进行pdf的解析（local_file_path"原始输入文件地址"）返回一个下载文件的地址 xx.zip url地址
        # 参数：yao
    logger.info(f">>> [Stub] 执行节点: {sys._getframe().f_code.co_name}")
    return state