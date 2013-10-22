# -----------------------------------------------------------------------------
# fastfood_yacc_lex.py
# author: zuojiepeng
# date: 2013/10/22
# -----------------------------------------------------------------------------
import ply.lex as lex
import ply.yacc as yacc

# token model description
tokens = (
		'GREATERTHAN',
		'LESSTHAN',
		'NAME',
		'NUMBER',
		'PLUS',
		'MINUS',
		'TIMES',
		'DIVIDE',
		'EQUALS',
		'LPAREN',
		'RPAREN',
	)

# token model symbol 
t_GREATERTHAN  = r'>'
t_LESSTHAN  = r'<'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

# token model action
def t_NUMBER(t):
	r'\d+'
	try:
		t.value = int(t.value)
	except ValueError:
		print "Integer value too large %d", t.value
		t.value = 0
	return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_error(t):
	print "Illegal character %s" % t.value[0]
	t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
#lexer.input("1+3/4")
lexer.input("2<3")
for token in lexer:
	print token

# grammar rule
precedence = (
		('nonassoc', 'GREATERTHAN', 'LESSTHAN'),
		('left', 'PLUS', 'MINUS'),
		('left', 'TIMES', 'DIVIDE'),
		('right', 'UMINUS'),
	)

names = {}

def p_statement_assign(t):
	'statement : NAME EQUALS expression'
	names[t[1]] = t[3]

def p_statement_expr(t):
	'statement : expression'
	print(t[1])

def p_expression_binop(t):
	'''expression : expression GREATERTHAN expression
			| expression LESSTHAN expression
			| expression PLUS expression
			| expression MINUS expression
			| expression TIMES expression
			| expression DIVIDE expression'''
	if t[2] == '>': 
		if t[1] > t[3]: t[0] = True
		else: t[0] = False
	elif t[2] == '<':
		if t[1] > t[3]: t[0] = False 
		else: t[0] = True 
	elif t[2] == '+': t[0] = t[1] + t[3]
	elif t[2] == '-': t[0] = t[1] - t[3]
	elif t[2] == '*': t[0] = t[1] * t[3]
	elif t[2] == '/': t[0] = t[1] / t[3]

def p_expression_uminus(t):
	'expression : MINUS expression %prec UMINUS'
	t[0] = -t[2]

def p_expression_group(t):
	'expression : LPAREN expression RPAREN'
	t[0] = t[2]

def p_expression_number(t):
	'expression : NUMBER'
	t[0] = t[1]

def p_expression_name(t):
	'expression : NAME'
	try:
		t[0] = names[t[1]]
	except LookupError:
		print "Undefined name '%s'" % t[1]
		t[0] = 0

def p_error(t):
	print "Syntax error at '%s'"  % t.value

yacc.yacc()
while True:
	try:
		s = raw_input('-->')
	except EOFError:
		print "Error occured"
		break
	if not s: continue
	yacc.parse(s)
	
