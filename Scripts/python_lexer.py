import ply.lex as lex

key_words = {
	'class':'CLASS',
	'def':'DEF',
	'del':'DEL',
	'if':'IF',
	'else':'ELSE',
	'elif':'ELIF',
	'for':'FOR',
	'in':'IN',
	'while':'WHILE',
	'break':'BREAK',
	'except':'EXCEPT',
	'raise':'RAISE',
	'import':'IMPORT',
	'from':'FROM',
	'as':'AS',
	'with':'WITH',
	'is':'IS',
	'return':'RETURN',
	'continue':'CONTINUE',
	'lambda':'LAMBDA',
	'try':'TRY',
	'and':'AND',
	'or':'OR',
	'not':'NOT',
	'assert':'ASSERT',
	'print':'PRINT',
	'pass':'PASS',
	'global':'GLOBAL',
	'exec':'EXEC',
	'finally':'FINALLY',
	'yield':'YIELD',
	}

class PythonLexer:

	tokens = [
	'LPAREN',
  	'RPAREN',
  	'COMMA',
  	'DOT',
  	'DOTS',
  	'TRIDOTS',
  	'LSQABRACK',
  	'RSQABRACK',
  	'LBRACE',
  	'RBRACE',
  	'SLASH',
  	'BACKSLASH',
  	'PLUS',
  	'ASSIGN',
  	'AUGASSIGN',
  	'EQUAL',
	'MINUS',
	'TIMES',
	'DIVIDE',
	'INTEGER',
	'HEX',
	'OCT',
	'FLOAT',
	'COMPLEX',
	'BINARY',
	'COMMENT',
	'SIGQUOT',
	'DOUBLEQUOT',
	'TRIPLEQUOT',
	'RUBSIGQUOT',
	'RUBDOUBLEQUOT',
	'RUBTRIPLEQUOT',
	'WHITESPACE',
	'NEWLINE',
	'COLON',
	'BASESTRING',
	'LONGSTRING',
	'LESSTHAN',
	'BIGGERTHAN',
	'LESSEQUAL',
	'BIGGEREQUAL',
	'NOTEQUAL',
	'NOTEQUAL2',
	'BITOR',
	'BITAND',
	'BITXOR',
	'LSHIFT',
	'RSHIFT',
	'MOD',
	'COMPLEMENT',
	'POWER',
	'IDENTIFIER',
	'CLASSDEFINE',
	'SEMICO',
	'SKIM',
	'AT',
	'INDENT',
	'DEDENT',
	'EOF',
	'STRMODIF',
	] + list(key_words.values())

	states = (
		('basestring','exclusive'),
		('longstring', 'exclusive'),
		('indent', 'exclusive')
	)



	def __init__(self):
		self.lexer = lex.lex(module=self)
		self.__indent = []
		self.__lcontinue = False
		self.__print_as_function = False
		self.__barrier_scope = { 'in_scope':False,
			'character':None,
			'count':0,
			'barrier_couple':{
				')':'(',
				']':'[',
				'}':'{'}
		}

	def setPrintAsFunction(self):
		print('kkkkkkkkkkkkkk')
		self.__print_as_function = True

	def reset(self):
		self.__print_as_function = False

	def input(self, in_str):
		return self.lexer.input(in_str)

	def token(self):
		tok = None

		try:
			tok = self.lexer.token()
		except lex.LexError:
			tok = lex.LexToken()
			tok.type = 'WHITESPACE'
			tok.value = None
			tok.lineno = self.lexer.lineno
			tok.lexpos = self.lexer.lexpos
			self.lexer.skip(1)
		return tok

	def t_RUBTRIPLEQUOT(self, t):
		r'([bB]?[rR]?|[uU]?[rR]?)(\'{3}|\"{3})'
		t.type = 'TRIPLEQUOT'
		if t.value[-1] == '\'':
			t.value = '\'\'\''
		else:
			t.value = '\"\"\"'
		return self.start_string(t, True)

	def t_RUBDOUBLEQUOT(self, t):
		r'([bB]?[rR]?|[uU]?[rR]?)\"'
		t.type = 'DOUBLEQUOT'
		t.value = '\"'
		return self.start_string(t)
	
	def t_RUBSIGQUOT(self, t):
		r'([bB]?[rR]?|[uU]?[rR]?)\''
		t.type = 'SIGQUOT'
		t.value = '\''
		return self.start_string(t)
	
	def t_OCT(self, t):
		r'0[oO][0-7]+[Ll]?'
		return t
	
	def t_HEX(self, t):
		r'0[xX][0-9a-fA-F]+[Ll]?'
		return t
	
	def t_COMPLEX(self, t):
		r'(\d+([eE][+-]?\d+)?|([0-9]*\.[0-9]+|[0-9]+\.[0-9]*)([eE][+-]?[0-9]+)?)\j'
		t.value = t.value.strip()
		return t

	def t_BINARY(self, t):
		r'0[bB][01]+'
		return t
	
	def t_IDENTIFIER(self, t):
		r'[_a-zA-Z][\d\w]*'
		t.type = key_words.get(t.value,'IDENTIFIER')
		if self.__print_as_function and t.type == 'PRINT':
			t.type = 'IDENTIFIER'
		return t
	
	def start_string(self, t, long_str=False):
		t.lexer.quot_mark = t.value
		t.lexer.start_pos = t.lexer.lexpos
		t.lexer.long_str = long_str
		if not long_str:
			t.lexer.push_state('basestring')
		else:
			t.lexer.push_state('longstring')
		return t
	
	def t_basestring_end(self, t):
		r'[\'\"]'
		if t.value == t.lexer.quot_mark:
			t.value = t.lexer.lexdata[t.lexer.start_pos:t.lexer.lexpos]
			t.type = 'BASESTRING'
			t.lexer.pop_state()
			return t
	
	def t_longstring_end(self, t):
		r'\'{3}|\"{3}'
		if t.value == t.lexer.quot_mark:
			t.value = t.lexer.lexdata[t.lexer.start_pos:t.lexer.lexpos]
			t.type = 'LONGSTRING'
			t.lexer.pop_state()
			return t
	
	def process_string(self, t):
		if t.value[0] == '\\':
			t.lexer.skip(2)
			return
		else:
			t.lexer.skip(1)
		if t.value[0] == '\n' and not t.lexer.long_str:
			raise Exception("Unexpected end of line at %d" % t.lexer.lexpos)
	
	def t_basestring_error(self, t):
		self.process_string(t)
	
	def t_longstring_error(self, t):
		self.process_string(t)
	
	def t_NEWLINE(self, t):
		r'\n'
		if self.__lcontinue:
			self.__lcontinue = False
			return
		if self.__barrier_scope['in_scope']:
			t.type = 'WHITESPACE'
			t.value = None
			return t
		t.lexer.push_state('indent')
		t.type = 'NEWLINE'
		return t
	
	def t_indent_blankline(self, t):
		r'[ \t]*\n'
		t.type = 'WHITESPACE'
		t.value = None
		# DONT pop_state!
		# because of the '\n'
		# we're still in the 'indent' mode
		return t
	
	def t_indent_comment(self, t):
		r'''[ \t]*\#.*\n'''
		pass
	
	def t_indent_end(self, t):
		r'[ \t]+'
	
		strip_str = t.value
		indent_num = len(strip_str)
		if len(self.__indent) > 0:
			if self.__indent[-1] == indent_num:
				# just a newline within the scope
				# return no more NEWLINE token
				t.lexer.pop_state()
				return
			if self.__indent[-1] < indent_num:
				# new scope starts with a bigger indent
				t.type = 'INDENT'
				self.__indent.append(indent_num)
				t.lexer.pop_state()
				return t
			if self.__indent[-1] > indent_num:
				# go through the indent stack, try to find the right indent level
				# if can't, raise a exception
				while len(self.__indent) > 0:
					if self.__indent[-1] == indent_num:
						t.type = 'DEDENT'
						t.lexer.pop_state()
						return t
					else:
						self.__indent.pop(-1)
						if len(self.__indent) == 0:
							raise Exception('IndentationError: unindent does not match any outer indentation level')
						t.type = 'DEDENT'
						t.value = None
						t.lexer.lexpos -= len(strip_str)
						return t
		else:
			# Without any indent yet, mybe a new file, or a fresh top scope
			# Lexer parser cannot realize an 'Unexpected indent' exception
			# hoping yacc part could do that
			self.__indent.append(indent_num)
			t.type = 'INDENT'
			t.lexer.pop_state()
			return t
	
	def t_indent_pass(self, t):
		# A newline without any indent
		r'\S+'
		if len(self.__indent) > 0:
			# Clean all indents
			# Accroding to Python grammar,
			# we should return every 'DEDENT' token
			# of scopes this statement closed
			self.__indent.pop(-1)
			t.lexer.lexpos -= len(t.value)
			t.type = 'DEDENT'
			t.value = None
			return t
		else:
			t.lexer.pop_state()
			# rollback to the beging of this token
			# to prevent swallowing it
			t.lexer.lexpos -= len(t.value)
	
	def t_BACKSLASH(self, t):
		r'\\'
		self.__lcontinue = True
	
	def t_WHITESPACE(self, t):
		r'[ \t]+'
		self.__lcontinue = False
	
	def left_barrier_scope(self, character):
		if self.__barrier_scope['in_scope']:
			if self.__barrier_scope['character'] == character:
				self.__barrier_scope['count'] += 1
			else:
				return
		else:
			self.__barrier_scope['in_scope'] = True
			self.__barrier_scope['character'] = character
			self.__barrier_scope['count'] = 1
	
	def right_barrier_scope(self, character):
		if self.__barrier_scope['in_scope']:
			if self.__barrier_scope['character'] ==\
					self.__barrier_scope['barrier_couple'].get(character):
				self.__barrier_scope['count'] -= 1
				if self.__barrier_scope['count'] == 0:
					self.__barrier_scope['character'] = None
					self.__barrier_scope['in_scope'] = False
		else:
			raise Exception('Unexpected '+ character)
	
	def t_LPAREN(self, t):
		r'\('
		self.left_barrier_scope(t.value)
		return t
	
	def t_RPAREN(self, t):
		r'\)'
		self.right_barrier_scope(t.value)
		return t
	
	def t_LSQABRACK(self, t):
		r'\['
		self.left_barrier_scope(t.value)
		return t
	
	def t_RSQABRACK(self, t):
		r'\]'
		self.right_barrier_scope(t.value)
		return t
	
	def t_LBRACE(self, t):
		r'\{'
		self.left_barrier_scope(t.value)
		return t
	
	def t_RBRACE(self, t):
		r'\}'
		self.right_barrier_scope(t.value)
		return t

	def t_AUGASSIGN(self, t):
		r'\+=|\-=|\*=|\/=|\^=|\&=|\%=|\|=|<<=|>>=|\*\*=|\/\/='
		return t
	
	def t_divide(self, t):
		r'\/\/'
		t.type = 'DIVIDE'
		return t
	
	def t_error(self, t):
		t.type = 'WHITESPACE'
		t.value = None
		return t

	def t_TRIDOTS(self, t):
		r'\.{3}'
		return t

	t_COMMA = r','
	t_DOT = r'\.'
	t_DOTS = r'\.{2,}'
	t_INTEGER = r'\d+([eE][+-]?\d+)?[Ll]?'
	
	t_FLOAT = r'([0-9]*\.[0-9]+|[0-9]+\.[0-9]*)([eE][+-]?[0-9]+)?'
	t_PLUS = r'\+'
	t_MINUS = r'\-'
	t_TIMES = r'\*'
	t_DIVIDE = r'\/'
	t_ignore_COMMENT = r'\#.*'
	t_ASSIGN = r'='
	t_EQUAL = r'=='
	t_COLON = r':'
	t_LESSTHAN = r'<'
	t_BIGGERTHAN = r'>'
	t_LESSEQUAL = r'<='
	t_BIGGEREQUAL = r'>='
	t_NOTEQUAL = r'!='
	t_NOTEQUAL2 = r'<>'
	t_BITOR = r'\|'
	t_BITAND = r'\&'
	t_BITXOR = r'\^'
	t_LSHIFT = r'<<'
	t_RSHIFT = r'>>'
	t_MOD = r'%'
	t_COMPLEMENT = r'~'
	t_POWER = r'\*\*'
	t_SEMICO = r';'
	t_SKIM = r'\`'
	t_AT = r'@'

#lexer = PythonLexer()

def main():
	#lexer = lex.lex()
	#with open('C:\\Python27\\Lib\\sha.py','r') as input_file:
	with open('.\\test.py') as input_file:
		input_text = input_file.read()
		lexer.input(input_text)
		while True:
			tok = lexer.token()
			if not tok: break
			print tok

if __name__ == '__main__':
	exit(main())