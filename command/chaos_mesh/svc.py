from command.command_register import command_register


@command_register('svc-http-request-delay')
class SvcHttpRequestDelay:
    pass


@command_register('svc-http-request-abort')
class SvcHttpRequestAbort:
    pass

