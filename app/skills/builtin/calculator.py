import ast,operator as op,re
OPS={ast.Add:op.add,ast.Sub:op.sub,ast.Mult:op.mul,ast.Div:op.truediv,ast.Pow:op.pow,ast.Mod:op.mod,ast.USub:op.neg}
def safe_eval(expression):
    node=ast.parse(expression,mode="eval").body
    def walk(n):
        if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)): return n.value
        if isinstance(n,ast.UnaryOp) and type(n.op) in OPS: return OPS[type(n.op)](walk(n.operand))
        if isinstance(n,ast.BinOp) and type(n.op) in OPS: return OPS[type(n.op)](walk(n.left),walk(n.right))
        raise ValueError("Expressão não permitida")
    return walk(node)
class CalculatorSkill:
    name="calculator"
    description="Realiza cálculos matemáticos simples com segurança."
    def matches(self,text):
        return bool(re.search(r"\b(calcul[ea]|quanto é|quanto da|quanto dá)\b",text.lower()))
    def handle(self,text,db,conversation_id,memories):
        expression=re.sub(r"(?i)^(.*?)(calcul[ea]|quanto é|quanto da|quanto dá)\s*","",text).strip(" ?.")
        if not expression: return "Envie a expressão que deseja calcular."
        try: return "O resultado é %s." % safe_eval(expression)
        except Exception: return "Não consegui calcular essa expressão com segurança."
