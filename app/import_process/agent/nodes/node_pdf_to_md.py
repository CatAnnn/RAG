import sys
from pathlib import Path

from sqlalchemy.testing.util import function_named

from app.core.logger import logger
from app.import_process.agent.state import ImportGraphState
from app.utils.task_utils import add_running_task, add_done_task
from app.utils.path_util import PROJECT_ROOT


def step_1_validate_paths(state):
    pass


def step_2_upload_and_poll(pdf_path_obj):
    pass


def step_3_download_and_extract(zip_url, local_dir_obj, stem):
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
        # 参数：要解析的pdf文件路径    返回值：要下载的zip文件地址
        zip_url = step_2_upload_and_poll(pdf_path_obj)
        # 4.下载zip包，并且解析和提取 （local_dir）
        # 参数：1.要下载的地址 2. local_dir_obj 解压的文件夹  3. 文件名 二狗子 (二狗子.pdf)
        # 返回值：解压后md文件的真实路径
        md_path = step_3_download_and_extract(zip_url, local_dir_obj, pdf_path_obj.stem)
        #  5. 把md_path地址进行赋值，读取md的文件内容 md_content赋值（文本内容）
        #  更新数据
        state['md_path'] = md_path
        state['local_dir'] = local_dir_obj #主要处理下！是str类型
        # md的内容读取，配置给md_content
        with open(md_path, 'r', encoding='utf-8') as f:
            state['md_content'] = f.read()
    except Exception as e:
        # 处理异常
        logger.error(f">>> [{function_name}]使用minerU解析发生了异常，异常信息：{e}")
        raise # 终止工作流
    finally:
        # 6. 结束的日志和任务状态的配置
        logger.info(f">>> [{function_name}]开始结束了！现在的状态为：{state}")
        add_done_task(state['task_id'], function_name)