import ply.yacc as yacc
from python_lexer import tokens

def p_stmt(p):
	r'''stmt : lambdef'''
	print('2 succeed!')
	pass

def p_test(p):
	r'''test : or_test
			 | or_test IF or_test ELSE test
			 | lambdef'''
	print('1 succeed!')
	pass

def p_or_test(p):
	r'''or_test : and_test OR and_tests
				| and_test OR and_test
				| and_test'''
	pass

def p_and_tests(p):
	r'''and_tests : and_test OR more_and_tests'''
	pass

def p_more_and_test(p):
	r'''more_and_tests : and_tests
					   | and_test'''
	pass

def p_and_test(p):
	r'''and_test : not_test AND not_tests
				 | not_test AND not_test
				 | not_test'''
	pass

def p_not_tests(p):
	r'''not_tests : not_test AND more_not_tests'''
	pass

def p_more_not_tests(p):
	r'''more_not_tests : not_tests
					   | not_test'''
	pass

def p_not_test(p):
	r'''not_test : NOT not_test
				 | comparison'''
	pass

def p_comparison(p):
	r'''comparison : expr comp_op exprs
				   | expr comp_op expr
				   | expr'''
	pass

def p_exprs(p):
	r'''exprs : expr comp_op more_exprs'''
	pass

def p_more_exprs(p):
	r'''more_exprs : exprs
				   | expr'''
	pass

precedence = (
	('left', 'IS', 'NOT', 'IN'),
)

def p_comp_op(p):
	r'''comp_op : LESSTHAN
				| BIGGERTHAN
				| EQUAL
				| LESSEQUAL
				| BIGGEREQUAL
				| NOTEQUAL
				| NOTEQUAL2
				| IN
				| NOT
				| IS NOT
				| NOT IN
				| IS'''
	pass

def p_expr(p):
	r'''expr : xor_expr BITOR xor_exprs
			 | xor_expr BITOR xor_expr
			 | xor_expr'''
	pass


def p_xor_exprs(p):
	r'''xor_exprs : xor_expr BITOR more_xor_exprs'''
	pass

def p_more_xor_expers(p):
	r'''more_xor_exprs : xor_exprs
					   | xor_expr'''
	pass

def p_xor_expr(p):
	r'''xor_expr : and_expr BITXOR and_exprs
				 | and_expr BITXOR and_expr
				 | and_expr'''
	pass

def p_and_exprs(p):
	r'''and_exprs : and_expr BITXOR more_and_exprs'''
	pass

def p_more_and_exprs(p):
	r'''more_and_exprs : and_exprs
					   | and_expr'''
	pass

def p_and_expr(p):
	r'''and_expr : shift_expr BITAND shift_exprs
				 | shift_expr BITAND shift_expr
				 | shift_expr'''
	pass

def p_shift_exprs(p):
	r'''shift_exprs : shift_expr BITAND more_shift_exprs'''
	pass

def p_more_shift_exprs(p):
	r'''more_shift_exprs : shift_exprs
						 | shift_expr'''
	pass

def p_shift_expr(p):
	r'''shift_expr : arith_expr LSHIFT arith_exprs
				   | arith_expr LSHIFT arith_expr
				   | arith_expr RSHIFT arith_exprs
				   | arith_expr RSHIFT arith_expr
				   | arith_expr'''
	pass

def p_arith_exprs(p):
	r'''arith_exprs : arith_expr LSHIFT more_arith_exprs
					| arith_expr RSHIFT more_arith_exprs'''
	pass

def p_more_arith_exprs(p):
	r'''more_arith_exprs : arith_exprs
						 | arith_expr'''
	pass

def p_arith_expr(p):
	r'''arith_expr : term PLUS terms
				   | term PLUS term
				   | term MINUS terms
				   | term MINUS term
				   | term'''
	pass

def p_terms(p):
	r'''terms : term PLUS more_terms
			  | term MINUS more_terms'''
	pass

def p_more_terms(p):
	r'''more_terms : terms
				   | term'''
	pass

def p_term(p):
	r'''term : factor TIMES factors
			 | factor TIMES factor
			 | factor DIVIDE factors
			 | factor DIVIDE factor
			 | factor MOD factors
			 | factor MOD factor
			 | factor'''
	pass

def p_factors(p):
	r'''factors : factor TIMES more_factors
				| factor DIVIDE more_factors
				| factor MOD more_factors'''
	pass

def p_more_factors(p):
	r'''more_factors : factors
					 | factor'''
	pass

def p_factor(p):
	r'''factor : PLUS factor
			   | MINUS factor
			   | COMPLEMENT factor
			   | power'''
	pass

def p_power(p):
	r'''power : atom
			  | atom POWER factor'''
	pass

def p_atom(p):
	r'''atom : SKIM testlist1 SKIM
			 | LSQABRACK listmaker RSQABRACK
			 | IDENTIFIER
			 | number
			 | strings'''
	pass

