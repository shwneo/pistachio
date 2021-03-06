import ply.yacc as yacc
import ply.lex as lex

from c_lexer import CLexer

c_lexer = CLexer()
tokens = c_lexer.tokens

start = 'translation_unit'
curr_string = ''
latest_decleared_name = ''
parameter_reducer_lock = False
latest_type_name = ''
initializer_level = 0
initializer_field = [0]
initializer_value = None
initializer_found = False
function_arg_list = []

initialized_objects_output = {}
curr_object = ''

def p_primary_expression(p):
	'''primary_expression : IDENTIFIER see_value
						  | CONSTANT see_value
						  | string see_string
						  | '(' expression ')' '''
	print('primary_expression reduced')
	pass

def p_see_value(p):
	'''see_value : '''
	global initializer_value
	initializer_value = p[-1]
	pass

def p_see_string(p):
	'''see_string : '''
	global initializer_value
	global curr_string
	initializer_value = curr_string
	curr_string = ''
	pass

def p_string(p):
	'''string : nature_strings'''
	pass

def p_nature_strings(p):
	'''nature_strings : STRING_LITERAL see_one_string nature_strings
					  | empty'''
	pass

def p_see_one_string(p):
	'''see_one_string : '''
	global curr_string
	curr_string = curr_string + p[-1].strip('"')
	pass

def p_postfix_expression(p):
	'''postfix_expression : postfix_expressions
						  | primary_expression postfix_expressions'''
	print('postfix_expression reduced')
	pass

def p_postfix_expressions(p):
	'''postfix_expressions : LSQABRACK expression RSQABRACK postfix_expressions
						   | '(' see_function_call ')' postfix_expressions
						   | '(' see_function_call collect_arg_begin argument_expression_list collect_arg_end ')' postfix_expressions
						   | '.' IDENTIFIER postfix_expressions
						   | PTR_OP IDENTIFIER postfix_expressions
						   | INC_OP postfix_expressions
						   | DEC_OP postfix_expressions
						   | empty'''
	pass

def p_collect_arg_begin(p):
	'''collect_arg_begin : '''
	pass

def p_collect_arg_end(p):
	'''collect_arg_end : '''
	global function_arg_list
	print(" with arg list = ", function_arg_list)
	function_arg_list[:] = []
	pass

def p_see_function_call(p):
	'''see_function_call : '''
	global initializer_value
	print(" --- Function %s called" % (initializer_value))
	pass

def p_argument_expression_list(p):
	'''argument_expression_list : assignment_expression push_arg argument_expression_lists'''
	pass

def p_argument_expression_lists(p):
	'''argument_expression_lists : ','  assignment_expression push_arg argument_expression_lists
								 | empty'''
	pass

def p_push_arg(p):
	'''push_arg : '''
	global function_arg_list
	global initializer_value
	function_arg_list.append(initializer_value)
	pass

def p_unary_expression(p):
	'''unary_expression : postfix_expression
						| INC_OP unary_expression
						| DEC_OP unary_expression
						| unary_operator cast_expression
						| SIZEOF unary_expression
						| SIZEOF '(' type_name ')' '''
	pass

def p_unary_operator(p):
	'''unary_operator : '&'
					  | '*'
					  | '+'
					  | '-'
					  | '~'
					  | '!' '''
	pass

def p_cast_expression(p):
	'''cast_expression : unary_expression
					   | '(' type_name ')'  cast_expression'''
	pass

def p_multiplicative_expression(p):
	'''multiplicative_expression : cast_expression multiplicative_expressions'''
	pass

def p_multiplicative_expressions(p):
	'''multiplicative_expressions : '*' cast_expression multiplicative_expressions
								  | '/' cast_expression multiplicative_expressions
								  | '%' cast_expression multiplicative_expressions
								  | empty'''
	pass

def p_additive_expression(p):
	'''additive_expression : multiplicative_expression additive_expressions'''
	pass

def p_additive_expressions(p):
	'''additive_expressions : '+' multiplicative_expression additive_expressions
							| '-' multiplicative_expression additive_expressions
							| empty'''
	pass

def p_shift_expression(p):
	'''shift_expression : additive_expression shift_expressions'''
	pass

def p_shift_expressions(p):
	'''shift_expressions : LEFT_OP additive_expression shift_expressions
						 | RIGHT_OP additive_expression shift_expressions
						 | empty'''
	pass

