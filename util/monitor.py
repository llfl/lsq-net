from torch.utils.tensorboard import SummaryWriter

__all__ = ['ProgressMonitor', 'TensorBoardMonitor', 'AverageMeter']


class AverageMeter:
    """Computes and stores the average and current value"""

    def __init__(self, name, fmt='%.6f'):
        self.name = name
        self.fmt = fmt
        self.val = self.avg = self.sum = self.count = 0

    def reset(self):
        self.val = self.avg = self.sum = self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

    def __str__(self):
        s = self.name + ' '
        s += self.fmt % self.avg
        return s


class Monitor:
    """This is an abstract interface for data loggers

    Train monitors log the progress of the training process to some backend.
    This backend can be a file, a web service, or some other means to collect and/or
    display the training
    """

    def __init__(self):
        pass

    def update(self, epoch, step_idx, step_num, prefix, avg_meters):
        raise NotImplementedError


class ProgressMonitor(Monitor):
    def __init__(self, logger):
        super(ProgressMonitor, self).__init__()
        self.logger = logger

    def update(self, epoch, step_idx, step_num, prefix, avg_meters):
        msg = prefix
        if epoch > -1:
            msg += ' [%d][%5d/%5d]   ' % (epoch, step_idx, int(step_num))
        else:
            msg += ' [%5d/%5d]   ' % (step_idx, int(step_num))
        for m in avg_meters:
            msg += str(m) + '   '
        self.logger.info(msg)


class TensorBoardMonitor(Monitor):
    def __init__(self, logger, log_dir):
        super(TensorBoardMonitor, self).__init__()
        self.writer = SummaryWriter(log_dir / 'tb_runs')
        logger.info('TensorBoard data directory: %s/tb_runs' % log_dir)

    def update(self, epoch, step_idx, step_num, prefix, avg_meters):
        current_step = epoch * step_num + step_idx
        for m in avg_meters:
            self.writer.add_scalar(prefix + '/' + m.name, m.val, current_step)