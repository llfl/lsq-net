import logging

import torch as t

from .resnet import *
import quan


def create_model(args):
    logger = logging.getLogger()

    model = None
    if args.dataloader.dataset == 'imagenet':
        if args.arch == 'resnet18':
            model = resnet18(pretrained=args.pre_trained)
        elif args.arch == 'resnet34':
            model = resnet34(pretrained=args.pre_trained)
        elif args.arch == 'resnet50':
            model = resnet50(pretrained=args.pre_trained)
        elif args.arch == 'resnet101':
            model = resnet101(pretrained=args.pre_trained)
        elif args.arch == 'resnet152':
            model = resnet152(pretrained=args.pre_trained)
    elif args.dataset.dataset == 'cifar10':
        pass

    if model is None:
        logger.error('Model architecture `%s` for `%s` dataset is not supported' % (args.arch, args.dataloader.dataset))
        exit(-1)

    msg = 'Created `%s` model for `%s` dataset' % (args.arch, args.dataloader.dataset)
    msg += '\n          Use pre-trained model = %s' % args.pre_trained
    logger.info(msg)

    replaced_modules = quan.find_modules_to_quantize(model, args.quan)
    model = quan.replace_module_by_names(model, replaced_modules)
    logger.info('Inserted quantizers into the original model')

    if args.device.gpu and not args.dataloader.serialized:
        model = t.nn.DataParallel(model, device_ids=args.device.gpu)

    return model.to(args.device.type)