def p_relational_expression(p):
	'''relational_expression : shift_expression relational_expressions'''
	pass

def p_relational_expressions(p):
	'''relational_expressions : '<' shift_expression relational_expressions
							  | '>' shift_expression relational_expressions
							  | LE_OP shift_expression relational_expressions
							  | GE_OP shift_expression relational_expressions
							  | empty'''
	pass

def p_equality_expression(p):
	'''equality_expression : relational_expression equality_expressions'''
	pass

def p_equality_expressions(p):
	'''equality_expressions : EQ_OP relational_expression equality_expressions
							| NE_OP relational_expression equality_expressions
							| empty'''
	pass

def p_and_expression(p):
	'''and_expression : equality_expression and_expressions'''
	pass

def p_and_expressions(p):
	'''and_expressions : '&' equality_expression and_expressions
					   | empty'''
	pass

def p_exclusive_or_expression(p):
	'''exclusive_or_expression : and_expression exclusive_or_expressions'''
	pass

def p_exclusive_or_expressions(p):
	'''exclusive_or_expressions : '^' and_expression exclusive_or_expressions
								| empty'''
	pass

def p_inclusive_or_expression(p):
	'''inclusive_or_expression : exclusive_or_expression inclusive_or_expressions'''
	pass

def p_inclusive_or_expressions(p):
	'''inclusive_or_expressions : '|' exclusive_or_expression inclusive_or_expressions
								| empty'''
	pass

def p_logical_and_expression(p):
	'''logical_and_expression : inclusive_or_expression logical_and_expressions'''
	pass

def p_logical_and_expressions(p):
	'''logical_and_expressions : AND_OP inclusive_or_expression logical_and_expressions
							   | empty'''
	pass

def p_logical_or_expression(p):
	'''logical_or_expression : logical_and_expression logical_or_expressions'''
	pass

def p_logical_or_expressions(p):
	'''logical_or_expressions : OR_OP logical_and_expression logical_or_expressions
							  | empty'''
	pass

def p_conditional_expression(p):
	'''conditional_expression : logical_or_expression
							  | logical_or_expression '?' expression ':' conditional_expression '''
	pass

def p_assignment_expression(p):
	'''assignment_expression : conditional_expression
							 | unary_expression assignment_operator assignment_expression'''
	pass

def p_assignment_operator(p):
	'''assignment_operator : '='
						   | MUL_ASSIGN
						   | DIV_ASSIGN
						   | MOD_ASSIGN
						   | AND_ASSIGN
						   | XOR_ASSIGN
						   | OR_ASSIGN
						   | RIGHT_ASSIGN
						   | LEFT_ASSIGN
						   | ADD_ASSIGN
						   | SUB_ASSIGN '''
	pass

def p_expression(p):
	'''expression : assignment_expression expressions'''
	pass

def p_expressions(p):
	'''expressions : ',' assignment_expression expressions
				   | empty'''
	pass

def p_constant_expression(p):
	'''constant_expression : conditional_expression'''
	pass

def p_declaration(p):
	'''declaration : declaration_specifiers ';'
				   | declaration_specifiers init_declarator_list ';'
				   | TYPEDEF declaration_specifiers declarator type_decleared ';'
				   | TYPEDEF declaration_specifiers declaration_specifiers ';'
				   | TYPEDEF declaration_specifiers ';' '''
	print('declaration reduced')
	pass

def p_type_decleared(p):
	'''type_decleared : '''
	global latest_decleared_name
	p.lexer.add_type_name(latest_decleared_name)
	print(' *** New type name ' + latest_decleared_name + " added")
	pass

def p_declaration_specifiers(p):
	'''declaration_specifiers : storage_class_specifier
							  | storage_class_specifier declaration_specifiers
							  | type_specifier
							  | type_specifier declaration_specifiers
							  | type_qualifier
							  | type_qualifier declaration_specifiers'''
	print('declaration_specifiers reduced')
	pass

def p_init_declarator_list(p):
	'''init_declarator_list : init_declarator init_declarator_lists'''
	pass

def p_init_declarator_lists(p):
	'''init_declarator_lists : ',' init_declarator init_declarator_lists
							 | empty '''
	pass

def p_init_declarator(p):
	'''init_declarator : declarator
					   | declarator '=' see_pass initializer'''
	print('init_declarator reduced')
	pass

