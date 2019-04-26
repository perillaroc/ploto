# coding=utf-8
"""
Cat file.

task schema:
    {
        'type': 'cdo_pre_processor',
        'operator': 'operator',
        ...
    }
"""
from ploto.logger import get_logger


def run_pre_processor(task, work_dir, config):
    logger = get_logger()
    cdo_operator = config['operator']
    if cdo_operator == 'select':
        from ploto.pre_processor.cdo_processor.select import run_cdo
        run_cdo(task, work_dir, config)
    else:
        logger.warn('cod operator is not supported: {cdo_operator}'.format(cdo_operator=cdo_operator))