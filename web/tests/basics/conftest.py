    
#===========================================================================
#command line parsers for py.test.
#===========================================================================

def pytest_addoption(parser):
    parser.addoption("--env", action="store",help="env: the env that runs the tests e.g. qa , dev")

def pytest_funcarg__env(request):
    return request.config.option.env