def p_see_pass(p):
	'''see_pass : '''
	global latest_type_name
	global latest_decleared_name
	global initialized_objects_output
	global curr_object
	print(' --- An assigned instance of %s named %s declared!' % (latest_type_name, latest_decleared_name))
	curr_object = latest_decleared_name
	initialized_objects_output[latest_decleared_name] = []
	initialized_objects_output[latest_decleared_name].append(latest_type_name)
	pass

def p_storage_class_specifier(p):
	'''storage_class_specifier : EXTERN
							   | STATIC
							   | AUTO
							   | REGISTER'''
	pass

def p_extension_specifiers(p):
	'''extension_specifiers : ATTRIBUTE '(' initializer ')'
							| INLINE
							| RESTRICT '''
	print('extension_specifiers reduced')
	pass

def p_type_specifier(p):
	'''type_specifier : VOID see_type_name
					  | CHAR see_type_name
					  | SHORT see_type_name
					  | INT see_type_name
					  | LONG see_type_name
					  | FLOAT see_type_name
					  | DOUBLE see_type_name
					  | SIGNED see_type_name
					  | UNSIGNED see_type_name
					  | struct_or_union_specifier
					  | enum_specifier
					  | TYPE_NAME see_type_name '''
	print('type_specifier reduced')
	pass

def p_struct_or_union_specifier(p):
	'''struct_or_union_specifier : struct_or_union IDENTIFIER see_type_name  LBRACE struct_declaration_list RBRACE
								 | struct_or_union LBRACE struct_declaration_list RBRACE
								 | struct_or_union IDENTIFIER see_type_name
								 | struct_or_union TYPE_NAME see_type_name '''
	print('struct_or_union_specifier reduced')
	pass

def p_see_type_name(p):
	'''see_type_name : '''
	global latest_type_name
	latest_type_name = p[-1]
	pass


def p_struct_or_union(p):
	'''struct_or_union : STRUCT
					   | UNION'''
	pass

def p_struct_declaration_list(p):
	'''struct_declaration_list : struct_declaration_lists'''
	pass

def p_struct_declaration_lists(p):
	'''struct_declaration_lists : struct_declaration struct_declaration_lists
								| struct_declaration'''
	pass

def p_struct_declaration(p):
	'''struct_declaration : specifier_qualifier_list struct_declarator_list ';' '''
	pass

def p_specifier_qualifier_list(p):
	'''specifier_qualifier_list : type_specifier specifier_qualifier_list
								| type_specifier
								| type_qualifier specifier_qualifier_list
								| type_qualifier'''
	print('specifier_qualifier_list reduced')
	pass

def p_struct_declarator_list(p):
	'''struct_declarator_list : struct_declarator struct_declarator_lists'''
	pass

def p_struct_declarator_lists(p):
	'''struct_declarator_lists : ',' struct_declarator struct_declarator_lists
							   | empty'''
	pass

def p_struct_declarator(p):
	'''struct_declarator : declarator
						 | ':' constant_expression
						 | declarator ':' constant_expression'''
	pass

def p_enum_specifier(p):
	'''enum_specifier : ENUM LBRACE enumerator_list RBRACE
					  | ENUM IDENTIFIER see_type_name LBRACE enumerator_list RBRACE
					  | ENUM IDENTIFIER see_type_name'''
	print('enum_specifier reduced')
	pass

def p_enumerator_list(p):
	'''enumerator_list : enumerator enumerator_lists'''
	pass

def p_enumerator_lists(p):
	'''enumerator_lists : ',' enumerator
						| empty'''
	pass

def p_enumerator(p):
	'''enumerator : IDENTIFIER
				  | IDENTIFIER '=' constant_expression'''
	print('enumerator reduced')
	pass

def p_type_qualifier(p):
	'''type_qualifier : CONST
					  | VOLATILE
					  | extension_specifiers'''
	print('type_qualifier reduced')
	pass

def p_declarator(p):
	'''declarator : pointer direct_declarator extension_specifiers
				  | direct_declarator extension_specifiers
				  | pointer direct_declarator
				  | direct_declarator'''
	print('declarator reduced')
	pass

def p_direct_declarator(p):
	'''direct_declarator : IDENTIFIER see_declared_name direct_declarators
						 | TYPE_NAME see_declared_name direct_declarators
						 | '(' declarator ')' direct_declarators end_param_reducer'''
	print('direct_declarator reduced')
	pass

