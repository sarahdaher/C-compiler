class VariableNotFoundException(BaseException):
    def __init__(self, name):
        self.msg = "Variable " + name + " not found"     

class FunctionNotFoundException(BaseException):
    def __init__(self, name):
        self.msg = "Function " + name + " not found"        

class Function:
    def __init__(self, name, arg, body):
        self.name = name
        self.arg = arg
        self.body = body

    def call(self, environment, arg):
        # environment => fonctions et variables globales
        # context => variables locales
        context = { 
            self.arg : arg
        }
        for stmt in self.body:
            a = stmt.call(environment, context)
            if a is not None:
                return a

ACTION_VAR_SET=0
ACTION_CALL=1
ACTION_RETURN=2
ACTION_PRINT=3
ACTION_DEF_VAR=4
ACTION_READ=5

class Statement:
    def __init__(self, action):
        self.action = action
        self.value = None
        self.name = None

    def call(self, environment, context):
        if self.action == ACTION_PRINT:
            print(self.value.calc(environment, context))

        elif self.action == ACTION_RETURN:
            return self.value.calc(environment, context)

        elif self.action == ACTION_DEF_VAR:
            context[self.name] = None

        elif self.action == ACTION_VAR_SET:
            if self.name in context:
                context[self.name] = self.value.calc(environment, context)
            elif self.name in environment["vars"]:
                environment["vars"][self.name] = self.value.calc(environment, context)
            else:
                raise VariableNotFoundException(self.name)

        elif self.action == ACTION_CALL:
            if self.name in environment["functions"]:
                environment["functions"][self.name].call(environment, self.value.calc(environment, context))
            else:
                raise FunctionNotFoundException(self.name)

        elif self.action == ACTION_READ:
            if self.name in context:
                context[self.name] = int(input())
            elif self.name in environment["vars"]:
                environment["vars"][self.name] = int(input())
            else:
                raise VariableNotFoundException(self.name)

EXPR_CST=0
EXPR_VAR_GET=1
EXPR_ADD=2
EXPR_SUB=3
EXPR_MUL=4
EXPR_DIV=5
EXPR_MOD=6
EXPR_CALL=7

class Expr:
    def __init__(self, type):
        self.type = type
        self.name = None
        self.value = None

    def calc(self, environment, context):
        if self.type == EXPR_CST:
            return self.value

        if self.type == EXPR_VAR_GET:
            if self.name in context:
                return context[self.name]
            elif self.name in environment["vars"]:
                return environment["vars"][self.name]
            else:
                raise VariableNotFoundException(self.name)

        if self.type == EXPR_ADD:
            return self.left.calc(environment, context) + self.right.calc(environment, context)

        if self.type == EXPR_MUL:
            return self.left.calc(environment, context) * self.right.calc(environment, context)

        if self.type == EXPR_SUB:
            return self.left.calc(environment, context) - self.right.calc(environment, context)

        if self.type == EXPR_DIV:
            return int(self.left.calc(environment, context) / self.right.calc(environment, context))

        if self.type == EXPR_MOD:
            return self.left.calc(environment, context) % self.right.calc(environment, context)

        if self.type == EXPR_CALL:
            if self.name in environment["functions"]:
                return environment["functions"][self.name].call(environment, self.value.calc(environment, context))
            else:
                raise FunctionNotFoundException(self.name)
