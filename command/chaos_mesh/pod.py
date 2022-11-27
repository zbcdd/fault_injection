from command.command_register import command_register


@command_register('pod-http-request-delay')
class PodHttpRequestDelay:
    pass


@command_register('pod-http-request-abort')
class PodHttpRequestAbort:
    pass