def p_see_declared_name(p):
	'''see_declared_name : '''
	global latest_decleared_name
	global parameter_reducer_lock
	if not parameter_reducer_lock:
		print('NAME OF %s DECLARED' % p[-1])
		latest_decleared_name = p[-1]
	pass

def p_direct_declarators(p):
	'''direct_declarators : LSQABRACK begin_param_reducer constant_expression end_param_reducer RSQABRACK direct_declarators
						  | LSQABRACK RSQABRACK direct_declarators
						  | '(' begin_param_reducer parameter_type_list end_param_reducer ')' direct_declarators
						  | '(' begin_param_reducer identifier_list end_param_reducer ')' direct_declarators
						  | '(' ')' direct_declarators
						  | empty'''
	print('direct_declarators reduced')
	pass

def p_begin_param_reducer(p):
	'''begin_param_reducer : '''
	global parameter_reducer_lock
	parameter_reducer_lock = True

def p_end_param_reducer(p):
	'''end_param_reducer : '''
	global parameter_reducer_lock
	parameter_reducer_lock = False

def p_pointer(p):
	'''pointer : '*'
			   | '*' type_qualifier_list
			   | '*' pointer
			   | '*' type_qualifier_list pointer '''
	pass

def p_type_qualifier_list(p):
	'''type_qualifier_list : type_qualifier_lists'''
	pass

def p_type_qualifier_lists(p):
	'''type_qualifier_lists : type_qualifier type_qualifier_lists
							| type_qualifier'''
	pass

def p_parameter_type_list(p):
	'''parameter_type_list : parameter_list'''
	pass

def p_parameter_list(p):
	'''parameter_list : parameter_declaration parameter_lists
					  | parameter_declaration'''
	pass

def p_parameter_lists(p):
	'''parameter_lists : ',' parameter_declaration parameter_lists
					   | ',' ELLIPSIS
					   | empty'''
	print('parameter_lists reduced')
	pass

def p_parameter_declaration(p):
	'''parameter_declaration : declaration_specifiers declarator
							 | declaration_specifiers abstract_declarator
							 | declaration_specifiers'''
	print('parameter_declaration reduced')
	pass

def p_identifier_list(p):
	'''identifier_list : IDENTIFIER identifier_lists'''
	print('identifier_list reduced')
	pass

def p_identifier_lists(p):
	'''identifier_lists : ',' IDENTIFIER identifier_lists
						| empty'''
	pass

def p_type_name(p):
	'''type_name : specifier_qualifier_list
				 | specifier_qualifier_list abstract_declarator'''
	pass

def p_abstract_declarator(p):
	'''abstract_declarator : pointer
						   | direct_abstract_declarator
						   | pointer direct_abstract_declarator'''
	pass

def p_direct_abstract_declarator(p):
	'''direct_abstract_declarator : '(' abstract_declarator ')' direct_abstract_declarators
								  | direct_abstract_declarators'''
	pass

def p_direct_abstract_declarators(p):
	'''direct_abstract_declarators : LSQABRACK RSQABRACK direct_abstract_declarators
								   | LSQABRACK constant_expression RSQABRACK direct_abstract_declarators
								   | '(' ')' direct_abstract_declarators
								   | '(' parameter_type_list ')' direct_abstract_declarators
								   | empty'''
	pass

def p_initializer(p):
	'''initializer : assignment_expression see_initializer
				   | LBRACE initializer_level_in initializer_list initializer_level_out RBRACE '''
	print('initializer reduced')
	pass

def p_initializer_list(p):
	'''initializer_list : initializer initializer_field_1st initializers'''
	pass

def p_initializers(p):
	'''initializers : ',' initializer initializer_field_more initializers
					| ','
					| empty '''
	pass

def p_initializer_field_1st(p):
	'''initializer_field_1st : '''
	global initializer_field
	global initializer_level
	global initializer_value
	initializer_field[-1] = 1
	print(' --- Find %d field %s @ level %d' % (initializer_field[-1], initializer_value, initializer_level))
	pass

def p_initializer_field_more(p):
	'''initializer_field_more : '''
	global initializer_field
	global initializer_level
	global initializer_value
	global initializer_found
	if initializer_found:
		initializer_field[-1] += 1
		print(' --- Find %d field %s @ level %d' % (initializer_field[-1], initializer_value, initializer_level))
		initializer_found = False
	pass