def p_number(p):
	r'''number : INTEGER
			   | HEX
			   | OCT
			   | FLOAT
			   | COMPLEX'''
	pass

def p_strings(p):
	r'''strings : SIGQUOT BASESTRING
				| SIGQUOT BASESTRING more_strings
				| DOUBLEQUOT BASESTRING
				| DOUBLEQUOT BASESTRING more_strings
				| TRIPLEQUOT LONGSTRING
				| TRIPLEQUOT LONGSTRING more_strings'''
	pass

def p_more_strings(p):
	r'''more_strings : SIGQUOT BASESTRING
					 | SIGQUOT BASESTRING strings
					 | DOUBLEQUOT BASESTRING
					 | DOUBLEQUOT BASESTRING strings
					 | TRIPLEQUOT LONGSTRING
					 | TRIPLEQUOT LONGSTRING strings'''
	pass

# testlist1: test (',' test)*
def p_testlist1(p):
	r'''testlist1 : test COMMA tests
				  | test COMMA test
				  | test'''
	pass


def p_tests(p):
	r'''tests : test COMMA more_tests'''
	pass

def p_more_tests(p):
	r'''more_tests : tests
				   | test'''
	pass

def p_testlist(p):
	r'''testlist : testlists'''
	pass

def p_testlists(p):
	r'''testlists : test COMMA testlists
				  | test COMMA
				  | test'''
	pass

def p_exprlist(p):
	r'''exprlist : exprlists'''
	pass

def p_exprlists(p):
	r'''exprlists : expr COMMA exprlists
				  | expr COMMA
				  | expr'''
	pass

def p_listmaker(p):
	r'''listmaker : testlist
				  | test list_for'''
	pass

def p_list_iter(p):
	r'''list_iter : list_for
				  | list_if'''
	pass

def p_list_for(p):
	r'''list_for : FOR exprlist IN testlist_safe
				 | FOR exprlist IN testlist_safe list_iter'''
	pass

def p_testlist_safe(p):
	r'''testlist_safe : old_tests'''
	pass

def p_old_tests(p):
	r'''old_tests : more_old_tests'''
	pass

def p_more_old_tests(p):
	r'''more_old_tests : old_test COMMA more_old_tests
					   | old_test COMMA
					   | old_test'''
	pass

def p_list_if(p):
	r'''list_if : IF old_test
				| IF old_test comp_iter'''
	pass

def p_comp_iter(p):
	r'''comp_iter : comp_for
				  | comp_if'''
	pass

def p_comp_for(p):
	r'''comp_for : FOR exprlist IN or_test
				 | FOR exprlist IN or_test comp_iter'''
	pass

def p_comp_if(p):
	r'''comp_if : IF old_test
				| IF old_test comp_iter'''
	pass

def p_old_test(p):
	r'''old_test : or_test
				 | old_lambdef'''
	pass

def p_old_lambdef(p):
	r'''old_lambdef : LAMBDA COLON old_test
					| LAMBDA varargslist COLON old_test'''
	print('Old Lambda reduced')
	pass

def p_labdef(p):
	r'''lambdef : LAMBDA COLON test
				| LAMBDA varargslist COLON test'''
	print('Lambda reduced')
	pass

def p_varargslist(p):
	r'''varargslist : fpdef_args
					| fpdef_args1
					| fpdef_args TIMES IDENTIFIER
					| fpdef_args TIMES IDENTIFIER POWER IDENTIFIER
					| fpdef_args POWER IDENTIFIER'''
	pass

def p_fplist(p):
	r'''fplist : fpdefs'''
	pass

def p_fpdefs(p):
	r'''fpdefs : fpdef COMMA fpdefs
			   | fpdef COMMA
			   | fpdef'''
	pass

def p_fpdef(p):
	r'''fpdef : IDENTIFIER
			  | LPAREN fplist RPAREN'''
	pass

def p_fpdef_args(p):
	r'''fpdef_args : fpdef_arg_list'''
	pass

def p_fpdef_arg_list(p):
	r'''fpdef_arg_list : fpdef_arg COMMA fpdef_arg_list
					   | fpdef_arg COMMA'''
	pass

def p_fpdef_args1(p):
	r'''fpdef_args1 : fpdef_arg_list1'''
	pass

def p_fpdef_arg_list1(p):
	r'''fpdef_arg_list1 : fpdef_arg COMMA fpdef_arg_list1
						| fpdef_arg'''
	pass



def p_fpdef_arg(p):
	r'''fpdef_arg : fpdef
				  | fpdef ASSIGN test'''
	pass


def p_error(p):
	if p is None:
		raise Exception('Error : Unexpected file ending')
	if p.type == 'WHITESPACE':
		yacc.errok()
	else:
		raise Exception('Syntax Error : Unexpected ' + p.type)

def p_empty(p):
    'empty :'
    pass

if __name__ == '__main__':
	yacc.yacc(debug=0)
	parser = yacc.yacc()
	with open('.\\test.py','r') as input_file:
		input_text = input_file.read()
		res = parser.parse(input_text)