def p_initializer_level_in(p):
	'''initializer_level_in : '''
	global initializer_level
	global initializer_field
	initializer_field[-1] += 1
	print(" --- Entring struct initializer as %d field @ level %d" % (initializer_field[-1], initializer_level))
	initializer_field.append(1)
	initializer_level += 1
	pass

def p_initializer_level_out(p):
	'''initializer_level_out : '''
	global initializer_level
	global initializer_field
	initializer_field.pop()
	initializer_level -= 1
	pass

def p_see_initializer(p):
	'''see_initializer : '''
	global initializer_found
	initializer_found = True
	print('see_initializer')
	pass

def p_statement(p):
	'''statement : labeled_statement
				 | compound_statement
				 | expression_statement
				 | selection_statement
				 | iteration_statement
				 | jump_statement'''
	pass

def p_labeled_statement(p):
	'''labeled_statement : IDENTIFIER ':' statement
						 | CASE constant_expression ':' statement
						 | DEFAULT ':' statement'''
	print('labeled_statement reduced')
	pass

def p_compound_statement(p):
	'''compound_statement : LBRACE RBRACE
						   | LBRACE statement_list RBRACE
						   | LBRACE declaration_list RBRACE
						   | LBRACE declaration_list statement_list RBRACE '''
	pass

def p_declaration_list(p):
	'''declaration_list : declaration_lists'''
	pass

def p_declaration_lists(p):
	'''declaration_lists : declaration declaration_lists
						 | declaration'''
	pass

def p_statement_list(p):
	'''statement_list : statement_lists'''
	pass

def p_statement_lists(p):
	'''statement_lists : statement statement_lists
					   | statement'''
	pass

def p_expression_statement(p):
	'''expression_statement : ';'
							| expression ';' '''
	print('expression_statement reduced')
	pass

def p_selection_statement(p):
	'''selection_statement : IF '(' expression ')' statement
						   | IF '(' expression ')' statement ELSE statement
						   | SWITCH '(' expression ')' statement'''
	pass

def p_iteration_statement(p):
	'''iteration_statement : WHILE '(' expression ')' statement
						   | DO statement WHILE '(' expression ')' ';'
						   | FOR '(' expression_statement expression_statement ')' statement
						   | FOR '(' expression_statement expression_statement expression ')' statement '''
	pass

def p_jump_statement(p):
	'''jump_statement : GOTO IDENTIFIER
					  | CONTINUE
					  | BREAK ';'
					  | RETURN ';'
					  | RETURN expression ';' '''
	pass

def p_translation_unit(p):
	'''translation_unit : translation_units'''
	pass

def p_translation_units(p):
	'''translation_units : external_declaration translation_units
						 | external_declaration'''
	print('translation units reduced!')
	pass

def p_external_declaration(p):
	'''external_declaration : function_definition
							| declaration'''
	print('external_declaration reduced')
	pass

def p_function_definition(p):
	'''function_definition : declaration_specifiers declarator declaration_list compound_statement
						   | declaration_specifiers declarator compound_statement
						   | declarator declaration_list compound_statement
						   | declarator compound_statement'''
	print('function_definition reduced')
	pass

def p_error(p):
	if p is None:
		# raise Exception('Error : Unexpected file ending')
		tok = lex.LexToken()
		tok.type = 'NEWLINE'
		tok.value = None
		return tok
	if p.type == 'IDENTIFIER':
		# unexpected identifier, may be it's a type name
		p.type = 'TYPE_NAME'
		print('IDENTIFIER %s as TYPE_NAME' % (p.value))
		yacc.errok()
		return p
	if p.type == 'TYPE_NAME':
		p.type = 'IDENTIFIER'
		print('TYPE_NAME %s as IDENTIFIER' % (p.value))
		yacc.errok()
		return p
	if p.type == 'WHITESPACE':
		yacc.errok()
	else:
		raise Exception('Syntax Error : Unexpected ' + p.type +
			' pos = %d' % p.lexpos)

def p_empty(p):
    'empty :'
    pass

def do_test_parsing(file_name):
	yacc.yacc(debug=True)
	parser = yacc.yacc()
	#with open('.\\test.py','r') as input_file:
	with open(file_name, 'r') as input_file:
		input_text = input_file.read()
		res = parser.parse(input_text, lexer = c_lexer)
if __name__ == '__main__':
	do_test_parsing('.\\test.c')